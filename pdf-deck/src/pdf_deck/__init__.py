"""PDF slide deck builder using fpdf2."""

from __future__ import annotations

from fpdf import FPDF


class Deck(FPDF):
    """Create multi-page PDF slide decks.

    Usage:

        d = Deck()
        d.add_title_slide("Title", subtitle="Subtitle")
        d.add_slide("Section", ["bullet 1", "bullet 2"])
        d.build("/path/to/output.pdf")
    """

    MARGIN = 20
    HEADER_H = 25

    def __init__(self, orientation='P', unit='mm', format='Letter'):
        super().__init__(orientation=orientation, unit=unit, format=format)
        self.set_auto_page_break(False)
        self.set_title('Research Summary')
        self._header_text = ''

    def header(self):
        self.set_fill_color(0, 51, 102)
        self.rect(
            x=self.MARGIN, y=0,
            w=self.w - 2 * self.MARGIN,
            h=self.HEADER_H,
            style='F',
        )
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.text(x=self.MARGIN + 5, y=16, text=self._header_text or '')
        self.set_font('Helvetica', '', 9)
        total = len(self.pages)
        self.text(
            x=self.w - self.MARGIN - 5,
            y=16,
            text=f'{self.page_no()}/{total}',
        )

    def footer(self):
        pass

    def add_slide(self, title: str, lines: list, subtitle: str = '') -> None:
        """Add a content slide.

        Args:
            title: Slide title shown in header and on the slide.
            lines: List of strings (bullets) or tuples (bold_header, detail).
            subtitle: Optional subtitle line below the title.
        """
        self.add_page()
        self._header_text = title
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(0, 0, 0)
        y = self.HEADER_H + 15
        self.text(x=self.MARGIN + 5, y=y, text=title)
        if subtitle:
            self.set_font('Helvetica', '', 12)
            self.set_text_color(100, 100, 100)
            y += 12
            self.text(x=self.MARGIN + 5, y=y, text=subtitle)
        y += 15
        self.set_text_color(0, 0, 0)
        for line in lines:
            if isinstance(line, tuple):
                bullet, detail = line
                self.set_font('Helvetica', 'B', 12)
                self.text(x=self.MARGIN + 5, y=y, text=bullet)
                y += 9
                if detail:
                    self.set_font('Helvetica', '', 10)
                    self.set_xy(self.MARGIN + 10, y)
                    self.multi_cell(
                        w=self.w - 2 * self.MARGIN - 15,
                        h=6,
                        text=detail,
                    )
                    y = self.get_y() + 8
            else:
                self.set_font('Helvetica', '', 11)
                self.set_xy(self.MARGIN + 5, y)
                self.multi_cell(
                    w=self.w - 2 * self.MARGIN - 5,
                    h=6,
                    text=f'- {line}',
                )
                y = self.get_y() + 6

    def add_title_slide(
        self,
        title: str,
        subtitle: str = '',
        author: str = '',
        date: str = '',
    ) -> None:
        """Add a centered title slide."""
        self.add_page()
        self._header_text = ''
        cx = self.w / 2
        self.set_font('Helvetica', 'B', 28)
        self.set_text_color(0, 51, 102)
        tw = self.get_string_width(title)
        self.text(x=cx - tw / 2, y=self.h / 2 - 40, text=title)
        if subtitle:
            self.set_font('Helvetica', '', 16)
            self.set_text_color(80, 80, 80)
            sw = self.get_string_width(subtitle)
            self.text(x=cx - sw / 2, y=self.h / 2 - 15, text=subtitle)
        info_parts: list[str] = []
        if author:
            info_parts.append(author)
        if date:
            info_parts.append(date)
        if info_parts:
            info = ' | '.join(info_parts)
            self.set_font('Helvetica', '', 11)
            self.set_text_color(120, 120, 120)
            iw = self.get_string_width(info)
            self.text(x=cx - iw / 2, y=self.h / 2 + 10, text=info)

    def build(self, path: str) -> str:
        """Render and save the PDF.

        Args:
            path: Output file path.

        Returns:
            The output file path.
        """
        self.output(path)
        return path
