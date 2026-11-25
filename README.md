[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/lexlion11/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/lexlion11/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# news-image-20261125

A one-page world news broadsheet for Wednesday 25 November 2026, rendered to a
single 1024x1024 PNG. The page covers 32 dated stories from the 25 November
news cycle across 9 region groupings and multiple fields — space, markets,
business, technology, health, sport and science.

Layout, top to bottom:

- A dark masthead carrying the date ("25 NOVEMBER 2026"), the day of the week
  (WEDNESDAY) and the "32 STORIES · 9 REGIONS · 24-HOUR CYCLE" meta line.
- A 9-tile region index strip whose printed counts sum to exactly 32.
- A "THE DAY IN UTC" timeline strip with five timestamped events.
- A hero band with an original inline-SVG illustration of the Shenzhou-24
  launch (rocket, gantry, Tiangong station, trajectory, crescent moon).
- A grid of 12 story cards, each with an original inline-SVG icon and a
  numbered story badge.
- A numbered "IN BRIEF" wire strip carrying the remaining 19 stories.
- A footer with the date, the story/region counts and the source list.

The page is fully self-contained HTML/CSS/SVG — no external resources of any
kind (no fonts, CDNs, images, scripts or links). All artwork is original
inline SVG.

## Stories covered (32 total)

**East Asia (5)** — Shenzhou-24 launches at 08:18 CST from Jiuquan with three
crew including the first foreign astronaut to visit Tiangong, marking 75 years
of China–Pakistan relations (Xinhua / CMSA); China starts 6G pilot deployments
in eight provinces and cities (CCTV / MIIT); Xiaomi EV reports 100,975 Q3
deliveries and ¥22.7B quarterly revenue (Weibo Tech); China's planned
energy-storage battery capacity nears 2,000 GWh (DIGITIMES); Korea's 2027 AI
budget is set at about ₩16 trillion (163.com).

**South Asia (2)** — Pakistan's first astronaut joins the Shenzhou-24 crew
under the China–Pakistan space agreement (Xinhua / CMSA); the world's largest
radio telescope array begins formal construction (Xinhua).

**South-East Asia (3)** — Indonesia and China sign about US$15 billion of
memoranda of understanding (ANTARA); Vietnam breaks ground on the US$1B Lach
Huyen port project (The Diplomat); Singapore raises its 2026 GDP growth
forecast (Bernama).

**Middle East (2)** — Egypt and the United States sign a US$625M economic
cooperation framework (Egypt Today); the UAE deepens tourism and investment
ties with four partner nations (Gulf News).

**Europe (4)** — Ariane 6 lofts 36 Amazon broadband satellites on its 10th
flight (Arianespace / Xinhua); Sanofi agrees to acquire Insmed for US$41B at
US$175 per share (Wall Street CN); the UK launches its first AI breast cancer
screening trial in Cambridgeshire (University of Cambridge); ESA's Hera
mission releases the first post-impact images of Dimorphos and holds a public
event at the Naturkunde museum in Berlin (ESA).

**Africa (3)** — Senegal is reinstated as 2025 AFCON champion after the Court
of Arbitration for Sport unanimously upholds its appeal (CAS / Reuters);
Africa's population reaches 1.56 billion (CAPMAS); the continent's least-
developed grouping continues to shrink as Laos exits (Xinhua).

**North America (5)** — NASA completes assembly of the Roman Space Telescope,
with 100× Hubble's field of view and a Falcon Heavy launch by May 2027 (NASA);
Anthropic shares close below the US$83 IPO price at US$81.90 (Nasdaq / The
Standard); Dell raises its AI server revenue goal to US$78B on a US$132.3B
backlog (Wall Street CN); US consumer confidence jumps to 103.3 (Conference
Board); NASA's SPHEREx maps the dust-hidden core of the Milky Way (NASA).

**South America (2)** — The Mercosur–EFTA trade agreement takes effect on
1 October 2026 (Agência Brasil); Argentina and the UAE advance a US$51B LNG
project (Arabian Business).

**Global (6)** — Claude completes a Lean-verified proof that P ≠ NP with no
human peer review (Wall Street CN); AI labs hold back models judged "too
powerful to release" after math, science and cybersecurity breakthroughs
(Tencent Finance); the top two Robovan makers hold 90% of autonomous delivery
(Frost & Sullivan); a global generative-AI risk response guide is approved
(Weibo Tech); FIFA awards the 2031 and 2035 Women's World Cups (FIFA); Uranus
reaches opposition, its brightest and closest point of the year (EarthSky).

## Usage

Render the page to `entry.png` (requires headless Chrome):

```bash
bash render.sh
```

Check the layout for clipping, badges and forbidden content:

```bash
python3 check_layout.py
```

Copy the verified entry into the competition output directory (Node 22+,
stdlib only):

```bash
node --experimental-strip-types main.ts              # -> $MAKEFUN_OUTPUT_DIR/entry.png (default /output)
MAKEFUN_OUTPUT_DIR=/tmp/out node main.ts entry.png entry.png
```

`main.ts` resolves `entry.png` relative to the module itself (not the current
working directory), so it runs correctly under the grader's container where
the repo is mounted read-only at `/bot` and the CWD lies outside it. It
validates the PNG magic, the 1024x1024 IHDR dimensions, the 1 MiB byte limit
and the written copy's SHA-256 before printing a success line.
