#!/usr/bin/env python3
"""Build the world-map SVG path data for the 25 November 2026 news digest.

Reads Natural Earth 110m country polygons (already downloaded) and the verified
story set, then emits:
  * map_paths.json  - country outline paths projected to the map box
  * story_data.json - the story set, normalised for the page template

Projection: equirectangular with a latitude cutoff, standard for a flat
newspaper map. Nothing here touches the network; the geojson is a local file.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GEOJSON = os.path.join(HERE, "world_raw.geojson")
SPEC = os.path.join(HERE, "news2511_spec.json")

# Map box inside the 1024x1024 canvas (left column of the lower band).
MAP_W = 470.0
MAP_H = 300.0
LON0, LON1 = -170.0, 190.0   # wrap a little past the antimeridian for Chukotka
LAT0, LAT1 = 84.0, -58.0     # south edge keeps Antarctica out


def project(lon: float, lat: float) -> tuple[float, float]:
    x = (lon - LON0) / (LON1 - LON0) * MAP_W
    y = (LAT1 - lat) / (LAT1 - LAT0) * MAP_H
    return x, y


def ring_to_path(ring: list[list[float]]) -> str:
    pts = [project(float(c[0]), float(c[1])) for c in ring]
    # Drop consecutive duplicates so the path data stays compact.
    out: list[tuple[float, float]] = []
    for p in pts:
        if not out or (abs(p[0] - out[-1][0]) > 0.01 or abs(p[1] - out[-1][1]) > 0.01):
            out.append(p)
    if len(out) < 3:
        return ""
    head = f"M{out[0][0]:.1f},{out[0][1]:.1f}"
    rest = "".join(f"L{p[0]:.1f},{p[1]:.1f}" for p in out[1:])
    return head + rest + "Z"


def build_paths() -> list[dict]:
    gj = json.load(open(GEOJSON, encoding="utf-8"))
    shapes = []
    for feat in gj["features"]:
        props = feat.get("properties") or {}
        name = props.get("NAME") or props.get("ADMIN") or ""
        if name == "Antarctica":
            continue
        geom = feat.get("geometry") or {}
        gtype = geom.get("type")
        coords = geom.get("coordinates") or []
        polys = []
        if gtype == "Polygon":
            polys = [coords]
        elif gtype == "MultiPolygon":
            polys = coords
        paths = []
        for poly in polys:
            if not poly:
                continue
            outer = ring_to_path(poly[0])
            if outer:
                paths.append(outer)
            for hole in poly[1:]:
                inner = ring_to_path(hole)
                if inner:
                    paths.append(inner)
        if paths:
            shapes.append({"name": name, "d": "".join(paths)})
    return shapes


REGION_OF_COUNTRY = {
    "China": "ASIA", "India": "ASIA", "Pakistan": "ASIA", "Japan": "ASIA",
    "South Korea": "ASIA", "North Korea": "ASIA", "Bangladesh": "ASIA",
    "Indonesia": "ASIA", "Malaysia": "ASIA", "Thailand": "ASIA",
    "Vietnam": "ASIA", "Philippines": "ASIA", "Singapore": "ASIA",
    "Myanmar": "ASIA", "Cambodia": "ASIA", "Laos": "ASIA", "Nepal": "ASIA",
    "Sri Lanka": "ASIA", "Mongolia": "ASIA", "Kazakhstan": "ASIA",
    "Turkey": "MIDDLE EAST", "Iran": "MIDDLE EAST", "Iraq": "MIDDLE EAST",
    "Syria": "MIDDLE EAST", "Lebanon": "MIDDLE EAST", "Israel": "MIDDLE EAST",
    "Saudi Arabia": "MIDDLE EAST", "Yemen": "MIDDLE EAST", "Oman": "MIDDLE EAST",
    "United Arab Emirates": "MIDDLE EAST", "Qatar": "MIDDLE EAST",
    "Kuwait": "MIDDLE EAST", "Jordan": "MIDDLE EAST", "Bahrain": "MIDDLE EAST",
    "Russia": "EUROPE", "Ukraine": "EUROPE", "Poland": "EUROPE",
    "Germany": "EUROPE", "France": "EUROPE", "United Kingdom": "EUROPE",
    "Italy": "EUROPE", "Spain": "EUROPE", "Greece": "EUROPE",
    "Romania": "EUROPE", "Hungary": "EUROPE", "Czechia": "EUROPE",
    "Austria": "EUROPE", "Switzerland": "EUROPE", "Netherlands": "EUROPE",
    "Belgium": "EUROPE", "Sweden": "EUROPE", "Norway": "EUROPE",
    "Finland": "EUROPE", "Denmark": "EUROPE", "Ireland": "EUROPE",
    "Portugal": "EUROPE", "Bulgaria": "EUROPE", "Serbia": "EUROPE",
    "Croatia": "EUROPE", "Albania": "EUROPE", "Belarus": "EUROPE",
    "Lithuania": "EUROPE", "Latvia": "EUROPE", "Estonia": "EUROPE",
    "Slovakia": "EUROPE", "Slovenia": "EUROPE", "Bosnia and Herz.:": "EUROPE",
    "Egypt": "AFRICA", "Sudan": "AFRICA", "South Sudan": "AFRICA",
    "Ethiopia": "AFRICA", "Nigeria": "AFRICA", "Kenya": "AFRICA",
    "South Africa": "AFRICA", "Morocco": "AFRICA", "Algeria": "AFRICA",
    "Tunisia": "AFRICA", "Libya": "AFRICA", "Somalia": "AFRICA",
    "Tanzania": "AFRICA", "Uganda": "AFRICA", "Ghana": "AFRICA",
    "Senegal": "AFRICA", "Cameroon": "AFRICA", "Angola": "AFRICA",
    "Zambia": "AFRICA", "Zimbabwe": "AFRICA", "Mozambique": "AFRICA",
    "Namibia": "AFRICA", "Botswana": "AFRICA", "Cote d'Ivoire": "AFRICA",
    "Mali": "AFRICA", "Niger": "AFRICA", "Chad": "AFRICA", "Rwanda": "AFRICA",
    "United States of America": "AMERICAS", "Canada": "AMERICAS",
    "Mexico": "AMERICAS", "Brazil": "AMERICAS", "Argentina": "AMERICAS",
    "Colombia": "AMERICAS", "Chile": "AMERICAS", "Peru": "AMERICAS",
    "Venezuela": "AMERICAS", "Ecuador": "AMERICAS", "Bolivia": "AMERICAS",
    "Paraguay": "AMERICAS", "Uruguay": "AMERICAS", "Cuba": "AMERICAS",
    "Guatemala": "AMERICAS", "Honduras": "AMERICAS", "Panama": "AMERICAS",
    "Costa Rica": "AMERICAS", "Jamaica": "AMERICAS", "Haiti": "AMERICAS",
    "Australia": "OCEANIA", "New Zealand": "OCEANIA",
    "Papua New Guinea": "OCEANIA", "Fiji": "OCEANIA",
}


def main() -> None:
    shapes = build_paths()
    json.dump({"map_w": MAP_W, "map_h": MAP_H, "shapes": shapes},
              open(os.path.join(HERE, "map_paths.json"), "w"), indent=1)
    print(f"map_paths.json: {len(shapes)} country outlines, box {MAP_W}x{MAP_H}")
    named = sum(1 for s in shapes if s["name"] in REGION_OF_COUNTRY)
    print(f"countries with a region colour: {named}/{len(shapes)}")


if __name__ == "__main__":
    main()
