from __future__ import annotations

import html
import re


TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$")
ORDERED_ITEM_RE = re.compile(r"^\d+\.\s+")
LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+|[A-Za-z0-9_./#-]+\.md|[A-Za-z0-9_./#-]+)\)")


def render_markdown(text: str) -> str:
    """Render the small Markdown subset used by the project docs.

    This renderer intentionally supports only safe, static documentation
    constructs: headings, paragraphs, bullet/numbered lists, fenced code blocks,
    tables, links, and inline code. Raw HTML is escaped.
    """
    lines = text.splitlines()
    html_parts: list[str] = []
    index = 0
    list_kind: str | None = None
    in_code = False
    code_lines: list[str] = []
    code_lang = ""

    def close_list() -> None:
        nonlocal list_kind
        if list_kind:
            html_parts.append(f"</{list_kind}>")
            list_kind = None

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if in_code:
            if stripped.startswith("```"):
                html_parts.append(
                    f'<pre class="doc-code"><code data-lang="{html.escape(code_lang)}">'
                    + html.escape("\n".join(code_lines))
                    + "</code></pre>"
                )
                in_code = False
                code_lines = []
                code_lang = ""
            else:
                code_lines.append(line)
            index += 1
            continue

        if stripped.startswith("```"):
            close_list()
            in_code = True
            code_lang = stripped[3:].strip()
            index += 1
            continue

        if not stripped:
            close_list()
            index += 1
            continue

        if _is_table_start(lines, index):
            close_list()
            table_html, next_index = _render_table(lines, index)
            html_parts.append(table_html)
            index = next_index
            continue

        if stripped.startswith("#"):
            close_list()
            level = min(len(stripped) - len(stripped.lstrip("#")), 4)
            content = stripped[level:].strip()
            if content:
                html_parts.append(f"<h{level}>{_render_inline(content)}</h{level}>")
                index += 1
                continue

        if stripped.startswith("- "):
            if list_kind != "ul":
                close_list()
                html_parts.append("<ul>")
                list_kind = "ul"
            html_parts.append(f"<li>{_render_inline(stripped[2:].strip())}</li>")
            index += 1
            continue

        if ORDERED_ITEM_RE.match(stripped):
            if list_kind != "ol":
                close_list()
                html_parts.append("<ol>")
                list_kind = "ol"
            item = ORDERED_ITEM_RE.sub("", stripped, count=1).strip()
            html_parts.append(f"<li>{_render_inline(item)}</li>")
            index += 1
            continue

        close_list()
        paragraph_lines = [stripped]
        index += 1
        while index < len(lines):
            next_line = lines[index].strip()
            if (
                not next_line
                or next_line.startswith("#")
                or next_line.startswith("- ")
                or next_line.startswith("```")
                or ORDERED_ITEM_RE.match(next_line)
                or _is_table_start(lines, index)
            ):
                break
            paragraph_lines.append(next_line)
            index += 1
        html_parts.append(f"<p>{_render_inline(' '.join(paragraph_lines))}</p>")

    close_list()
    if in_code:
        html_parts.append(
            f'<pre class="doc-code"><code data-lang="{html.escape(code_lang)}">'
            + html.escape("\n".join(code_lines))
            + "</code></pre>"
        )

    return "\n".join(html_parts)


def _is_table_start(lines: list[str], index: int) -> bool:
    return (
        index + 1 < len(lines)
        and "|" in lines[index]
        and TABLE_SEPARATOR_RE.match(lines[index + 1].strip()) is not None
    )


def _render_table(lines: list[str], index: int) -> tuple[str, int]:
    header = _split_table_row(lines[index])
    rows: list[list[str]] = []
    index += 2
    while index < len(lines) and "|" in lines[index] and lines[index].strip():
        rows.append(_split_table_row(lines[index]))
        index += 1

    parts = ['<div class="doc-table-wrap"><table class="doc-table"><thead><tr>']
    for cell in header:
        parts.append(f"<th>{_render_inline(cell)}</th>")
    parts.append("</tr></thead><tbody>")
    for row in rows:
        parts.append("<tr>")
        for cell in row:
            parts.append(f"<td>{_render_inline(cell)}</td>")
        parts.append("</tr>")
    parts.append("</tbody></table></div>")
    return "".join(parts), index


def _split_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def _render_inline(text: str) -> str:
    placeholders: list[str] = []

    def stash(value: str) -> str:
        placeholders.append(value)
        return f"\x00{len(placeholders) - 1}\x00"

    def link_repl(match: re.Match[str]) -> str:
        label = html.escape(match.group(1))
        href = _normalize_href(match.group(2))
        href = html.escape(href, quote=True)
        return stash(f'<a href="{href}">{label}</a>')

    text = LINK_RE.sub(link_repl, text)

    def code_repl(match: re.Match[str]) -> str:
        return stash(f"<code>{html.escape(match.group(1))}</code>")

    text = re.sub(r"`([^`]+)`", code_repl, text)
    rendered = html.escape(text)
    for idx, value in enumerate(placeholders):
        rendered = rendered.replace(html.escape(f"\x00{idx}\x00"), value)
    return rendered


def _normalize_href(href: str) -> str:
    if href.startswith("http://") or href.startswith("https://"):
        return href
    if ".md" in href:
        clean = href.lstrip("./")
        while clean.startswith("../"):
            clean = clean[3:]
        return f"/doc/{clean}"
    return href
