"""Command-line entry point for the AI magazine layout generator.

Usage:
    python -m magazine_layout --issue samples/issue_042.json --out build/proof.pdf
    python -m magazine_layout --issue samples/issue_042.json --preview-spreads
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from magazine_layout.config.defaults import DEFAULT_DPI, DEFAULT_TRIM_SIZE
from magazine_layout.core.layout_engine import LayoutEngine
from magazine_layout.handlers.spread_handler import handle_preview_spreads
from magazine_layout.services.render_service import RenderService
from magazine_layout.utils.io import load_issue_json
from magazine_layout.utils.logging import get_logger

log = get_logger(__name__)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="magazine-layout",
        description="AI magazine layout generator — paginate, grid, and export.",
    )
    p.add_argument("--issue", type=Path, required=True, help="Path to issue JSON.")
    p.add_argument("--out", type=Path, default=Path("build/proof.pdf"), help="Output PDF path.")
    p.add_argument("--dpi", type=int, default=DEFAULT_DPI, help="Export DPI (default 300).")
    p.add_argument(
        "--trim",
        default=DEFAULT_TRIM_SIZE,
        help="Trim size WxH in inches, e.g. 8.5x11.",
    )
    p.add_argument("--preview-spreads", action="store_true", help="Print spread plan and exit.")
    p.add_argument("--preset", default="editorial_classic", help="Layout preset name.")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    issue = load_issue_json(args.issue)
    engine = LayoutEngine(preset=args.preset, trim=args.trim, dpi=args.dpi)
    plan = engine.plan(issue)

    if args.preview_spreads:
        handle_preview_spreads(plan)
        return 0

    renderer = RenderService(dpi=args.dpi, trim=args.trim)
    renderer.render(plan, out_path=args.out)
    log.info("wrote %s (%d spreads)", args.out, len(plan.spreads))
    return 0


if __name__ == "__main__":
    sys.exit(main())