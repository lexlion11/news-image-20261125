#!/usr/bin/env python3
"""Measure the rendered layout of page.html and report overflow / content checks.

Runs headless Chrome on an instrumented copy of the page, walks every element,
compares its bounding box against the 1024x1024 viewport, and reports elements
that stick out. Also checks the story-number badges for completeness/uniqueness,
that the required strings are present, and that no forbidden subject matter
appears.

Usage: python3 check_layout.py [page.html]
Exit code 0 = clean, 1 = overflow or forbidden content found.
"""
import html as html_mod
import json
import os
import re
import subprocess
import sys
import tempfile

DIR = os.path.dirname(os.path.abspath(__file__))
PAGE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(DIR, "page.html")

PROBE = r"""
(() => {
  const out = { overflow: [], badges: [], bodyText: '', scroll: null };
  // The deliverable is a 1024x1024 PNG; the page sets html/body to exactly that
  // size, so the canvas is 1024x1024 even though Chrome's window innerHeight
  // is smaller. Measure against the canvas, not the window.
  const vw = 1024, vh = 1024;
  const doc = document.documentElement;
  out.scroll = { sw: doc.scrollWidth, sh: doc.scrollHeight, winW: window.innerWidth, winH: window.innerHeight };
  const SKIP = new Set(['HTML', 'BODY']);
  for (const el of document.querySelectorAll('*')) {
    if (SKIP.has(el.tagName)) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    const over = [];
    if (r.left < -0.5) over.push('left=' + r.left.toFixed(1));
    if (r.top < -0.5) over.push('top=' + r.top.toFixed(1));
    if (r.right > vw + 0.5) over.push('right=' + r.right.toFixed(1));
    if (r.bottom > vh + 0.5) over.push('bottom=' + r.bottom.toFixed(1));
    // Decorative SVG strokes may bleed off the edge on purpose.
    const decorative = el.closest('svg') !== null && !el.textContent.trim();
    if (over.length && !decorative) {
      out.overflow.push({
        tag: el.tagName,
        cls: (el.getAttribute('class') || '').slice(0, 40),
        over: over.join(','),
        rect: [r.left, r.top, r.right, r.bottom].map(v => Math.round(v)),
        txt: (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 70)
      });
    }
  }
  for (const el of document.querySelectorAll('.hnumbadge, .cnum')) {
    out.badges.push({ cls: el.getAttribute('class'), txt: (el.textContent || '').trim() });
  }
  out.bodyText = (document.body.innerText || '').replace(/\s+/g, ' ');
  return JSON.stringify(out);
})()
"""


def instrument(page_src: str) -> str:
    """Return page_src with the probe injected; result lands in body[data-probe]."""
    snippet = (
        "<script>var R;try{R=" + PROBE + ";}catch(e){R='ERR '+String(e);}"
        "document.body.setAttribute('data-probe', R||'EMPTY');</script>"
    )
    return page_src.replace("</body>", snippet + "</body>")


def render_dump(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        page_src = fh.read()
    with tempfile.TemporaryDirectory(prefix="layout-probe-") as tmp:
        profile = os.path.join(tmp, "profile")
        os.makedirs(profile)
        wrapper = os.path.join(tmp, "probe.html")
        with open(wrapper, "w", encoding="utf-8") as fh:
            fh.write(instrument(page_src))
        cmd = [
            "/usr/bin/google-chrome",
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            "--window-size=1024,1024",
            "--force-device-scale-factor=1",
            "--virtual-time-budget=6000",
            f"--user-data-dir={profile}",
            "--dump-dom",
            f"file://{wrapper}",
        ]
        return subprocess.run(cmd, capture_output=True, text=True, timeout=150).stdout


def probe(path: str) -> dict:
    dom = render_dump(path)
    m = re.search(r'data-probe="(.*?)"', dom, re.S)
    if not m:
        print("PROBE FAILED: no data-probe attribute in dumped DOM")
        sys.exit(2)
    raw = html_mod.unescape(m.group(1))
    return json.loads(raw)


data = probe(PAGE)

print("viewport/scroll:", json.dumps(data["scroll"]))
ov = data["overflow"]
print(f"overflowing elements: {len(ov)}")
for o in ov:
    print(f"   {o['tag']:<8} cls={o['cls']:<22} {o['over']:<28} rect={o['rect']} {o['txt'][:46]!r}")

badges = data["badges"]
nums = [int(b["txt"]) for b in badges if re.fullmatch(r"\d+", b["txt"])]
print(f"badges: total={len(badges)} numeric={len(nums)} unique={len(set(nums))}")
if nums:
    print("   numbers:", sorted(nums))
    print("   min/max:", min(nums), max(nums))
    print("   missing in 1..max:", sorted(set(range(1, max(nums) + 1)) - set(nums)))
    print("   duplicated:", sorted({n for n in nums if nums.count(n) > 1}))

body = data.get("bodyText", "")
must = ["25 NOVEMBER", "2026", "Shenzhou", "Jensen", "Anthropic", "6G", "Senegal"]
missing = [s for s in must if s not in body]
print("required strings missing:", missing)

forbidden = ["war ", "conflict", "military", "killed", "casualt", "attack", "bomb", "shelling", "airstrike"]
hits = [w for w in forbidden if w in body.lower()]
print("forbidden-word hits:", hits)

bad = bool(ov) or bool(hits) or bool(missing)
print("RESULT:", "FAIL" if bad else "PASS")
sys.exit(1 if bad else 0)
