# GAMES: editorial notes

How GAMES prints its crosswords, as found in review. The text step reads this file
(xword-ocr textstep.instructions); reviewers can check a transcription against it; the
gxd export will use it to convert to gxd's own conventions.

Each note: what GAMES does, how we transcribe it, and where it was settled.

- **Fill-in blanks** are printed as a long dash until about mid-1978 ("—— spree", "Bete ——")
  and as a rule after ("Magna ____"); in July/August 1978 it varies by puzzle. We keep the clue text as printed and tag each blank (the text
  step's "blanks"); the export writes tagged blanks as "___" and other long dashes as "--".
  A dash used as punctuation is not a blank. (Alex, 2026-10-17.)
- **Picture clues** (the Illustrated Crossword, 1977–78): a drawing in place of words. The
  clue is "[picture: what it shows]"; the drawing is saved beside the puzzle
  (pictures/<clue>.png) for when xd can carry images. (Alex, 2026-10-16.)
- **Headings**: a section banner ("PENCILWISE") is not a title. A label for the kind of
  puzzle ("Illustrated Crossword") over the puzzle's own name ("Armchair Safari"): the name
  is the title, the label a line labelled "kind". "Crossword Puzzle #1" over the grid is the
  Number. Which labelled lines go in the xd's Notes is decided at export, for the whole run.
  (games1977-09-01, reviewed.)
