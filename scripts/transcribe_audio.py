#!/usr/bin/env python3
"""Download audio via yt-dlp+node, then Whisper-transcribe to .transcripts."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYLIST = ROOT / "notes" / "playlist.tsv"
OUT = ROOT / ".transcripts"
AUDIO = ROOT / ".audio"
YTDLP = ROOT / ".venv" / "bin" / "yt-dlp"
NODE = Path("/opt/homebrew/bin/node")
PY = ROOT / ".venv" / "bin" / "python"


def ytdlp_base_args() -> list[str]:
    args = ["--remote-components", "ejs:github", "--js-runtimes", f"node:{NODE}"]
    browser = os.environ.get("YTDLP_COOKIES_BROWSER", "brave")
    if browser:
        args.extend(["--cookies-from-browser", browser])
    return args


def fmt_duration(seconds: int) -> str:
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m:02d}m {s:02d}s"
    return f"{m}m {s:02d}s"


def stamp(seconds: float) -> str:
    t = int(seconds)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def load_playlist() -> list[dict]:
    rows = []
    for line in PLAYLIST.read_text().splitlines():
        if not line.strip():
            continue
        idx, vid, dur, title = line.split("\t", 3)
        seconds = int(dur)
        rows.append(
            {
                "index": int(idx),
                "id": vid,
                "duration_seconds": seconds,
                "duration": fmt_duration(seconds),
                "title": title,
                "url": f"https://www.youtube.com/watch?v={vid}",
            }
        )
    return rows


def download_audio(video_id: str, dest_stem: Path) -> Path:
    AUDIO.mkdir(parents=True, exist_ok=True)
    produced = dest_stem.with_suffix(".mp3")
    if produced.exists() and produced.stat().st_size > 100_000:
        print(f"    reuse {produced.name}", flush=True)
        return produced
    alts = [
        p
        for p in dest_stem.parent.glob(dest_stem.name + ".*")
        if p.suffix.lower() in {".mp3", ".m4a", ".webm", ".opus", ".wav"} and p.stat().st_size > 100_000
    ]
    if alts:
        print(f"    reuse {alts[0].name}", flush=True)
        return alts[0]
    outtmpl = str(dest_stem) + ".%(ext)s"
    cmd = [
        str(YTDLP),
        *ytdlp_base_args(),
        "-f",
        "ba/b",
        "-x",
        "--audio-format",
        "mp3",
        "--audio-quality",
        "5",
        "-o",
        outtmpl,
        f"https://www.youtube.com/watch?v={video_id}",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    produced = dest_stem.with_suffix(".mp3")
    if not produced.exists():
        alts = list(dest_stem.parent.glob(dest_stem.name + ".*"))
        alts = [p for p in alts if p.suffix.lower() in {".mp3", ".m4a", ".webm", ".opus", ".wav"}]
        if alts:
            produced = alts[0]
    if proc.returncode != 0 and not produced.exists():
        raise RuntimeError(proc.stderr[-1500:] or proc.stdout[-1500:] or "yt-dlp audio failed")
    if not produced.exists():
        raise RuntimeError("no audio file written\n" + (proc.stderr[-800:] or ""))
    return produced


def transcribe(path: Path, model, *, beam_size: int = 1) -> list[tuple[float, str]]:
    segments, _info = model.transcribe(
        str(path),
        language="en",
        vad_filter=True,
        beam_size=beam_size,
        condition_on_previous_text=False,
    )
    cues = []
    last_report = -60.0
    for seg in segments:
        text = (seg.text or "").replace("\n", " ").strip()
        if text:
            cues.append((float(seg.start), text))
        if seg.start - last_report >= 60:
            print(f"    … {stamp(seg.start)} cues={len(cues)}", flush=True)
            last_report = float(seg.start)
    return cues


def save_txt(meta: dict, cues: list[tuple[float, str]], path: Path) -> None:
    lines = [
        f"VIDEO {meta['index']:03d}",
        f"TITLE: {meta['title']}",
        f"URL: {meta['url']}",
        f"DURATION: {meta['duration']}",
        "LANGUAGE: English (Whisper STT)",
        "SOURCE: local Whisper transcription of yt-dlp audio (no YouTube captions available)",
        "",
    ]
    for start, text in cues:
        lines.append(f"[{stamp(start)}] {text}")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: transcribe_audio.py INDEX [INDEX2 ...] [--model SIZE]", file=sys.stderr)
        sys.exit(2)
    argv = sys.argv[1:]
    model = "base"
    if "--model" in argv:
        i = argv.index("--model")
        model = argv[i + 1]
        argv = argv[:i] + argv[i + 2 :]
    indices = {int(a) for a in argv if not a.startswith("--")}
    rows = [r for r in load_playlist() if r["index"] in indices]
    # preserve playlist order
    rows.sort(key=lambda r: r["index"])
    OUT.mkdir(exist_ok=True)
    from faster_whisper import WhisperModel

    print(f"loading whisper model={model}", flush=True)
    whisper = WhisperModel(model, device="cpu", compute_type="int8")
    ok = 0
    for i, row in enumerate(rows, 1):
        idx = f"{row['index']:03d}"
        txt = OUT / f"{idx}-{row['id']}.txt"
        print(f"[{i}/{len(rows)}] {idx} {row['id']} {row['duration']} {row['title'][:50]}", flush=True)
        if row["duration_seconds"] > 3 * 3600:
            print("    SKIP mega video (>3h) — use compilation index notes", flush=True)
            continue
        if txt.exists() and txt.stat().st_size > 500:
            print(f"    SKIP existing {txt.name}", flush=True)
            ok += 1
            continue
        try:
            audio = download_audio(row["id"], AUDIO / idx)
            print(f"    audio {audio.name} ({audio.stat().st_size // 1_000_000}MB)", flush=True)
            t0 = time.time()
            cues = transcribe(audio, whisper)
            if len(" ".join(t for _, t in cues)) < 200:
                raise RuntimeError(f"transcript too short ({len(cues)} cues)")
            save_txt(row, cues, txt)
            payload = {
                **row,
                "cue_count": len(cues),
                "source": "whisper",
                "cues": [{"start": s, "text": t} for s, t in cues],
            }
            (OUT / f"{idx}-{row['id']}.json").write_text(
                json.dumps(payload, ensure_ascii=False), encoding="utf-8"
            )
            chars = sum(len(t) for _, t in cues)
            print(f"    ok cues={len(cues)} chars={chars} in {time.time()-t0:.0f}s", flush=True)
            ok += 1
        except Exception as e:
            print(f"    FAIL {e}", flush=True)
        time.sleep(1)
    print(f"done {ok}/{len(rows)}", flush=True)
    if ok < len(rows):
        sys.exit(1)


if __name__ == "__main__":
    main()
