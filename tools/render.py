#!/usr/bin/env python3
"""Render the GAMES status page, site/index.html (plus a copy of puzzles.tsv),
from puzzles.tsv. Runs in CI on every push to main; locally:

    python tools/render.py

GAMES is in copyright: the page shows metadata only (issue, puzzle number,
state, reason), never clues, grids or page images.
"""
import collections
import csv
import datetime as dt
import html
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = "https://everypuzzleproject.org/"
REPO = "https://github.com/EveryPuzzleProject/games"
BLITZ = "https://github.com/EveryPuzzleProject/blitz"
VOLUNTEER = "https://github.com/EveryPuzzleProject/blitz/blob/main/VOLUNTEER.md"
REVIEW_SITE = "https://blitz.xwordapp.com/review/"
RECORD = "https://blitz.xwordapp.com/view.html?p=games/"
ISSUES = "https://github.com/EveryPuzzleProject/blitz/issues"
XD = "https://github.com/century-arcade/xdformat"
# puzzles.tsv state -> (label, colour), in display order. Same states and
# colours as blitz's home page. Only restored counts toward done.
STATES = {
    "restored": ("Restored", "#3f8f5f"),
    "needs-person": ("Needs a person", "#d9822b"),
    "review": ("In review", "#3b6fb6"),
    "open": ("Open for review", "#a9c3e6"),
    "later": ("Not open yet", "var(--later)"),
    "missing": ("Missing", "transparent"),
}
LINKED = {"restored", "review", "needs-person"}  # states with a record page
REASONS = {  # blitz's reason codes (docs/puzzle.js)
    "scan-missing": "Part of the scan is missing",
    "no-key": "Answer key not found",
    "unread": "Some answer squares can't be read",
    "quick": "One small check left",
    "ruling": "A printed mistake to rule on",
    "not-found": "Not found in the scans yet",
}


def e(s) -> str:
    return html.escape(str(s or ""))


def issue(date: str) -> str:
    """'1977-09-01' -> 'September 1977' (GAMES dates are issues, not days)."""
    d = dt.date.fromisoformat(date)
    return f"{d:%B} {d.year}"


