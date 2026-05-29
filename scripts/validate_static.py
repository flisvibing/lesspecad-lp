#!/usr/bin/env python3
"""Basic static checks for the Lesspecad landing page."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path


class LandingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self._in_title = False
        self.ids: set[str] = set()
        self.anchors: list[str] = []
        self.images_without_alt = 0
        self.meta_description = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if tag == "title":
            self._in_title = True
        if "id" in attr_map and attr_map["id"]:
            self.ids.add(attr_map["id"] or "")
        if tag == "a" and (href := attr_map.get("href")):
            self.anchors.append(href)
        if tag == "img" and not attr_map.get("alt"):
            self.images_without_alt += 1
        if tag == "meta" and attr_map.get("name") == "description" and attr_map.get("content"):
            self.meta_description = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data.strip()


def main() -> None:
    html_path = Path("index.html")
    css_path = Path("styles.css")
    assert html_path.exists(), "index.html is missing"
    assert css_path.exists(), "styles.css is missing"

    parser = LandingParser()
    parser.feed(html_path.read_text(encoding="utf-8"))

    assert "Lesspecad" in parser.title, "document title must mention Lesspecad"
    assert parser.meta_description, "meta description is required"
    assert parser.images_without_alt == 0, "all images need alt text"

    missing_targets = [href for href in parser.anchors if href.startswith("#") and href[1:] not in parser.ids]
    assert not missing_targets, f"missing anchor targets: {missing_targets}"

    css = css_path.read_text(encoding="utf-8")
    required_tokens = ["--primary", "--accent", "prefers-reduced-motion", "@media (max-width: 640px)"]
    missing_tokens = [token for token in required_tokens if token not in css]
    assert not missing_tokens, f"missing CSS safeguards: {missing_tokens}"

    print("Static landing page checks passed.")


if __name__ == "__main__":
    main()
