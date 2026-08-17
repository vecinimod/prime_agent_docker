---
name: pdf-deck
description: Create PDF slide decks from structured content. Use when you need to generate presentation-style PDFs from research summaries or other structured text.
---

# PDF Deck

Create multi-page PDF slide decks with title slides and content slides.
Uses `fpdf2` — installed automatically by the skill's pyproject.toml.

Call directly from the kernel:

    from pdf_deck import Deck

    d = Deck()
    d.add_title_slide("Title", subtitle="Subtitle", author="Author")
    d.add_slide("Section 1", ["point one", "point two"])
    d.add_slide("Section 2", [("Key term", "definition"), "more info"])
    d.build("/app/output.pdf")

## API

- `Deck()` — create a slide deck (Letter size, portrait)
- `add_title_slide(title, subtitle, author, date)` — centered title slide
- `add_slide(title, lines, subtitle)` — content slide with header
  - `lines` can be `str` (bullet), or `tuple(bold_header, detail_text)`
- `build(path)` — render and save PDF, returns the path

## Notes

- Uses core Helvetica fonts (latin-1 only) — no special Unicode characters
- Header has dark blue bar with slide title and page numbers
- `multi_cell` auto-wraps long text
