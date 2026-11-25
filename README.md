# news-image-20261125

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/badge/news-image-20261125.svg)
[![rank](https://make.fun/badge/news-image-20261125/lexlion11/news-image-20261125/rank.svg)](https://make.fun/badge/news-image-20261125/lexlion11/news-image-20261125/rank.svg)
[![reward](https://make.fun/badge/news-image-20261125/lexlion11/news-image-20261125/reward.svg)](https://make.fun/badge/news-image-20261125/lexlion11/news-image-20261125/reward.svg)

A single-page broadsheet that sums up the world news of **Wednesday 25 November 2026**
in one 1024×1024 image (`entry.png`), rendered from a fully self-contained
`page.html` with headless Chrome.

## What the image covers

- **Lead story** — Shenzhou-24: Pakistani astronaut Muhammad Zeeshan Ali becomes the
  first foreign visitor aboard China's Tiangong space station (launch 08:18 CST from
  Jiuquan, docking 14:35).
- **Asia** — Kospi plunges 6.2%; China approves 6G trials in eight provinces;
  Bangladesh garment minimum wage +36%; Japan's second extra budget; Malaysia sues
  Google for RM60m.
- **Americas** — US proposes tariffs on 14 economies; US GDP revised to 4.3%;
  jobless claims fall to 189,000; Dow above 50,000; Lula signs a public-accounts
  control law.
- **Europe** — UK energy cap +26% in January; EU–Western Balkans summit without
  Serbia; 24-hour strike halts ferries and regional flights; Eurostar strike;
  Merz defends a record 2027 budget.
- **Africa** — Phala Phala report thrown out; Tinubu seeks a ₦3.2trn budget cut;
  Senegal rejects Morocco's CAS 'contact' claim; Nigeria detains 5 tons of lead azide.
- **Oceania** — Solomon Islands–Australia security treaty; Australian inflation eases
  to 4.1%.
- **World** — UN reports 364,000 displaced since August; 47,000 women killed by
  partners or relatives in 2025.

## Usage

```bash
# Render the image (headless Chrome)
google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size=1024,1024 --force-device-scale-factor=1 \
  --virtual-time-budget=6000 --screenshot=entry.png "file://$PWD/page.html"

# Deliver the image to the output directory (Node stdlib only)
node main.ts                      # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=./out node main.ts
```

`main.ts` resolves `entry.png` relative to the module (`import.meta.url`), so it can
be run from any working directory. It validates that the source is a 1024×1024 PNG
and fails loudly otherwise.
