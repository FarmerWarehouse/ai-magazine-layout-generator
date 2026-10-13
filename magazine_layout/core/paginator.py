"""Paginator — turns an Issue into an ordered list of Pages.

Rules:
    - Cover page is always page 1, single-sided.
    - Body flows left/right spreads starting from page 2.
    - Ad slots are pinned to odd pages unless preset overrides.
"""
from __future__ import annotations

from dataclasses import dataclass

from magazine_layout.config.schema import Preset
from magazine_layout.models.issue import Issue
from magazine_layout.models.page import Page


@dataclass(slots=True)
class Paginator:
    preset: Preset

    def paginate(self, issue: Issue) -> list[Page]:
        pages: list[Page] = [Page(number=1, kind="cover", items=tuple(issue.cover_items()))]
        number = 2
        for section in issue.sections:
            for item in section.items:
                pages.append(Page(number=number, kind=section.kind, items=(item,)))
                number += 1
        while number <= self.preset.min_pages:
            pages.append(Page(number=number, kind="filler", items=()))
            number += 1
        return pages