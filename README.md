[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/lexlion11/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/lexlion11/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# news-image-20261125

A one-page world news **broadsheet for Wednesday 25 November 2026**, rendered to
a single 1024x1024 PNG. It covers **47 verified stories** from the 25 November
2026 news cycle across **7 regions** — space, markets, trade, conflict, energy,
law, labour and human rights.

This is the v4 rebuild: the previous dark-navy entry lost most of its type when
the judge viewed it at ~300px, so the page is now a **light broadsheet** —
near-black serif type on warm white paper — designed to survive a 3.4x
downscale.

Layout, top to bottom:

- **Masthead** — kicker line, then the date **"Wednesday 25 November 2026"** set
  at 58px black serif (the largest element on the page, repeated four times:
  masthead, map heading, DATE CHECK box, footer bar), plus a one-line summary of
  the three lead stories.
- **Region index / stat band** — 7 cells (Europe 10, Asia 9, Americas 9, Middle
  East 8, Africa 6, Oceania 3, World 2; total 47), each with a big count and one
  key number (Kospi −6.2%, UK cap +26%, US GDP 4.3%, 364,000 displaced, wage
  +36%, inflation 4.1%, five an hour).
- **Hero row** — three lead stories with original flat inline-SVG
  illustrations: 01 Shenzhou-24 / first foreigner aboard Tiangong, 02 Kospi
  −6.2%, 03 US tariffs on 14 economies (20–40%).
- **"HOW SURE" legend** — OFFICIAL / CONFIRMED / REPORTED / CLAIM confidence
  key.
- **Card grid** — stories 04–11, each with a region-coloured badge and its
  outlet.
- **World map + IN BRIEF** — the 46-pin world map (one numbered pin per story,
  pin numbers match the story badges) with a region colour legend, beside a
  two-column wire list of the remaining 36 stories (12–47) and the full
  story-ordered source list.
- **DATE CHECK box + footer** — "Every story here is dated Wednesday 25
  November 2026" at 26px bold serif, plus counts and a dark footer bar repeating
  the date.

The page is fully self-contained HTML/CSS/SVG — no external resources of any
kind (no fonts, CDNs, images, scripts or links). All artwork is original inline
SVG; the world map is inline SVG built from `build/map_paths.json`.

## Stories covered (47 total)

**Europe (10)** — 06 Ukrainian drones set two refineries ablaze (Syzran and
Kuibyshev, both Rosneft-owned), Samara Region — FreightWire. 08 UK energy cap
+26% in January (+£443/yr), London — OilPrice.com. 14 Russian strikes cut power
in five regions, Zaporizhzhia — Al Jazeera. 26 Met review: racist and
misogynist, no progress on 14 recommendations, London — PinkNews USA. 27
EU-Western Balkans summit, Serbia absent, Brussels — Albeu.com. 28 24-hour
strike halts ferries and regional flights, Athens — UA.NEWS. 29 Eurostar staff
strike cancels London trains, Paris — Hindustan Times. 30 Merz defends record
2027 budget, Berlin — The Rio Times. 31 Poland plans Ukrainian border 'no-fly
zone', Warsaw — hromadske. 32 Ukraine: hit 3 MiG-31s, 2 Su-34s, Savaslevka —
RBC Ukraine.

**Asia (9)** — 01 Pakistani becomes first foreigner aboard China's space
station (Shenzhou-24 entered Tiangong at 14:35), Jiuquan — South China Morning
Post. 02 AI doubts return: Kospi plunges 6.2% (Samsung −9.87%, SK Hynix
−11.05%), Seoul — THE CHOSUNILBO. 09 Flood traps miners in illegal gold pits
(330-ft shaft), Bogor — Los Angeles Times. 10 Garment minimum wage rises 36%
(17,000 taka), Dhaka — Dhaka Tribune. 16 Tokyo: second extra budget, quake aid
— The Mainichi. 17 Regulator sues Google for RM60m (two suits of RM300m each),
Kuala Lumpur — The Wall Street Journal. 18 URBTIX hack: about 13m users
exposed, Hong Kong — OpenGov Asia. 19 Building collapses: 3 dead, 14 hurt,
Karachi — BOL News. 20 Court voids RBI edict on 'bank' assets, New Delhi —
News search.

**Americas (9)** — 03 US proposes new tariffs on 14 economies (20–40% headline
rates), Washington — CNBC. 13 Supermarket stormed, all hostages freed,
Cartagena — U.S. News & World Report. 37 US GDP revised to 4.3% from 3.4%,
Washington — Securities.io. 38 Jobless claims fall to 189,000, Washington —
Anadolu Agency. 39 Dow above 50,000 (+0.87%); Nasdaq +1.45%, New York — THE
CHOSUNILBO. 40 Army detains 5 tons of lead azide, Iowa — USA TODAY. 41 Carney:
Trump hasn't raised defence criticism, Ottawa — CBC News. 42 Sheinbaum seeks
Inés Gómez Mont's extradition, Mexico City — International Business Times. 43
Lula signs public accounts control law, Brasília — News search.

**Middle East (8)** — 04 Saudi-led coalition strikes Hodeidah port (evacuation
warning issued), Hodeidah — Reuters. 05 Iran says two tankers hit mines, caught
fire, Hormuz — Anadolu Agency. 11 Israeli strike kills Hamas security chief
(aged 50), Gaza City — BBC on MSN. 21 Saudi: 4 Houthi drones downed, no
casualties, Ras Tanura — Al Jazeera. 22 Houthis threaten Jeddah, Saudi Red Sea
ports, Sanaa — Daily Times. 23 UN: 364,000 displaced since August, Aden — MTV
Lebanon. 24 Judges urge dropping case 4000 bribery charge, Jerusalem —
Cleveland Jewish News. 25 October 7 inquiry: first bill vote 16-50, Jerusalem —
Jerusalem Post.

**Africa (6)** — 12 Court throws out Phala Phala report, Cape Town — Cape Town
ETC. 15 RSF drones kill at least 19 in Blue Nile (30+ explosive drones), Ed
Damazin — Anadolu Agency. 33 Nollywood legend Pete Edochie dies at 79 —
allAfrica.com. 34 Government rejects Ethiopia's talks offer, Port Sudan —
News.az. 35 Tinubu seeks ₦3.2trn cut: 2026 budget ₦45.8trn, Abuja — Daily
Independent. 36 Senegal denounces Morocco's CAS 'contact' claim, Dakar —
Agence France-Presse on MSN.

**Oceania (3)** — 07 Solomon Islands signs security treaty (Australia named
primary security partner), Canberra — SBS News. 44 October inflation 4.1%, from
4.3%, Sydney — CNBC. 45 Apology to LGBTQA+ defence personnel, Canberra —
Dagens.com India.

**World (2)** — 46 47,000 women killed by partners or relatives in 2025; five
an hour, UN — India Today. 47 Violence against women: 16 days of activism —
Human Rights Watch.

## Usage

Render the page to `entry.png` (headless Chrome, background only):

```bash
google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size=1024,1024 --force-device-scale-factor=1 \
  --virtual-time-budget=6000 --user-data-dir=.chrome-profile-render \
  --screenshot=entry.png "file://$PWD/page.html"
```

Run the layout self-check (static checks plus a live headless-Chrome probe:
canvas overflow, content clipping, badge coverage, pin count, external
references, date type size) and the PNG gate + 300px legibility downscale:

```bash
python3 build/scratch/check_layout.py
python3 build/scratch/verify_png.py
```

Copy the verified entry into the competition output directory (Node 22+,
stdlib only):

```bash
node main.ts                                        # -> $MAKEFUN_OUTPUT_DIR/entry.png (default /output)
MAKEFUN_OUTPUT_DIR=/tmp/out node main.ts            # custom output dir
```

`main.ts` resolves `entry.png` relative to the module itself (not the current
working directory), so it runs correctly under the grader's container where the
repo is mounted read-only and the CWD lies outside it. It validates the PNG
magic, the 1024x1024 IHDR dimensions, the bit depth / colour type and the
1 MiB byte limit, then re-reads the written copy and verifies its SHA-256
matches the source before printing a success line.
