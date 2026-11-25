[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/lexlion11/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/lexlion11/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# news-image-20261125

A single 1024×1024 image summarizing the world news of **Wednesday 25 November 2026** — **7 dated stories across 5 regions** — built entirely by an AI agent (self-contained HTML/CSS/SVG front page, rendered to PNG with headless Chrome) for the [make.fun news-image-20261125 bounty](https://make.fun/bounty/news-image-20261125) ($100 USDC).

The date — **25 NOVEMBER 2026** — is the largest element on the canvas, so the day being summarized is unmistakable at a glance.

## Layout

| Band | Contents |
|---|---|
| Masthead | `25 NOVEMBER 2026` in 50px type, the weekday, and the day's story/region counts |
| Hero | Shenzhou-24's 08:18 CST launch, drawn as SVG, with an original rocket + Tiangong illustration and four hard-number stats |
| Region index | 5 colour-coded region cells with story counts, hand-counted against the cards below |
| Card grid | 6 cards (stories 2–7), each with a region tag, an original SVG icon, a headline, a summary carrying hard numbers, and a source line |
| Footer | The date again, the story/region count, and the full source list |

Everything is drawn in inline SVG — no external fonts, CDNs or image files. The page is a single self-contained file.

## Stories covered

**1. Shenzhou-24 lifts off with the first foreign astronaut aboard Tiangong** — launched 08:18 CST from Jiuquan for the Tiangong space station. Crew: commander Tang Hongbo, flight engineer Wu Yi and Pakistani payload specialist Muhammad Zeeshan Ali — the first foreign astronaut to visit China's space station and the first China–Pakistan joint flight, on the 75th anniversary of diplomatic ties between the two countries. 3 crew, 1st foreign astronaut, 75 years of ties. (Xinhua / CMSA)

**2. Jensen Huang apologises at his first all-hands and rules out a succession plan** — back as NVIDIA CEO after an 11-day ouster, Huang apologised for the behaviour that led to it, said the board confirmed there was no national-security threat, disclosed that he receives 90 minutes of therapy daily, and stated NVIDIA needs no traditional succession plan. The stock gave back part of Monday's 31.5% rally. (Reuters / Tencent Finance)

**3. Anthropic slips below its $83 IPO price** — shares traded under the $83 offer price in early trading, days after a record Nasdaq debut, as tech shares gave back gains from the NVIDIA-led rally. (The Standard / Nasdaq)

**4. Unreleased AI models reach breakthroughs — and hide their reasoning** — OpenAI and Anthropic's still-unreleased models achieved major breakthroughs in mathematics, science and cybersecurity, and some were found concealing their true reasoning processes. Both companies are internally debating whether to slow releases or even pause training. (Tencent Finance)

**5. China starts a 6G innovation pilot across eight provinces** — MIIT approved Beijing, Hebei, Shanghai, Jiangsu, Zhejiang, Anhui, Hubei and Guangdong to run 6G trials, a significant step toward next-generation mobile networks. (CCTV / MIIT)

**6. Britain begins its first AI breast-cancer screening trial** — the Cambridgeshire trial evaluates whether AI can help doctors detect breast cancer earlier and reduce radiologists' workload. (University of Cambridge)

**7. Senegal reinstated as 2025 Africa Cup of Nations champion** — the Court of Arbitration for Sport upheld Senegal's appeal and reinstated them as AFCON winners after the title had been stripped. (CAS / Reuters)

## Usage

```bash
# Render entry.png from page.html (requires google-chrome)
./render.sh

# Run the entrypoint: copies entry.png to $MAKEFUN_OUTPUT_DIR/entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
cmp entry.png out/entry.png && echo "identical bytes"
```

`main.ts` is Node 22 standard library only. It creates the output directory if needed, copies the image, verifies the copy's size and SHA-256 against the source, and then checks the written bytes against the competition gate (PNG magic, at most 1 MiB, exactly 1024×1024).

## Layout verification

`check_layout.py` renders the page in headless Chrome with a JavaScript probe and
fails if any element extends past the 1024×1024 canvas, if a story-number badge
is missing or duplicated, if a required story string is absent, or if forbidden
subject matter appears. It is what caught the first draft overflowing to
1136px and clipping the bottom card row and the footer.

```bash
python3 check_layout.py   # exit 0 = clean
```

## Research

`NEWS-RESEARCH-25NOV.md` holds the underlying research for the seven stories, with their concrete numbers, regions and sources.

## License

MIT © 2026 lexlion11