def main() -> None:
    rows = list(csv.DictReader(open(ROOT / "puzzles.tsv", encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE))
    rows = [r for r in rows if r.get("date")]
    rows.sort(key=lambda r: (r["date"], r["xdid"]))
    count = collections.Counter(r["state"] for r in rows)
    order = list(STATES) + sorted(s for s in count if s not in STATES)  # unknown states last, grey
    label = lambda s: STATES.get(s, (s, ""))[0]
    colour = lambda s: STATES.get(s, ("", "#999"))[1]
    total, done = len(rows), count["restored"]

    def title(r) -> str:
        bits = [f"{issue(r['date'])} issue"]
        if r["number"]:
            bits.append(f"No. {r['number']}")
        bits.append(label(r["state"]))
        t = " · ".join(bits)
        if r["reason"]:
            t += f": {REASONS.get(r['reason'], r['reason'])}"
        return t

    def tile(r) -> str:
        cls = f'tile st-{e(r["state"])}'
        t = e(title(r))
        if r["state"] in LINKED:
            return f'<a class="{cls}" href="{RECORD}{e(r["xdid"])}" title="{t}" aria-label="{t}"></a>'
        return f'<span class="{cls}" title="{t}"></span>'

    bar = "".join(f'<span class="st-{s}" style="width:{100 * count[s] / total:.3f}%" title="{e(label(s))}: {count[s]}"></span>'
                  for s in order if count[s])
    legend = "".join(f'<span><i class="sw st-{s}"></i><b>{count[s]}</b> {e(label(s).lower())}</span>' for s in order if count[s])

    years = collections.defaultdict(list)
    for r in rows:
        years[r["date"][:4]].append(r)
    year_rows = "\n".join(
        f'<div class="yr">{y}<small>{sum(r["state"] == "restored" for r in rs)} of {len(rs)}</small></div>'
        f'<div class="tiles">{"".join(tile(r) for r in rs)}</div>'
        for y, rs in sorted(years.items()))

    wanted_rows = [r for r in rows if r["state"] in ("needs-person", "missing")]
    groups = collections.defaultdict(list)
    for r in wanted_rows:
        groups[r["reason"] or "other"].append(r)

    def wanted_item(r) -> str:
        text = f"{issue(r['date'])}" + (f", No. {r['number']}" if r["number"] else "")
        if r["state"] in LINKED:
            return f'<li><a href="{RECORD}{e(r["xdid"])}">{e(text)}</a></li>'
        return f"<li>{e(text)}</li>"

    if groups:
        wanted = "\n".join(
            f'<details><summary>{e(REASONS.get(why, why))} <span>· {len(rs)}</span></summary>'
            f'<ul>{"".join(wanted_item(r) for r in rs)}</ul></details>'
            for why, rs in sorted(groups.items(), key=lambda kv: -len(kv[1])))
    else:
        wanted = '<p class="muted">Nothing right now: no puzzle is waiting on a person or missing from the scans.</p>'

    states_css = "\n".join(f".st-{s} {{ background:{c}; }}" for s, (_, c) in STATES.items())
    first, last = rows[0]["date"][:4], rows[-1]["date"][:4]

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GAMES crosswords</title>
<meta name="description" content="Every Puzzle Project: indexing and restoring the crosswords in GAMES magazine, 1977 on.">
<style>
:root {{ --bg:#fbfaf7; --fg:#1d1d1b; --muted:#6b6a65; --line:#e3e0d8; --card:#fff; --accent:#8a1c1c; --later:#dcd8ce; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#161614; --fg:#ecebe6; --muted:#a3a19a; --line:#34332f; --card:#1f1f1c; --accent:#e07a6a; --later:#45443f; }} }}
:root[data-theme="dark"] {{ --bg:#161614; --fg:#ecebe6; --muted:#a3a19a; --line:#34332f; --card:#1f1f1c; --accent:#e07a6a; --later:#45443f; }}
* {{ box-sizing:border-box }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:16px/1.55 Georgia, "Times New Roman", serif }}
main {{ max-width:960px; margin:0 auto; padding:24px 16px 64px }}
nav.top {{ font:14px system-ui, sans-serif; display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap }}
h1 {{ font-size:2.2rem; margin:20px 0 4px }} h1 i {{ font-style:italic }}
h2 {{ margin:40px 0 10px; font-size:1.35rem; border-bottom:2px solid var(--fg); padding-bottom:4px }}
a {{ color:var(--accent) }} .muted {{ color:var(--muted) }} .lede {{ font-size:1.1rem; max-width:44em }}
.sans {{ font-family:system-ui, sans-serif }}
.big {{ font:700 48px/1 Georgia, serif; margin:18px 0 0 }} .big small {{ font:500 16px system-ui, sans-serif; color:var(--muted); margin-left:6px }}
.bar {{ display:flex; gap:2px; height:16px; border-radius:8px; overflow:hidden; background:var(--line); margin:14px 0 10px }}
.bar span {{ display:block; height:100% }}
.legend {{ display:flex; flex-wrap:wrap; gap:6px 18px; font:14px system-ui, sans-serif; color:var(--muted) }}
.legend b {{ color:var(--fg); font-weight:600 }}
.sw {{ display:inline-block; width:12px; height:12px; border-radius:3px; margin-right:6px; vertical-align:-1px }}
{states_css}
.st-open {{ box-shadow:inset 0 0 0 1px #3b6fb6 }}
.st-missing {{ border:1.5px dashed var(--muted) }}
.bar .st-missing {{ border:0; background:repeating-linear-gradient(135deg, var(--muted) 0 2px, transparent 2px 6px); opacity:.6 }}
.years {{ display:grid; grid-template-columns:92px 1fr; gap:8px 12px; align-items:start; margin-top:12px }}
.yr {{ font:600 15px Georgia, serif; white-space:nowrap }} .yr small {{ display:block; font:12px system-ui, sans-serif; color:var(--muted); font-weight:400 }}
.tiles {{ display:flex; flex-wrap:wrap; gap:3px }}
.tile {{ display:block; width:15px; height:15px; border-radius:3px }}
a.tile:hover, a.tile:focus {{ outline:2px solid var(--fg); outline-offset:1px }}
.wanted details {{ border-top:1px solid var(--line); padding:8px 0; font-family:system-ui, sans-serif }}
.wanted summary {{ cursor:pointer; font-weight:600 }} .wanted summary span {{ color:var(--muted); font-weight:400 }}
.wanted ul {{ margin:6px 0 0; columns:2 220px }}
.cta {{ background:var(--card); border:1px solid var(--line); border-left:4px solid var(--accent); padding:14px 20px }}
.cta ul {{ margin:0; padding-left:20px }} .cta li + li {{ margin-top:8px }}
code {{ font-size:.9em; background:var(--line); padding:1px 4px; border-radius:3px }}
footer {{ margin-top:48px; font:13px system-ui, sans-serif; color:var(--muted) }}
@media (max-width:560px) {{ .years {{ grid-template-columns:1fr; gap:2px 0 }} .tiles {{ margin-bottom:10px }} h1 {{ font-size:1.8rem }} .big {{ font-size:40px }} }}
</style></head><body><main>
<nav class="top"><a href="{HOME}">← Every Puzzle Project</a><a href="{REPO}">EveryPuzzleProject/games on GitHub</a></nav>

<h1><i>GAMES</i>, 1977 on</h1>
<p class="lede"><i>GAMES</i>, the American puzzle magazine, first appeared in September 1977, and from 1979 its puzzle pages,
"Pencilwise", were edited by Will Shortz. We're indexing every crossword it printed and restoring each one, checked against
scans from the Internet Archive, as an <a href="{XD}">xd</a> file, so the puzzles are preserved and searchable.</p>
<p class="muted sans" style="font-size:14px">The magazine is in copyright, so this page lists only when each puzzle ran and how far it has
got: no clues, grids or page images.</p>

<h2>Progress</h2>
<div class="big">{done}<small>of {total} crosswords restored</small></div>
<div class="bar">{bar}</div>
<div class="legend">{legend}</div>

<h2>Year by year, {first}–{last}</h2>
<p class="muted sans" style="font-size:14px;margin:0">Every crossword found so far, one square each, by issue. Hover a square for its issue
and state; click a filled one to see its record. The scans thin out after 1989.</p>
<div class="years">
{year_rows}
</div>

<h2>Wanted: people</h2>
<div class="wanted">
<p class="sans" style="font-size:15px;margin-top:0">Puzzles Claude can't finish alone, grouped by what they need. If you can find a missing page,
a cleaner scan or an answer key, <a href="{ISSUES}">open an issue</a> (please don't upload page images: issues are public).</p>
{wanted}
</div>

<h2>How you can help</h2>
<div class="cta sans"><ul>
<li><b>Check puzzles against the scan</b> on the <a href="{REVIEW_SITE}">review site</a>, once reviewed puzzles are posted there. No account needed.</li>
<li><b>Review puzzles with your AI agent.</b> From a <a href="{BLITZ}">blitz</a> checkout, <code>uv run blitz start 3 games</code> forks this repo,
claims three open puzzles with a draft pull request, and downloads their scans; see <a href="{VOLUNTEER}">VOLUNTEER.md</a>.</li>
</ul></div>

<footer>Part of the <a href="{HOME}">Every Puzzle Project</a>. Data: <a href="{REPO}">EveryPuzzleProject/games</a>
(<a href="puzzles.tsv">puzzles.tsv</a>), written by the <a href="{BLITZ}">blitz</a> tools. Generated {dt.date.today().isoformat()}.</footer>
</main></body></html>
"""
    out = ROOT / "site"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8", newline="\n")
    shutil.copy(ROOT / "puzzles.tsv", out / "puzzles.tsv")
    print(f"site/index.html: {total} puzzles, {dict(count)}, {len(wanted_rows)} wanted")


if __name__ == "__main__":
    main()
