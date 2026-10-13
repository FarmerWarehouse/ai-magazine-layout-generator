"""Spread preview handler — prints a human-readable plan of spreads."""
from __future__ import annotations

from rich.console import Console
from rich.table import Table

from magazine_layout.core.layout_engine import LayoutPlan


def handle_preview_spreads(plan: LayoutPlan) -> None:
    console = Console()
    table = Table(title=f"Spread plan — preset={plan.preset} trim={plan.trim}")
    table.add_column("Spread", justify="right")
    table.add_column("Left page", justify="left")
    table.add_column("Right page", justify="left")
    table.add_column("Grid", justify="left")
    for idx, spread in enumerate(plan.spreads, start=1):
        left = f"#{spread.left.number} ({spread.left.kind})"
        right = f"#{spread.right.number} ({spread.right.kind})" if spread.right else "—"
        grid = f"{spread.grid.columns}x{spread.grid.rows} g={spread.grid.gutter_mm}mm"
        table.add_row(str(idx), left, right, grid)
    console.print(table)