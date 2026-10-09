# Reviewing *GAMES* puzzles

What a reviewer needs to know about *GAMES* on top of the general rules in
blitz (`uv run blitz instructions games` prints both). Add to it when a review
round teaches something: say where to look, not what the answer is.

## About *GAMES*
- *GAMES* (1977 on) printed several puzzles on a page, each in its own ruled
  panel with a title and byline: crosswords next to word games, quizzes and
  logic puzzles. Only this puzzle's text belongs to it. Remove captions from
  the neighbouring panels, and check that every clue is this puzzle's (its
  number fits this grid and its answer fits the answer grid).
- Titles are set in large type above or beside the grid, and the OCR often
  misses them (`title` is empty) or takes the introduction for the title.
  Set `meta:title` to the printed title. Stars after a title (★, ★★, ★★★,
  read by OCR as `*`) are the magazine's difficulty rating, not part of the
  title: leave them out and give the rating in the note ("difficulty ★★").
  An introduction ("For solvers who enjoy crosswords on the challenging
  side...") is a caption, not the title. The title is the puzzle's own name
  ("Armchair Safari"), not a label for its kind ("Illustrated Crossword") or
  its number ("Crossword Puzzle #1"). Only when the puzzle has no name of its
  own is the label its title. A printed number goes in `"meta:puzzle_number"`,
  digits only (`"1"`), even when it's also in the title; mention a kind label
  in the note.
- Byline as printed ("by Merl H. Reagle"); the author is the name alone. Some
  early puzzles are signed with initials only ("J.L."): keep them as printed.
- "Answer Drawer, page 61", "Pencilwise continues on page 65" and similar
  page pointers are not part of the puzzle: remove them from captions. Text
  the magazine printed about this puzzle (an introduction, a test solver's
  comment on it) is a caption: keep it.
- Answers are printed at the back of the same issue (the "Answer Drawer"),
  many grids side by side. `answers.png` is this puzzle's grid cut from that
  page, sometimes from another scan of the same issue. If it doesn't fit this
  puzzle's grid and clues, it's the wrong key: say so ("blocker").
- Some scans are of copies a reader solved: pencilled letters in the grid,
  ticks or crossings-out next to clues. Ignore all handwriting. Only what was
  printed counts, in both the grid and the clues.
- Clues are numbered without a period ("12 Rolling stone"), and the Down list
  often continues in short columns under the grid. Abbreviation hints are
  part of the clue: keep ": 2 wds.", ": Abbr.", ": Fr." exactly as printed.
- In illustrated crosswords some clues are pictures. Write a picture clue as
  `[picture: ...]` with a few plain words for what's drawn, then any letters
  or words printed in or under the picture, exactly as printed:
  `[picture: a fried egg] S`. Describe only what's drawn, not the answer:
  "a teacup and saucer", not "china".
- Not every grid here is a crossword. If this one is a cryptic (clues that
  end in the answer's length, "(7)"), a word search, a logic puzzle or another
  kind of puzzle, set "ready": false, "remaining": "blocker" and start the
  note with "not a crossword:" and what it is. Don't review it further.
