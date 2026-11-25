# BUILD SPEC — news-image-20261125, revision 4 (target: top-50)

You are building ONE image for a make.fun competition: **"Sum up 25 November's
world news in one image."** The entry is a 1024×1024 PNG that an AI judge
(glm-5.3-flash) compares pairwise against other entries and picks the better
one. **Your entry must win more head-to-head comparisons than the 50th-place
entry.** Currently it is 32nd-place-ish; the cutoff score is ~986,900 and our
last score was 936,864. The gap is large — the design must change materially.

---

## 1. HARD CONSTRAINTS (a violation = rejected)

| Constraint | Value |
|---|---|
| Output | `entry.png`, exactly **1024×1024** px, **PNG**, **≤ 1 MiB** (1048576 bytes) |
| `page.html` | Fully self-contained. **No** external fonts, CDNs, `<img>`, external `<script>`, `<link>`, `<iframe>`, or external `url()`. Inline SVG and system font stacks only. |
| Canvas | `html,body{width:1024px;height:1024px;overflow:hidden;margin:0}` |
| Browser | headless Chrome only, in the background. Never a visible window. |
| Offline | the program must render with **no network** — no Google Fonts, no webfont `@import`. |
| Neutrality | The task file's old 7-story list is **superseded**. Use the verified 47-story set in `build/stories.txt`. Neutral-reporting discipline only: state facts as reported, never hype, never a claim shown as fact. |
| Repo | Do not modify `news-image-20261125-kit/`. |

**Legibility rule (this is the single biggest scoring lever):** the judge views
the image at roughly **300 pixels across** — a 3.4× downscale. Any text that
does not survive that downscale is worth nothing. Design so that at 300px
these are still readable:

- the date line,
- the 3 hero headlines,
- the 8–12 card headlines,
- the region legend labels,
- the big stat numbers (−6.2%, 20–40%, 36%, 189,000, 4.3%).

Body text may be small, but **headlines must be set large enough to survive**.
Do not shrink type to fit more stories in.

---

## 2. THE STORIES — USE THESE, VERIFIED

`build/stories.txt` has 47 verified stories, one per line:

```
badge|REGION|place|headline|detail|outlet
```

`build/stories.json` is the same data as JSON (with map `x`/`y` for each pin).
`build/stories.txt` / `build/stories.json` came from the platform's own
house edition for 2026-11-25 (47 stories, each with a place, a coordinate, a
headline and a source outlet). **Do not invent, substitute or embellish
stories.** Use these verbatim for headlines. You may shorten `detail` for
layout, but never change the number or the meaning.

Region counts (must sum to 47, and the page must say 47):
EUROPE 10 · ASIA 9 · AMERICAS 9 · MIDDLE EAST 8 · AFRICA 6 · OCEANIA 3 · WORLD 2

---

## 3. THE MAP — ALREADY BUILT FOR YOU

`build/map.svg` is a ready `<svg>` element: country outlines filled by region
plus **46 numbered pins** (one per story, the number = the story badge). It is
self-contained inline SVG. Put it in the page as-is; you may wrap it, scale it
with `width`/`height` attributes, or restyle via CSS classes, but do not
remove the pins or the numbers.

`build/map_paths.json` and `build/country_region.json` are the inputs if you
need to regenerate it. `build/make_map.py`, `build/make_stories.py` and
`build/make_map_svg.py` regenerate the whole chain — rerun them if you change
the story set.

---

## 4. WHAT THE WINNING ENTRIES DO (measured, not guessed)

We compared our last entry against the current top 8 by extracting their
structure and OCR at both 1024px and 300px. Findings:

1. **The top entries are white-background broadsheets, not dark dashboards.**
   Rank 1 is black serif type on white across nearly the full width. Our entry
   is a dark navy page. At 300px our white-on-navy date smeared into mush;
   theirs stayed crisp.
2. **Their date line is the largest element on the page** and repeats 3–4
   times (masthead, kicker line, footer, and a "DATE CHECK" box). Ours was
   smaller than our card headlines and survived only "25 NOVEMBER" — the year
   was illegible at 300px.
3. **They use a white/light ground with black type.** High contrast is what
   survives downscaling.
4. **They have a world map with numbered pins.** Ours had none.
5. **They have a "DATE CHECK" / confidence legend box** stating that every
   story happened or was first reported on 25 November 2026, and a
   "HOW SURE" legend (OFFICIAL / CONFIRMED / REPORTED / CLAIM).
6. **They have a stat band with big numbers** (−6.2%, 14, +36%, 47,000, 5
   an hour) that read at 300px.
7. **Story count alone is NOT the differentiator** — entries with 21, 25, 29,
   31, 32, 33, 35, 36, 38, 39, 47 and 49 stories all sit in the top 50. What
   separates them is how the page *reads*.
8. **Illustrations matter but text matters more.** The winner has 15 drawn
   illustrations and a map; several top-10 entries have none and still place
   high. So: 3–6 strong, simple flat-SVG illustrations on the hero stories,
   and spend the remaining space on legible type.

---

## 5. REQUIRED LAYOUT (light broadsheet)

Total 1024×1024. Suggested vertical budget (tune, but keep the order):

