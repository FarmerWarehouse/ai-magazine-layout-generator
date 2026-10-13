"""Grid solver — picks column/row counts and gutters for a page.

Heuristic:
    - Feature pages: 3 columns, 1:1.618 gutters, generous margins.
    - Ad pages:      full-bleed, single slot.
    - Filler:        2 columns, default margins.
"""
from __future__ import annotations

from magazine_layout.config.schema import Preset
from magazine_layout.models.grid import Grid
from magazine_layout.models.page import Page


def solve_grid(page: Page, preset: Preset, side: str) -> Grid:
    if page.kind == "cover":
        return Grid(columns=1, rows=1, gutter_mm=0.0, margin_mm=preset.margin_mm, slots=1)
    if page.kind == "ad":
        return Grid(columns=1, rows=1, gutter_mm=0.0, margin_mm=0.0, slots=1)
    if page.kind == "filler":
        return Grid(columns=2, rows=3, gutter_mm=preset.gutter_mm, margin_mm=preset.margin_mm, slots=6)
    cols = preset.feature_columns
    rows = preset.feature_rows
    outer = preset.margin_mm
    inner = preset.margin_mm * 1.5 if side in ("left", "right") else preset.margin_mm
    return Grid(
        columns=cols,
        rows=rows,
        gutter_mm=preset.gutter_mm,
        margin_mm=outer,
        inner_margin_mm=inner,
        slots=cols * rows,
    )