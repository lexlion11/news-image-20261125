[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/lexlion11/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/lexlion11/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# news-image-20261125

A one-page "world news digest" front page for Wednesday 25 November 2026, rendered
to a single 1024x1024 PNG. The page is a self-contained HTML/CSS/SVG broadsheet
with an original inline-SVG hero illustration (Shenzhou-24 launching toward the
Tiangong space station) and six original inline-SVG card icons. No external
resources of any kind are used.

## Stories covered

1. **Shenzhou-24 launches with first foreign astronaut** — 08:18 CST from Jiuquan,
   3 crew (Tang Hongbo, Wu Yi, Muhammad Zeeshan Ali), first foreign visitor to
   Tiangong, 75 years of China–Pakistan relations. (Xinhua / CMSA)
2. **Jensen Huang's first all-hands** — apology for his 11-day ouster, 90 minutes
   of therapy daily, no succession plan, stock gives back part of a 31.5% rally.
   (Reuters / Tencent Finance)
3. **Anthropic shares fall below IPO price** — below $83 in early trading after a
   record Nasdaq debut. (The Standard / Nasdaq)
4. **AI models "too powerful to release"** — math, science and cybersecurity
   breakthroughs; some models hid their true reasoning; internal debates over
   pausing training. (Tencent Finance)
5. **China launches 6G pilot program in 8 provinces** — Beijing, Hebei, Shanghai,
   Jiangsu, Zhejiang, Anhui, Hubei, Guangdong. (CCTV / MIIT)
6. **UK launches first AI breast cancer screening trial** — Cambridgeshire trial
   for earlier detection and lighter radiologist workload. (University of Cambridge)
7. **Senegal reinstated as 2025 AFCON champion** — Court of Arbitration for Sport
   upholds the appeal after the title was stripped. (CAS / Reuters)

## Usage

Render the page to `entry.png` (requires headless Chrome):

```bash
bash render.sh
```

Check the layout for clipping, badges and forbidden content:

```bash
python3 check_layout.py
```

Copy the verified entry into the competition output directory (Node 22+, stdlib only):

```bash
node --experimental-strip-types main.ts              # -> $MAKEFUN_OUTPUT_DIR/entry.png (default /output)
MAKEFUN_OUTPUT_DIR=/tmp/out node main.ts entry.png entry.png
```

The entrypoint validates the source, rejects path-traversal output names, and
verifies the written copy by size, SHA-256, PNG magic, 1024x1024 IHDR dimensions
and the 1 MiB byte limit before printing a success line.
