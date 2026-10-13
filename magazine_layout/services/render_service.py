"""RenderService — rasterizes a LayoutPlan to a print-ready PDF.

Backend: reportlab. Coordinates are in points (1/72 inch).
DPI only affects rasterized previews, not vector PDF output.
"""
from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from magazine_layout.core.layout_engine import LayoutPlan
from magazine_layout.services.font_service import FontService
from magazine_layout.utils.geometry import inches_to_points
from magazine_layout.utils.logging import get_logger

log = get_logger(__name__)


class RenderService:
    def __init__(self, dpi: int, trim: str) -> None:
        self._dpi = dpi
        self._trim = trim
        self._fonts = FontService()

    def render(self, plan: LayoutPlan, out_path: Path) -> None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        width, height = self._parse_trim(plan.trim)
        c = canvas.Canvas(str(out_path), pagesize=(width, height))
        for spread in plan.spreads:
            self._draw_page(c, spread.left, width, height)
            c.showPage()
            if spread.right is not None:
                self._draw_page(c, spread.right, width, height)
                c.showPage()
        c.save()
        log.debug("rendered %d spreads at %ddpi", len(plan.spreads), self._dpi)

    def _draw_page(self, c: canvas.Canvas, page, width: float, height: float) -> None:
        c.setFont(self._fonts.body_font(), 10)
        c.drawString(inches_to_points(0.75), height - inches_to_points(0.75), f"page {page.number} — {page.kind}")

    def _parse_trim(self, trim: str) -> tuple[float, float]:
        w, h = trim.lower().split("x")
        return inches_to_points(float(w)), inches_to_points(float(h))
</｜｜DSML｜｜ parameter>