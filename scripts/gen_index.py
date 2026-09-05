#!/usr/bin/env python3
"""Regenerate notes/00-playlist-index.md and notes/README.md from playlist.tsv
plus whatever note files actually exist on disk."""

from __future__ import annotations

import glob
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "notes"
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0"

CHUNKS = [(1, 20), (21, 40), (41, 60), (61, 80), (81, 100),
          (101, 120), (121, 140), (141, 160), (161, 180), (181, 203)]


def hms(sec: int) -> str:
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h}h {m:02d}m {s:02d}s" if h else f"{m}m {s:02d}s"


def clean_title(t: str) -> str:
    """Strip the boilerplate course prefix, keep the actual topic."""
    t = re.sub(r"^\s*Core\s*Java\s*(with|With)?\s*OCJP\s*/\s*SCJP\s*:?\s*", "", t)
    t = t.replace("||", " — ").replace("|", " — ")
    t = re.sub(r"\s{2,}", " ", t).strip(" —\t")
    return t


def esc(t: str) -> str:
    return t.replace("|", "\\|")


def main() -> None:
    rows = []
    for line in (NOTES / "playlist.tsv").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        num, vid, dur, title = line.split("\t", 3)
        rows.append((num, vid, int(dur), title))

    note_for: dict[str, str] = {}
    for f in glob.glob(str(NOTES / "chunk-*" / "[0-9][0-9][0-9]-*.md")):
        num = os.path.basename(f)[:3]
        note_for[num] = os.path.relpath(f, NOTES)

    total = sum(r[2] for r in rows)
    covered = sum(1 for r in rows if r[0] in note_for)

    out: list[str] = []
    out += [
        "# Core Java with OCJP/SCJP — Durga Sir — Playlist index",
        "",
        f"- **Instructor:** Durga Sir (Durga Software Solutions)",
        f"- **Videos:** {len(rows)}",
        f"- **Total runtime:** {hms(total)}",
        f"- **Notes written:** {covered} of {len(rows)}",
        f"- **Playlist:** {PLAYLIST_URL}",
        "",
        "Notes are corrected against a real compiler (javac 26) and carry",
        "**⚠️ Modern Java** callouts wherever the language moved on since this",
        "Java 6/7-era recording, plus **❗ Correction** boxes where the lecture is",
        "inaccurate. Each video has a `.md`, `.docx` and `.doc` version.",
        "",
        "## Coverage by chunk",
        "",
        "| Chunk | Videos | Notes | Runtime |",
        "|---|---|---|---|",
    ]
    for lo, hi in CHUNKS:
        span = [r for r in rows if lo <= int(r[0]) <= hi]
        if not span:
            continue
        done = sum(1 for r in span if r[0] in note_for)
        mark = "✅" if done == len(span) else ("—" if done == 0 else f"{done}/{len(span)}")
        out.append(
            f"| chunk-{lo:03d}-{hi:03d} | {lo:03d}–{hi:03d} | {mark} | {hms(sum(r[2] for r in span))} |"
        )

    missing = [r[0] for r in rows if r[0] not in note_for]
    if missing:
        out += ["", f"**Not yet written ({len(missing)}):** " + ", ".join(missing), ""]

    out += ["", "## All videos", "", "| # | Duration | Topic | Video | Notes |", "|---|---|---|---|---|"]
    for num, vid, dur, title in rows:
        link = f"[watch](https://www.youtube.com/watch?v={vid})"
        note = f"[notes]({note_for[num]})" if num in note_for else "—"
        out.append(f"| {num} | {hms(dur)} | {esc(clean_title(title))} | {link} | {note} |")

    (NOTES / "00-playlist-index.md").write_text("\n".join(out) + "\n", encoding="utf-8")

    readme = [
        "# Durga Sir — Core Java (OCJP/SCJP) study notes",
        "",
        f"Detailed notes from the {len(rows)}-video *Core Java with OCJP/SCJP* playlist by",
        f"Durga Sir ({hms(total)} of lecture). One file per video.",
        "",
        f"**Coverage:** {covered} of {len(rows)} videos.",
        "",
        "## How these notes differ from the raw lecture",
        "",
        "The recordings date from the Java 6/7 era, so the notes are not a plain",
        "transcript. Every note has been through a correctness pass:",
        "",
        "- Technical claims are checked against a real compiler (**javac 26**).",
        "- **⚠️ Modern Java** callouts mark what has changed since the recording,",
        "  and in which release — while keeping what Sir taught, because that is",
        "  still the OCJP answer and still true of legacy code.",
        "- **❗ Correction** callouts mark statements that are inaccurate.",
        "- Auto-caption noise has been decoded and removed.",
        "",
        "## Anatomy of a note",
        "",
        "1. Video info — title, position, duration, link",
        "2. What this lecture covers — the agenda",
        "3. Timestamped sections following the lecture, with code and tables inline",
        "4. Exam and interview points",
        "",
        "## Formats",
        "",
        "| File | Use |",
        "|---|---|",
        "| `.md` | the source; edit this one |",
        "| `.docx` | Word |",
        "| `.doc` | Word (HTML-based), opens anywhere |",
        "",
        "Regenerate the Word versions after editing any Markdown:",
        "",
        "```bash",
        ".venv/bin/python scripts/md_to_docx.py     # .md -> .docx",
        ".venv/bin/python scripts/md_to_doc.py      # .md -> .doc",
        ".venv/bin/python scripts/gen_index.py      # rebuild this index",
        "```",
        "",
        "## Index",
        "",
        "Full video list with links: [00-playlist-index.md](00-playlist-index.md)",
        "",
        "| Chunk | Videos | Notes |",
        "|---|---|---|",
    ]
    for lo, hi in CHUNKS:
        span = [r for r in rows if lo <= int(r[0]) <= hi]
        if not span:
            continue
        done = sum(1 for r in span if r[0] in note_for)
        mark = "✅ all" if done == len(span) else ("— none" if done == 0 else f"{done} of {len(span)}")
        readme.append(f"| [chunk-{lo:03d}-{hi:03d}](chunk-{lo:03d}-{hi:03d}/) | {lo:03d}–{hi:03d} | {mark} |")

    (NOTES / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    print(f"index: {covered}/{len(rows)} notes, {hms(total)} runtime")


if __name__ == "__main__":
    main()
