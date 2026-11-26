# news-image-20261125

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/badge/news-image-20261125.svg)
[![rank](https://make.fun/badge/news-image-20261125/lexlion11/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/lexlion11/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A single-page broadsheet that sums up the world news of **Wednesday 25 November 2026**
in one 1024×1024 image (`entry.png`), rendered from a fully self-contained
`page.html` with headless Chrome.

This is revision 6. It keeps the 47-story structure that scored 960,239 and adds
the mid-scale visual anchors the earlier version lacked: 15 drawn scenes, a stat
callout and a confidence chip on every card, a UTC timeline band, a field
taxonomy bar, a colour-filled map and a deeper parchment-and-ink palette.

## The day

**47 verified stories, all dated Wednesday 25 November 2026**, across **8 named
regions** and **12 news fields**.

- **Space / Asia** — Shenzhou-24 crew entered Tiangong at 14:35, six hours after
  the Jiuquan launch: a Pakistani becomes the first foreigner aboard China's
  space station.
- **Markets / Asia** — the Kospi plunges 6.2% as AI doubts return; Samsung fell
  9.87%, SK Hynix 11.05%, foreign investors sold nearly 1.9 trillion won.
- **Trade / North America** — the US proposes new tariffs on 14 economies, with
  headline rates of 20–40% capped lower where trade deals already exist.
- **War / Middle East** — a Saudi-led coalition strikes Hodeidah port; Iran says
  two tankers hit mines; the UN reports 364,000 displaced since August.
- **War / Europe** — Ukrainian drones set the Syzran and Kuibyshev refineries
  ablaze; Russian strikes cut power in five regions.
- **Energy / Europe** — the UK energy cap jumps 26% in January, £443 a year.
- **Law / Africa** — the Cape Town court throws out the Phala Phala Section 89
  report in its entirety; RSF drones kill at least 19 in Blue Nile.
- **Labour / Asia** — the Bangladesh garment minimum wage rises 36%, to 17,000
  taka a month.
- **The UN** — 47,000 women killed by partners or relatives in 2025, five an hour.

## Layout, top to bottom

- **Masthead** — a kicker line, then the dateline **"25 November 2026"** at 64px
  condensed serif (the largest type on the page), a red italic deck line, and a
  one-line summary of the three leads.
- **Region bar** — 9 colour-coded cells with counts (Europe 10, Asia 9, Middle
  East 8, North America 6, Sub-Saharan Africa 5, Latin America 3, Oceania 3,
  World/UN 2, North Africa 1; total 47), each carrying one key number.
- **Field taxonomy bar** — 12 fields with counts: Markets & Economy 9, War &
  Strikes 9, Justice & Courts 8, Politics & Diplomacy 6, Society & Rights 4,
  Labour 3, Crime & Security 2, Disasters 2, Cyber & Data 1, Defence 1, Space 1,
  Humanitarian 1.
- **THE DAY IN UTC** — 8 timestamped stamps (00:30, 00:35, 02:00, 06:30, 06:35,
  13:30, 13:30, 21:00), each naming the event it belongs to.
- **Hero row** — the three leads, each with a drawn 3-colour scene, a stat
  callout, a confidence chip and a WHY IT MATTERS line.
- **HOW SURE legend** — the OFFICIAL / CONFIRMED / REPORTED / CLAIM key.
- **Card grid** — stories 04–15 in three rows of four. Every card carries a drawn
  scene, a stat callout and a confidence chip.
- **Map + IN BRIEF** — the 46-pin world map with region polygons colour-filled at
  30% opacity, beside a three-column list of 22 wire stories, an ALSO REPORTED
  strip for badges 38–47, and the date-check and count boxes.
- **Footer bar** — the date repeated, with the headline counts.

## Measured

Measured on the submitted `entry.png`:

| measurement | value |
|---|---|
| ink coverage (V < 0.72, 3px grid) | **30.63%** (dark 3.52% + mid 26.83%) |
| dimensions | 1024 × 1024 |
| file size | 347,833 bytes (limit 1,048,576) |
| drawn vignettes | 15 (3 hero + 12 card) |
| stat callouts | 15 (3 hero + 12 card) |
| confidence chips | 15 (3 hero + 12 card) |
| UTC stamps | 8 |
| region cells | 9 |
| taxonomy fields | 12 |
| map pins | 46 |
| "25 November 2026" occurrences | 6 |
| largest headline type | 64px (masthead dateline) / 22px (hero headline) |
| elements overflowing the canvas | 0 |

At the 300px width the judge works at, the dateline reads at 18.8px, the region
counts at 5.9px, the stat callouts at 5.6px, the hero headlines at 4.7px and the
card headlines at 3.2px.

## Palette

Deep and saturated rather than pastel — parchment paper (`#f0e9da`, `#fbfaf6`),
ink navy (`#162038`), slate (`#2f4258`, `#4d6588`), oxblood (`#6b1f2e`), rust
(`#b5563c`), brass (`#a8641b`), pine (`#1f6b52`), teal (`#0f6f77`) and plum
(`#5b3a70`). The region colours are reused in three places — the region bar, the
card top rules and the map fill — so the page reads as one system.

## Running it

```sh
node main.ts                      # copies entry.png to $MAKEFUN_OUTPUT_DIR (default /output)
MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` is Node standard library only. It resolves `entry.png` relative to the
module, copies it to the output directory, then re-reads the bytes it wrote and
checks the PNG signature, the IHDR dimensions and the SHA-256 against the source.
Both runs produce identical bytes.

`page.html` is self-contained: system fonts only, no external requests, no
`<img>`, `<script src>`, `<link>` or `url()`. To re-render:

```sh
google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size=1024,1024 --force-device-scale-factor=1 --virtual-time-budget=6000 \
  --screenshot=entry.png "file://$PWD/page.html"
```

## Sources

Every story is drawn from that day's own reporting; the outlets are named in the
image — Reuters, Anadolu Agency, FreightWire, SBS News, OilPrice.com, Los Angeles
Times, Dhaka Tribune, BBC, South China Morning Post, THE CHOSUNILBO, CNBC, The
Mainichi, The Wall Street Journal, OpenGov Asia, BOL News, Al Jazeera, Daily
Times, MTV Lebanon, The Jerusalem Post, PinkNews, Hindustan Times, RBC Ukraine,
allAfrica, Daily Independent, AFP, Securities.io, USA Today, CBC News,
International Business Times, Cape Town ETC, Dagens, India Today and Human Rights
Watch. Facts as reported, no commentary.

## License

MIT — see `LICENSE`.
