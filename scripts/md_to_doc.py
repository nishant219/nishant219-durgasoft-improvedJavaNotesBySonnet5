#!/usr/bin/env python3
"""Markdown -> Word-compatible .doc (HTML), tables in document order.

Replaces the old md -> docx -> doc chain, whose last hop appended every table
to the end of the body and leaked raw `**markdown**` into the text.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "notes"

HEAD = """<html xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:w="urn:schemas-microsoft-com:office:word">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>{title}</title>
<style>
body {{ font-family: Calibri, Arial, sans-serif; font-size: 11pt; line-height: 1.35;
  max-width: 46em; }}
h1 {{ font-size: 18pt; }}
h2 {{ font-size: 14pt; border-bottom: 1px solid #ccc; padding-bottom: 2px; }}
h3 {{ font-size: 12pt; }}
h4 {{ font-size: 11pt; }}
pre, code {{ font-family: Consolas, Courier New, monospace; }}
pre {{ font-size: 9pt; background: #f4f4f4; padding: 8px; white-space: pre-wrap;
  border-left: 3px solid #bbb; }}
code {{ font-size: 10pt; background: #f0f0f0; padding: 0 2px; }}
table {{ border-collapse: collapse; margin: 8px 0 16px 0; }}
td, th {{ border: 1px solid #666; padding: 4px 8px; vertical-align: top; }}
th {{ font-weight: bold; background: #eee; }}
blockquote {{ margin: 8px 0 8px 0; padding: 6px 12px; border-left: 4px solid #d0a000;
  background: #fffbe6; }}
</style>
</head>
<body>
"""
TAIL = "</body></html>\n"

HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
UL = re.compile(r"^\s*[-*]\s+(.*)$")
OL = re.compile(r"^\s*(\d+)\.\s+(.*)$")
TABLE_SEP = re.compile(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
HR = re.compile(r"^(-{3,}|\*{3,}|_{3,})$")
TOKEN = re.compile(
    r"(`[^`]+`|\*\*[^*]+\*\*|\[[^\]]+\]\([^)]+\)|(?<!\*)\*(?!\*)[^*]+\*(?!\*))"
)


def inline(text: str) -> str:
    """Markdown inline marks -> HTML, escaping everything else."""
    out = []
    pos = 0
    for m in TOKEN.finditer(text):
        out.append(html.escape(text[pos : m.start()]))
        raw = m.group(0)
        if raw.startswith("`"):
            out.append(f"<code>{html.escape(raw[1:-1])}</code>")
        elif raw.startswith("**"):
            out.append(f"<b>{html.escape(raw[2:-2])}</b>")
        elif raw.startswith("["):
            lm = re.match(r"\[([^\]]+)\]\(([^)]+)\)", raw)
            label, href = lm.group(1), lm.group(2)
            out.append(f'<a href="{html.escape(href, quote=True)}">{html.escape(label)}</a>')
        else:
            out.append(f"<i>{html.escape(raw[1:-1])}</i>")
        pos = m.end()
    out.append(html.escape(text[pos:]))
    return "".join(out)


def split_row(line: str) -> list[str]:
    line = line.strip().strip("|")
    return [c.strip() for c in line.split("|")]


def read_continuation(lines: list[str], i: int, buf: list[str]) -> int:
    """Absorb wrapped lines of a paragraph or list item into buf; return new i."""
    while i < len(lines):
        nxt = lines[i].strip()
        if not nxt or HR.match(nxt) or HEADING.match(nxt) or nxt.startswith(("```", ">", "|")):
            break
        if UL.match(lines[i]) or OL.match(lines[i]):
            break
        buf.append(nxt)
        i += 1
    return i


def render(lines: list[str]) -> str:
    """Render a block of markdown lines to HTML. Recurses for blockquotes."""
    parts: list[str] = []
    i = 0
    list_open: str | None = None

    def close_list() -> None:
        nonlocal list_open
        if list_open:
            parts.append(f"</{list_open}>\n")
            list_open = None

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            close_list()
            i += 1
            code = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            parts.append("<pre>" + html.escape("\n".join(code).strip("\n")) + "</pre>\n")
            continue

        if not stripped:
            close_list()
            i += 1
            continue

        if HR.match(stripped):
            close_list()
            parts.append("<hr>\n")
            i += 1
            continue

        hm = HEADING.match(stripped)
        if hm:
            close_list()
            level = min(len(hm.group(1)), 6)
            parts.append(f"<h{level}>{inline(hm.group(2).strip())}</h{level}>\n")
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and TABLE_SEP.match(lines[i + 1].strip()):
            close_list()
            rows = [split_row(stripped)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i].strip()))
                i += 1
            parts.append("<table>\n")
            for r, row in enumerate(rows):
                tag = "th" if r == 0 else "td"
                cells = "".join(f"<{tag}>{inline(c)}</{tag}>" for c in row)
                parts.append(f"<tr>{cells}</tr>\n")
            parts.append("</table>\n")
            continue

        if stripped.startswith(">"):
            close_list()
            quote: list[str] = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q = lines[i].strip()[1:]
                quote.append(q[1:] if q.startswith(" ") else q)
                i += 1
            # recurse: a callout may hold tables, code fences and lists
            parts.append(f"<blockquote>\n{render(quote)}</blockquote>\n")
            continue

        um, om = UL.match(line), OL.match(line)
        if um or om:
            kind = "ul" if um else "ol"
            if list_open != kind:
                close_list()
                parts.append(f"<{kind}>\n")
                list_open = kind
            item = [um.group(1) if um else om.group(2)]
            i += 1
            i = read_continuation(lines, i, item)
            parts.append(f"<li>{inline(' '.join(item))}</li>\n")
            continue

        # a paragraph runs until a blank line or the start of another block,
        # so inline marks may wrap across source lines
        close_list()
        para = [stripped]
        i = read_continuation(lines, i + 1, para)
        parts.append(f"<p>{inline(' '.join(para))}</p>\n")

    close_list()
    return "".join(parts)


def convert(md: str, title: str) -> str:
    body = render(md.replace("\r\n", "\n").split("\n"))
    return HEAD.format(title=html.escape(title)) + body + TAIL


def demo() -> None:
    md = (
        "# T\n\nsome **bold** and `code` and <script>\n\n"
        "| A | B |\n|---|---|\n| 1 | **2** |\n\n"
        "text after table\n\n- one\n- two\n\n```java\nint x = 1 < 2;\n```\n"
        "> warn **me**\n"
    )
    out = convert(md, "T")
    body = out.split("<body>", 1)[1]
    assert body.index("<table>") < body.index("text after table"), "table must stay in order"
    assert "<b>bold</b>" in body and "**" not in body, "bold must convert, no leakage"
    assert "&lt;script&gt;" in body, "html must be escaped"
    assert "<code>code</code>" in body
    assert "int x = 1 &lt; 2;" in body, "code must be escaped"
    assert body.count("<li>") == 2 and body.count("<ul>") == 1, "one list, two items"
    assert "<blockquote>" in body and "warn <b>me</b>" in body

    # a callout carries nested blocks, and bold survives a line wrap
    rich = convert(
        "> **Modern Java** — the count\n> is no longer 53.\n>\n"
        "> | V | N |\n> |---|---|\n> | 8 | 53 |\n>\n"
        "> ```java\n> int _ = 10;\n> ```\n",
        "T",
    )
    q = rich.split("<blockquote>", 1)[1].split("</blockquote>", 1)[0]
    assert "<table>" in q, "callout must keep its table"
    assert "<pre>" in q, "callout must keep its code block"
    assert "<b>Modern Java</b>" in q, "bold must survive the line wrap"
    assert "**" not in rich, "no raw markdown may leak"

    # a list item that wraps across source lines stays one item
    wrapped = convert("- **exit and\n  finalize** are methods\n- second\n", "T")
    assert wrapped.count("<li>") == 2, "wrapped line must not become a new item"
    assert "<b>exit and finalize</b>" in wrapped, "bold must survive the wrap"
    assert "**" not in wrapped
    print("demo ok")


def main() -> None:
    if len(sys.argv) >= 2 and sys.argv[1] == "--demo":
        demo()
        return
    if len(sys.argv) >= 3:
        src, dest = Path(sys.argv[1]), Path(sys.argv[2])
        dest.write_text(convert(src.read_text(encoding="utf-8"), src.stem), encoding="utf-8")
        print(dest)
        return
    n = 0
    for md in sorted(NOTES.rglob("*.md")):
        dest = md.with_suffix(".doc")
        dest.write_text(convert(md.read_text(encoding="utf-8"), md.stem), encoding="utf-8")
        n += 1
    print(f"converted {n} md -> doc")


if __name__ == "__main__":
    main()
