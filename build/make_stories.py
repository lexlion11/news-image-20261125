#!/usr/bin/env python3
"""Turn the verified 25 November 2026 story set into page-ready data.

Input : news2511_spec.json  (the platform's own house edition for 2026-11-25:
         47 stories with region, place, geo coordinates, headline, hook,
         supporting points and outlet names)
Output: stories.json        (what the page template renders)

Design rules baked in here:
  * every story keeps a numeric badge 01..N so the map pins can carry the
    same number;
  * region ids are normalised to the seven the platform's own edition uses;
  * the geo coordinates become x/y inside the map box, using the same
    projection as make_map.py, so pins land on the right country.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "news2511_spec.json")
OUT = os.path.join(HERE, "stories.json")

# Same projection constants as make_map.py.
MAP_W = 470.0
MAP_H = 300.0
LON0, LON1 = -170.0, 190.0
LAT0, LAT1 = 84.0, -58.0

REGION_LABEL = {
    "asia": "ASIA",
    "middle-east": "MIDDLE EAST",
    "europe": "EUROPE",
    "africa": "AFRICA",
    "americas": "AMERICAS",
    "oceania": "OCEANIA",
    "world": "WORLD",
}


def project(lon: float, lat: float) -> tuple[float, float]:
    x = (lon - LON0) / (LON1 - LON0) * MAP_W
    y = (LAT1 - lat) / (LAT1 - LAT0) * MAP_H
    return round(x, 1), round(y, 1)


# Region colour and short code, used for the map legend and region index.
REGION_STYLE = {
    "ASIA": ("#b8342a", "AS"),
    "MIDDLE EAST": ("#c26a18", "ME"),
    "EUROPE": ("#1f5fa8", "EU"),
    "AFRICA": ("#1d7a4d", "AF"),
    "AMERICAS": ("#5a3ea8", "AM"),
    "OCEANIA": ("#0f7f8c", "OC"),
    "WORLD": ("#3b3b46", "GL"),
}

# A few stories in the house edition carry no coordinate. Their places are
# named, so the pin is placed by hand (lat, lon) instead of being dropped.
MANUAL_GEO = {
    "AI doubts return: Kospi plunges 6.2%": (37.5665, 126.9780),   # Seoul
    "Ukraine: hit 3 MiG-31s, 2 Su-34s": (54.8833, 42.0167),        # Savasleyka air base
    "47,000 women killed by partners or relatives in 2025; five an hour": (40.7484, -73.9857),  # UN HQ, New York
}


def clean(text: str | None) -> str:
    if not text:
        return ""
    out = " ".join(text.split())
    return out.rstrip(".")


def main() -> None:
    spec = json.load(open(SPEC, encoding="utf-8"))
    rows = []
    for story in spec["stories"]:
        n = story["n"]
        region = REGION_LABEL.get(story["region"] or "", "WORLD")
        headline = clean(story["headline"])
        hook = clean(story.get("hook"))
        # The house hook repeats the headline; prefer the supporting points
        # when the hook says nothing new.
        detail = ""
        for point in story.get("points") or []:
            detail = clean(point)
            break
        place = story.get("place") or ""
        x = y = None
        geo = story.get("geo")
        if geo:
            # geo is {"lat": <latitude>, "lon": <longitude>}
            x, y = project(float(geo["lon"]), float(geo["lat"]))
        elif headline in MANUAL_GEO:
            lat, lon = MANUAL_GEO[headline]
            x, y = project(lon, lat)
        rows.append({
            "n": n,
            "badge": f"{n:02d}",
            "headline": headline,
            "detail": detail or hook,
            "place": place,
            "region": region,
            "region_code": REGION_STYLE[region][1],
            "tier": story.get("tier"),
            "x": x,
            "y": y,
            "source": (story.get("sources") or [""])[0],
        })

    # Renumber 1..N contiguously, keeping the platform's own order (leads first).
    for i, row in enumerate(rows, start=1):
        row["n"] = i
        row["badge"] = f"{i:02d}"

    counts: dict[str, int] = {}
    for row in rows:
        counts[row["region"]] = counts.get(row["region"], 0) + 1

    json.dump({
        "day": "2026-11-25",
        "date_long": "Wednesday 25 November 2026",
        "total": len(rows),
        "region_counts": counts,
        "stories": rows,
    }, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"stories.json: {len(rows)} stories")
    for region, count in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {region:14} {count}")
    missing = [r["badge"] for r in rows if r["x"] is None]
    print(f"stories without a map coordinate: {missing}")


if __name__ == "__main__":
    main()
