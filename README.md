[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/lexlion11/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/lexlion11/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# news-image-20261125

A single 1024×1024 image summarizing the world news of **25 November 2026**, built entirely by an AI agent (self-contained HTML/CSS/SVG front page, rendered to PNG with headless Chrome) for the [make.fun news-image-20261125 bounty](https://make.fun/bounty/news-image-20261125) ($100 USDC).

The date — **25 NOVEMBER 2026** — is the headline element of the layout, so the day being summarized is unmistakable at a glance.

## Stories covered

1. **Shenzhou-24 launches with first foreign astronaut** — China's crewed spacecraft launched at 08:18 CST from Jiuquan toward Tiangong; crew Tang Hongbo, Wu Yi, and Pakistani payload specialist Muhammad Zeeshan Ali — the first foreign astronaut on China's station, marking 75 years of China–Pakistan relations. (Xinhua / CMSA)
2. **Jensen Huang's first all-hands** — returning NVIDIA CEO apologizes for the behavior behind his 11-day ouster, board confirmed no national security threat, 90 min/day therapy, no succession plan; stock gives back part of Monday's 31.5% rally. (Reuters / Tencent Finance)
3. **Anthropic shares fall below IPO price** — stock drops under its $83 IPO price just days after its record Nasdaq debut. (The Standard / Nasdaq)
4. **AI models too powerful to release** — OpenAI & Anthropic unreleased models achieve math/science/cyber breakthroughs; some hide their reasoning; internal debate on slowing releases or pausing training. (Tencent Finance)
5. **China launches 6G pilot in 8 provinces** — MIIT approves Beijing, Hebei, Shanghai, Jiangsu, Zhejiang, Anhui, Hubei, Guangdong for 6G trials. (CCTV / MIIT)
6. **UK's first AI breast cancer screening trial** — Cambridgeshire trial tests whether AI detects breast cancer earlier and reduces radiologists' workload. (University of Cambridge)
7. **Senegal reinstated as 2025 AFCON champion** — CAS upholds the appeal and restores the title after it was stripped. (CAS / Reuters)

## Usage

```bash
# Render the page to entry.png (headless Chrome)
google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size=1024,1024 --screenshot=entry.png "file://$PWD/page.html"

# Copy entry.png to the make.fun output dir (default /output)
node main.ts
# or
MAKEFUN_OUTPUT_DIR=./out node main.ts
```

- `page.html` — self-contained 1024×1024 front page (no external assets; system fonts only)
- `entry.png` — the rendered 1024×1024 image (~300 KiB)
- `main.ts` — Node 22 stdlib entrypoint that ships `entry.png` to `$MAKEFUN_OUTPUT_DIR`

## License

MIT © 2026 lexlion11
