# Contributing to ai-magazine-layout-generator

Thanks for wanting to help lay out magazines with AI. This is a Windows-first
desktop toolkit, but the layout engine is OS-agnostic Python.

## Development setup

1. Install Python 3.11+ (3.12 recommended for 2026 builds).
2. Create a venv:
   ```
   py -3.12 -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dev deps:
   ```
   pip install -e ".[dev]"
   ```
4. Run the test suite:
   ```
   pytest -q
   ```
5. Run the CLI smoke test:
   ```
   python -m magazine_layout.cli --issue samples/issue_042.json --out build/proof.pdf
   ```

## Project layout

- `magazine_layout/` — the core package. Everything importable lives here.
- `magazine_layout/handlers/` — per-command entry points (spread, grid, spread preview).
- `magazine_layout/services/` — long-running services: render service, font service, LLM layout advisor.
- `magazine_layout/models/` — dataclasses for Issue, Spread, Grid, Placement, Typography.
- `magazine_layout/utils/` — geometry, color, pagination math, IO helpers.
- `magazine_layout/config/` — defaults, presets, and schema validation.
- `tests/` — pytest suite. New features need a test.

## Coding standards

- Type hints required on public functions.
- `ruff` for lint, `mypy --strict` for types.
- No print debugging in merged code; use `magazine_layout.utils.logging`.
- Keep modules under ~400 lines. Split by responsibility, not by line count.

## Adding a new layout preset

1. Drop a JSON file in `magazine_layout/config/presets/`.
2. Register it in `magazine_layout/config/preset_registry.py`.
3. Add a golden test in `tests/test_presets.py` that asserts grid math
   matches the expected column/row counts for a known page size.

## Commit style

Conventional commits: `feat(grid): add asymmetric three-column bleed`,
`fix(render): correct gutter rounding on 300dpi exports`, etc.

## Reporting issues

Use the GitHub issue templates. Include: Windows version, Python version,
the issue JSON (redacted), and the exact command that failed.