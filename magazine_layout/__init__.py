"""ai-magazine-layout-generator — AI-driven magazine layout toolkit.

Public surface:
    Issue, Spread, Grid, Placement  — core models
    LayoutEngine                    — orchestrates pagination + placement
    RenderService                   — rasterizes spreads to PDF/PNG
"""

from magazine_layout.core.layout_engine import LayoutEngine
from magazine_layout.models.grid import Grid
from magazine_layout.models.issue import Issue
from magazine_layout.models.placement import Placement
from magazine_layout.models.spread import Spread

__all__ = ["Issue", "Spread", "Grid", "Placement", "LayoutEngine"]
__version__ = "0.4.2"