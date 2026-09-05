#!/usr/bin/env python3
"""Fetch playlist metadata + English transcripts for a video range."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import YouTubeTranscriptApiException

ROOT = Path(__file__).resolve().parents[1]
PLAYLIST = ROOT / "notes" / "playlist.tsv"
OUT_DIR = ROOT / ".transcripts"


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
                "playlist_url": "https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0",
                "playlist": "java tutorial by durga sir",
                "instructor": "Durga Sir (Durga Software Solutions)",
            }
        )
    return rows


def fetch_one(api: YouTubeTranscriptApi, video_id: str) -> dict:
    listing = api.list(video_id)
    available = [
        {
            "language": t.language,
            "language_code": t.language_code,
            "generated": t.is_generated,
        }
        for t in listing
    ]
    # Prefer English; if manual English is a stub, use auto English; else any language.
    candidates = []
    for t in listing:
        candidates.append(t)
    chosen = None
    fetched = None
    # Try English generated first if both exist — manual uploads in this playlist are often empty.
    for prefer_generated in (True, False):
        for t in candidates:
            if t.language_code.startswith("en") and t.is_generated is prefer_generated:
                try:
                    fetched = t.fetch()
                    if sum(len(s.text) for s in fetched) > 200:
                        chosen = t
                        break
                except Exception:
                    continue
        if chosen:
            break
    if chosen is None:
        for t in candidates:
            try:
                fetched = t.fetch()
                chosen = t
                break
            except Exception:
                continue
    if chosen is None or fetched is None:
        raise YouTubeTranscriptApiException(f"No usable transcript for {video_id}")
    snippets = [{"start": round(s.start, 2), "duration": round(s.duration, 2), "text": s.text} for s in fetched]
    text = " ".join(s["text"].replace("\n", " ") for s in snippets)
    return {
        "language": chosen.language,
        "language_code": chosen.language_code,
        "generated": chosen.is_generated,
        "available": available,
        "snippet_count": len(snippets),
        "snippets": snippets,
        "text": text,
    }


def main() -> None:
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    end = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    OUT_DIR.mkdir(exist_ok=True)
    api = YouTubeTranscriptApi()
    rows = [r for r in load_playlist() if start <= r["index"] <= end]
    summary = []
    for i, row in enumerate(rows, 1):
        out = OUT_DIR / f"{row['index']:03d}-{row['id']}.json"
        print(f"[{i}/{len(rows)}] {row['index']:03d} {row['id']} {row['title'][:70]}", flush=True)
        try:
            data = fetch_one(api, row["id"])
            payload = {**row, **data}
            out.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
            txt = OUT_DIR / f"{row['index']:03d}-{row['id']}.txt"
            lines = [
                f"VIDEO {row['index']:03d}",
                f"TITLE: {row['title']}",
                f"URL: {row['url']}",
                f"DURATION: {row['duration']}",
                f"LANGUAGE: {data['language']} ({'auto' if data['generated'] else 'manual'})",
                "",
            ]
            for s in data["snippets"]:
                m, sec = divmod(int(s["start"]), 60)
                h, m = divmod(m, 60)
                stamp = f"{h:d}:{m:02d}:{sec:02d}" if h else f"{m:02d}:{sec:02d}"
                lines.append(f"[{stamp}] {s['text'].replace(chr(10), ' ')}")
            txt.write_text("\n".join(lines))
            summary.append(
                {
                    "index": row["index"],
                    "ok": True,
                    "file": str(out),
                    "chars": len(data["text"]),
                    "snippets": data["snippet_count"],
                }
            )
            print(f"    ok snippets={data['snippet_count']} chars={len(data['text'])}", flush=True)
        except YouTubeTranscriptApiException as e:
            summary.append({"index": row["index"], "ok": False, "error": str(e)})
            print(f"    FAIL {e}", flush=True)
            time.sleep(1.2)
    (OUT_DIR / f"summary-{start:03d}-{end:03d}.json").write_text(json.dumps(summary, indent=2))
    failed = [s for s in summary if not s.get("ok")]
    print(f"done {len(summary)-len(failed)}/{len(summary)} ok", flush=True)
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
