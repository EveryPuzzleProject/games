# *GAMES*

*GAMES* is an American puzzle magazine, first published in September 1977.
Its first issue ran six crosswords, all signed "J.L.". From 1979 its puzzle
pages, "Pencilwise", were edited by Will Shortz, who ran them for well over
a decade before becoming the *New York Times* crossword editor. The constructors
include William Lutwiniak, Merl Reagle, Mike Shenk, Henry Hook, Stanley
Newman and many more.

A *GAMES* page usually holds several puzzles side by side: crosswords next to
word games, quizzes and logic puzzles. The answers are at the back of each
issue, in the "Answer Drawer". The scans come from the Internet Archive.

- 492 crosswords found, 1977–1999. The scans are thinner after 1989.
- **1977 through 1979 are open for review now** (release `games-1977-1979`).
- Each issue's 25×25 giant (for example "The World's Most Ornery Crossword",
  1980) can print two full sets of clues, Hard and Easier. These are held
  back until the packets can show both.
- Cryptics are out of scope and were left out.

## How you can help

- **Review puzzles with your AI agent.** From a [blitz](https://github.com/EveryPuzzleProject/blitz)
  checkout, `uv run blitz start 3 games` forks this repo, claims three open puzzles with a draft
  pull request, and downloads their scans; see blitz's `VOLUNTEER.md`.
- **Check puzzles against the scan** on the [review site](https://blitz.xwordapp.com/review/),
  once reviewed puzzles are posted there.

## What's here

| File | What it is |
|---|---|
| `puzzles.tsv` | Every puzzle the tools know of, with its state (open, not open yet, restored, needs a person + reason, missing). Written by the tools' sync; don't edit by hand. |
| `review-notes.md` | What a reviewer needs to know about *GAMES*'s pages; `blitz instructions games` prints it with the general rules. |
| `reviews/<puzzle>/` | Reviews sent as pull requests: the OCR reading (`ocr.json`) and the review (`review.json`). |
| `xd/` | The current .xd of every reviewed puzzle (from the OCR plus `fixes/`). |
| `fixes/fixes.toml` | Hand fixes to the harvest: page hints, typed grids. The corrections ledger (`fixes/corrections.jsonl`) starts with the first import. |
| Releases | Review packets (scan crops + OCR), one `.tar.gz` per puzzle. |

Page images live in the private `games-scans`. The tools are
[blitz](https://github.com/EveryPuzzleProject/blitz) and
[xword-ocr](https://github.com/EveryPuzzleProject/xword-ocr), which read this repo from a
checkout beside them.
