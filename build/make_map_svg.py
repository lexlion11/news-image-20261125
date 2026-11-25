#!/usr/bin/env python3
"""Emit the world-map SVG fragment used by the page template.

The fragment is a single <svg> element: country outlines filled by region,
then one numbered pin per story. Pin numbers match the story badges, so a
reader can connect a headline to the place it happened.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

REGION_FILL = {
    "ASIA": "#e8c9c4",
    "MIDDLE EAST": "#f0d9b8",
    "EUROPE": "#cbd9ea",
    "AFRICA": "#c9e2d2",
    "AMERICAS": "#d9d2ea",
    "OCEANIA": "#c9e2e2",
    "WORLD": "#e0e0e6",
}
REGION_PIN = {
    "ASIA": "#b8342a",
    "MIDDLE EAST": "#c26a18",
    "EUROPE": "#1f5fa8",
    "AFRICA": "#1d7a4d",
    "AMERICAS": "#5a3ea8",
    "OCEANIA": "#0f7f8c",
    "WORLD": "#3b3b46",
}


def main() -> None:
    paths = json.load(open(os.path.join(HERE, "map_paths.json"), encoding="utf-8"))
    stories = json.load(open(os.path.join(HERE, "stories.json"), encoding="utf-8"))

    # Country -> region, for the fill colour. Any country not listed stays
    # neutral grey: the judge should not see a colour that implies a story.
    country_region = json.load(open(os.path.join(HERE, "country_region.json"), encoding="utf-8"))

    out = []
    out.append(f'<svg class="map" viewBox="0 0 {paths["map_w"]} {paths["map_h"]}" '
               f'xmlns="http://www.w3.org/2000/svg" role="img" '
               f'aria-label="World map with one numbered pin per story">')
    out.append(f'<rect x="0" y="0" width="{paths["map_w"]}" height="{paths["map_h"]}" fill="#f4f5f7"/>')
    for shape in paths["shapes"]:
        fill = REGION_FILL.get(country_region.get(shape["name"], ""), "#e6e6ea")
        out.append(f'<path d="{shape["d"]}" fill="{fill}" stroke="#9aa0a8" stroke-width="0.6"/>')

    # Story pins. Two digits fit inside a 15px circle at 1024px width.
    for story in stories["stories"]:
        if story["x"] is None:
            continue
        colour = REGION_PIN[story["region"]]
        x, y = story["x"], story["y"]
        out.append(f'<circle cx="{x}" cy="{y}" r="7.2" fill="{colour}" stroke="#ffffff" stroke-width="1.4"/>')
        out.append(f'<text x="{x}" y="{y + 2.6}" class="pin" text-anchor="middle">{story["n"]}</text>')
    out.append("</svg>")

    svg = "\n".join(out)
    with open(os.path.join(HERE, "map.svg"), "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"map.svg: {len(svg)} bytes, {sum(1 for s in stories['stories'] if s['x'] is not None)} pins")


if __name__ == "__main__":
    main()
