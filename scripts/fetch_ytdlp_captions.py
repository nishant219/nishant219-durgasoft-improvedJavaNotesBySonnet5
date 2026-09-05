#!/usr/bin/env python3
"""Download real YouTube auto-captions via yt-dlp + Node (PO token)."""

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
YTDLP = ROOT / ".venv" / "bin" / "yt-dlp"
NODE = Path("/opt/homebrew/bin/node")


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


def json3_to_cues(raw: dict) -> list[tuple[float, str]]:
    cues = []
    for ev in raw.get("events") or []:
        segs = ev.get("segs")
        if not segs:
            continue
        text = "".join(s.get("utf8") or "" for s in segs)
        text = text.replace("\n", " ").replace("\xa0", " ").strip()
        if not text or text == "\n":
            continue
        start = ev.get("tStartMs", 0) / 1000.0
        if cues and cues[-1][1] == text and abs(start - cues[-1][0]) < 0.4:
            continue
        cues.append((start, text))
    return cues


def stamp(seconds: float) -> str:
    t = int(seconds)
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def download_json3(video_id: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    outtmpl = str(dest.with_suffix(""))  # yt-dlp adds .en.json3
    cmd = [
        str(YTDLP),
        *ytdlp_base_args(),
        "--write-auto-sub",
        "--sub-lang",
        "en",
        "--skip-download",
        "--sub-format",
        "json3",
        "-o",
        outtmpl + ".%(ext)s",
        f"https://www.youtube.com/watch?v={video_id}",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    produced = dest.parent / f"{dest.stem}.en.json3"
    if not produced.exists():
        # sometimes named without .en
        alts = list(dest.parent.glob(f"{dest.stem}*.json3"))
        if alts:
            produced = alts[0]
    if proc.returncode != 0 and not produced.exists():
        raise RuntimeError(proc.stderr[-1500:] or proc.stdout[-1500:] or "yt-dlp failed")
    if not produced.exists():
        raise RuntimeError("no json3 caption file written\n" + proc.stderr[-800:])
    return produced


def save_txt(meta: dict, cues: list[tuple[float, str]], path: Path) -> None:
    lines = [
        f"VIDEO {meta['index']:03d}",
        f"TITLE: {meta['title']}",
        f"URL: {meta['url']}",
        f"DURATION: {meta['duration']}",
        "LANGUAGE: English (auto-generated)",
        "SOURCE: real YouTube auto-captions (yt-dlp + node PO token)",
        "",
    ]
    for start, text in cues:
        lines.append(f"[{stamp(start)}] {text}")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    end = int(sys.argv[2]) if len(sys.argv) > 2 else start
    OUT.mkdir(exist_ok=True)
    ytdlp_dir = OUT / "ytdlp"
    ytdlp_dir.mkdir(exist_ok=True)
    rows = [r for r in load_playlist() if start <= r["index"] <= end]
    ok = 0
    for i, row in enumerate(rows, 1):
        idx = f"{row['index']:03d}"
        txt = OUT / f"{idx}-{row['id']}.txt"
        print(f"[{i}/{len(rows)}] {idx} {row['id']} {row['title'][:64]}", flush=True)
        try:
            raw_path = download_json3(row["id"], ytdlp_dir / idx)
            data = json.loads(raw_path.read_text(encoding="utf-8"))
            cues = json3_to_cues(data)
            if len(" ".join(t for _, t in cues)) < 200:
                raise RuntimeError(f"caption too short ({len(cues)} cues)")
            save_txt(row, cues, txt)
            payload = {**row, "cue_count": len(cues), "cues": [{"start": s, "text": t} for s, t in cues]}
            (OUT / f"{idx}-{row['id']}.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            chars = sum(len(t) for _, t in cues)
            print(f"    ok cues={len(cues)} chars={chars}", flush=True)
            ok += 1
        except Exception as e:
            print(f"    FAIL {e}", flush=True)
        time.sleep(1.5)
    print(f"done {ok}/{len(rows)}", flush=True)
    if ok < len(rows):
        sys.exit(1)


if __name__ == "__main__":
    main()