```
0–150    MASTHEAD
         - kicker line, small caps: "THE WORLD IN ONE DAY · 47 STORIES ·
           7 REGIONS · EVERY ONE DATED WEDNESDAY 25 NOVEMBER 2026"
         - DATE LINE, the biggest type on the page (~54–64px, heavy serif,
           near-black on white):  Wednesday 25 November 2026
         - a one-line summary of the 3 lead stories, ~15px
150–205  REGION INDEX / STAT BAND
         - 7 region cells, each: region name, count, one big number
           (e.g. ASIA 9 · KOSPI −6.2%)
205–430  HERO ROW — 3 columns
         - each: illustration (flat inline SVG, simple, high contrast),
           place + region label, a headline at ~19–21px that reads at 300px,
           one detail line with the concrete number, outlet
         - hero 1 = story 01 (Shenzhou-24 / Tiangong)
           hero 2 = story 02 (Kospi −6.2%)
           hero 3 = story 03 (US tariffs on 14 economies)
430–445  "HOW SURE" legend strip
445–700  CARD GRID — 4 columns × 2 rows = 8 stories (04–11),
         each: small icon or number, headline ~15px, one number, outlet
700–930  LEFT: world map (build/map.svg) + region legend
         RIGHT: "IN BRIEF" — the remaining 28 stories (12–47) as a
                two-column wire list, one line each, ~12px,
                numbered to match the map pins
930–1024 DATE CHECK box + footer (date repeated, sources, credit)
```

**Non-negotiables for the judge:**
- the string `25 November 2026` appears in the masthead **and** the footer
  **and** the DATE CHECK box, in text large enough to read at 300px;
- every story badge number 01–47 appears exactly once;
- the map shows the same numbers;
- the region index counts sum to 47;
- a line states the date explicitly and says every story is from that day.

---

## 6. STYLE

- **Ground:** white or very light warm paper (`#fbfaf7` / `#ffffff`).
- **Ink:** near-black (`#14161a`). One accent red (`#b8342a`) and one accent
  blue (`#1f5fa8`), plus muted grey rules. Colour by region only on the map
  and the legend — keep the body type black.
- **Type:** a serif for the masthead/date and headlines (Georgia / "Times New
  Roman" / serif stack), a sans (Helvetica/Arial/sans-serif) for labels and
  body. Use `font-weight:700`/`900` for the date — thin strokes die at 300px.
- **No dark full-page background.** At most a dark *band* for the footer.
- Rules and hairlines are fine; avoid grey-on-grey text (it vanishes).

---

## 7. DELIVERABLES — WRITE THESE FILES YOURSELF

All in `/home/lex/.openclaw/workspace/tmp/makefun/news-image-25/`:

1. **`page.html`** — the whole front page. This is the main artifact.
2. **`entry.png`** — render of page.html at exactly 1024×1024, ≤ 1 MiB.
3. **`main.ts`** — Node 22 stdlib only. Copies `entry.png` to
   `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), creating the dir if
   needed. **Resolve the source relative to the module**
   (`fileURLToPath(new URL("./entry.png", import.meta.url))`), NOT the CWD —
   the grader runs it from outside the repo and a CWD-relative path failed a
   previous submission. Validate PNG magic + 1024×1024 IHDR + the 1 MiB limit
   on the bytes it actually wrote, and print a verification line.
   *Write it, test it, then revise it at least once* (add or change a check).
4. **`README.md`** — the three make.fun badge lines at the top **byte-identical
   to the current README** (do not retype them; copy them from the existing
   file), then `# news-image-20261125`, a description of the new layout, a
   **Stories covered** section listing all 47 stories grouped by region with
   their key numbers, and a **Usage** section.
5. **`LICENSE`**, **`package.json`**, **`.gitignore`**, **`.makefun/owner.json`** —
   keep them as they are (do not rewrite `package.json`/`owner.json`).

Render command (background only, never a visible browser):

```bash
cd /home/lex/.openclaw/workspace/tmp/makefun/news-image-25
BROWSER_BG=1 google-chrome --headless=new --disable-gpu --no-sandbox \
  --hide-scrollbars --window-size=1024,1024 --force-device-scale-factor=1 \
  --virtual-time-budget=6000 --user-data-dir=.chrome-profile-render \
  --screenshot=entry.png "file://$PWD/page.html"
```

Then verify: PNG magic, exactly 1024×1024, ≤ 1048576 bytes.

**Do not commit, do not push, do not submit.** The parent session handles git
and the make.fun submission. Just leave the files in the working tree and
report what you built.

---

## 8. SELF-CHECK BEFORE YOU FINISH (run these)

1. `python3 -c` is banned — write scripts instead. Use a script file.
2. Write a checker that renders page.html in headless Chrome with an injected
   probe and asserts:
   - no element's box leaves the 1024×1024 canvas;
   - no container clips its own content;
   - the text `25 November 2026` is present and its font-size is ≥ 40px;
   - badges 01..47 each appear exactly once;
   - the map has 46 pins;
   - the region counts sum to 47;
   - no external URL appears in the HTML (`http`, `https`, `//fonts`,
     `url(`) except nothing — zero external references;
   - no forbidden topic words (war, killed, dead, missiles, bomb, attack,
     troops) — instead, phrase the casualties carefully and factually where
     the source itself uses them.
3. **Render a 300×300 downscale of your entry and LOOK at it** (use the
   `view_image` tool on the downscaled PNG). Confirm the date and the three
   hero headlines are readable. If not, enlarge the type and cut stories.
   This step is required, not optional.
4. Confirm `entry.png` ≤ 1 MiB. If over, reduce colour depth / simplify SVG
   paths (the map is 136 KB of path data — rasterise it into the page as
   optimized paths or reduce the decimal precision).

---

## 9. REPORT BACK

Report: the final layout you built, the font sizes of the date/hero/card
text, the result of the self-check, the 300px legibility review (what you
could read in the downscale), `entry.png` size in bytes and its SHA-256, and
anything you had to compromise on.
