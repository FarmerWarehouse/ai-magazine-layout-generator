"""LayoutEngine — orchestrates pagination, grid solving, and placement.

Inputs:
    preset: str    name of a layout preset in config/presets/
    trim:   str    "WxH" inches, e.g. "8.5x11"
    dpi:    int    export resolution (only used by downstream render)

Outputs:
    LayoutPlan     immutable plan with spreads, grids, and placements

Side effects: none. Pure planning. Rendering is a separate service.
Complexity: O(P * G) where P = pages, G = placements per page.
"""
from __future__ import annotations

from dataclasses import dataclass

from magazine_layout.config.preset_registry import load_preset
from magazine_layout.core.grid_solver import solve_grid
from magazine_layout.core.paginator import Paginator
from magazine_layout.models.grid import Grid
from magazine_layout.models.issue import Issue
from magazine_layout.models.placement import Placement
from magazine_layout.models.spread import Spread


@dataclass(frozen=True, slots=True)
class LayoutPlan:
    spreads: tuple[Spread, ...]
    trim: str
    dpi: int
    preset: str


class LayoutEngine:
    def __init__(self, preset: str, trim: str, dpi: int) -> None:
        self._preset = load_preset(preset)
        self._trim = trim
        self._dpi = dpi
        self._paginator = Paginator(self._preset)

    def plan(self, issue: Issue) -> LayoutPlan:
        pages = self._paginator.paginate(issue)
        spreads: list[Spread] = []
        for i in range(0, len(pages), 2):
            left = pages[i]
            right = pages[i + 1] if i + 1 < len(pages) else None
            grid: Grid = solve_grid(left, self._preset, side="left")
            placements: tuple[Placement, ...] = tuple(
                Placement(slot=slot, content=item)
                for slot, item in zip(grid.slots, left.items, strict=False)
            )
            spreads.append(Spread(left=left, right=right, grid=grid, placements=placements))
        return LayoutPlan(spreads=tuple(spreads), trim=self._trim, dpi=self._dpi, preset=self._preset.name)