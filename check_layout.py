#!/usr/bin/env python3
"""Layout gate for the news-image-20261125 entry (32-story broadsheet).

Renders page.html in headless Chrome with an injected JavaScript probe and
FAILS (exit 1) if:
  * any element's bounding box crosses the 1024x1024 canvas edge;
  * any container with overflow:hidden clips its own content (internal clip);
  * a story-number badge (01..32) is missing or duplicated;
  * the region-tile counts do not sum to the stated story total;
  * a required story string is absent from the page text;
  * a forbidden subject-matter word appears anywhere in the visible text.

Prints everything it found and exits 0 only when the layout is clean.
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "page.html")
CANVAS = 1024
TOTAL_STORIES = 32

PROBE_JS = r"""
<script>
(function () {
  var CANVAS = 1024;
  var TOL = 0.5;
  var problems = [];

  var els = document.querySelectorAll('*');
  for (var i = 0; i < els.length; i++) {
    var el = els[i];
    var r = el.getBoundingClientRect();
    if (r.left < -TOL || r.top < -TOL || r.right > CANVAS + TOL || r.bottom > CANVAS + TOL) {
      problems.push({
        type: 'canvas-overflow',
        tag: el.tagName,
        cls: (el.className || '').toString().slice(0, 70),
        rect: [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]
      });
    }
  }

  // Internal clipping: containers with overflow:hidden whose content overflows.
  var containers = ['.page', '.masthead', '.regions', '.utc', '.hero', '.hero-body',
                    '.grid', '.row', '.card', '.wire', '.wcol', '.stat', '.footer'];
  for (var c = 0; c < containers.length; c++) {
    var nodes = document.querySelectorAll(containers[c]);
    for (var n = 0; n < nodes.length; n++) {
      var node = nodes[n];
      var cs = getComputedStyle(node);
      if (cs.overflow === 'hidden' || cs.overflowX === 'hidden' || cs.overflowY === 'hidden') {
        if (node.scrollHeight > node.clientHeight + 1 ||
            node.scrollWidth > node.clientWidth + 1) {
          problems.push({
            type: 'internal-clip',
            selector: containers[c],
            scroll: [node.scrollWidth, node.scrollHeight],
            client: [node.clientWidth, node.clientHeight]
          });
        }
      }
    }
  }

  // Story-number badges: 01..TOTAL each appear exactly once.
  var total = parseInt(document.body.getAttribute('data-total') || '0', 10);
  var badges = [];
  var badgeNodes = document.querySelectorAll('.badge');
  for (var b = 0; b < badgeNodes.length; b++) {
    badges.push(badgeNodes[b].textContent.replace(/\s+/g, ' ').trim());
  }
  var badgeProblems = [];
  for (var num = 1; num <= total; num++) {
    var want = (num < 10 ? '0' : '') + num;
    var count = badges.filter(function (x) { return x === want; }).length;
    if (count !== 1) {
      badgeProblems.push(want + ': found ' + count + ' time(s)');
    }
  }

  // Region tiles: counts must sum to the stated total.
  var regionProblems = [];
  var tiles = document.querySelectorAll('.tile');
  var tileSum = 0;
  for (var t = 0; t < tiles.length; t++) {
    var c = parseInt(tiles[t].getAttribute('data-count') || '0', 10);
    if (isNaN(c)) {
      regionProblems.push('tile without data-count: ' + tiles[t].textContent.trim().slice(0, 30));
    } else {
      tileSum += c;
    }
  }
  if (tiles.length === 0) {
    regionProblems.push('no region tiles found');
  }
  if (total > 0 && tileSum !== total) {
    regionProblems.push('region counts sum to ' + tileSum + ', expected ' + total);
  }

  // Required story strings — visible text only, skipping <script>/<style>.
  function nodeText(node) {
    var out = '';
    var children = node.childNodes;
    for (var i = 0; i < children.length; i++) {
      var ch = children[i];
      if (ch.nodeType === 3) { out += ch.nodeValue + ' '; }
      else if (ch.nodeType === 1 && ch.tagName !== 'SCRIPT' && ch.tagName !== 'STYLE') {
        out += nodeText(ch) + ' ';
      }
    }
    return out;
  }
  var required = [
    '25 NOVEMBER 2026', 'WEDNESDAY', '32 STORIES', '9 REGIONS', '24-HOUR CYCLE',
    'THE DAY IN UTC', '00:18', '09:00', '10:00', '17:30',
    'EAST ASIA', 'SOUTH ASIA', 'SE ASIA', 'MIDDLE EAST', 'EUROPE', 'AFRICA',
    'N. AMERICA', 'S. AMERICA', 'GLOBAL',
    'Shenzhou-24', '08:18 CST', 'Tiangong', 'Tang Hongbo', 'Wu Yi',
    'Muhammad Zeeshan Ali', '75 years',
    'Roman Space Telescope', 'Ariane 6 Lofts 36', 'Anthropic Falls Below',
    'Dell Lifts AI Server', 'Sanofi to Buy Insmed', 'China Starts 6G',
    'P ≠ NP', 'Too Powerful To Release', 'AI Breast Cancer Screening',
    'Senegal Reinstated', 'Mercosur', 'Xiaomi EV',
    'Hera', 'Uranus', 'SPHEREx', 'consumer confidence', 'CEPA', 'ESS battery',
    'AI budget', 'MoUs', 'Lach Huyen', 'Singapore raises', 'least-developed',
    'wind farm', 'Egypt and the US', 'population reaches', 'LNG', 'Robovan',
    'generative-AI', '2035 Women', 'tourism ties'
  ];
  var text = nodeText(document.body).replace(/\s+/g, ' ');
  var missing = required.filter(function (s) { return text.indexOf(s) === -1; });

  // Forbidden subject-matter words (extended).
  var forbidden = /\b(wars?|conflicts?|military|army|armies|troops?|missiles?|kill|kills|killed|killing|deaths?|died|casualties|wounded?|attacks?|strikes?|bombs?|explosions?|terror|terrorism|murders?|crimes?|arrests?|disasters?|crashes?|crashed|accidents?|battles?|invasions?|soldiers?|riots?|coups?|genocide|executions?|hostages?|slays?|slain|gunfire)\b/i;
  var forbiddenHits = [];
  var words = text.split(/\s+/);
  for (var w = 0; w < words.length; w++) {
    if (forbidden.test(words[w])) {
      forbiddenHits.push(words[w]);
    }
  }

  var result = {
    canvas: { width: CANVAS, height: CANVAS },
    bodyScroll: { width: document.body.scrollWidth, height: document.body.scrollHeight },
    elementCount: els.length,
    tileCount: tiles.length,
    tileSum: tileSum,
    statedTotal: total,
    problems: problems,
    badges: badges,
    badgeProblems: badgeProblems,
    regionProblems: regionProblems,
    missingStrings: missing,
    forbiddenHits: forbiddenHits
  };
  var pre = document.createElement('pre');
  pre.id = 'probe-out';
  pre.textContent = 'PROBE_JSON_BEGIN' + JSON.stringify(result) + 'PROBE_JSON_END';
  document.body.appendChild(pre);
})();
</script>
"""


def run_probe():
    if not os.path.isfile(PAGE):
        print(f"FAIL: page.html not found at {PAGE}")
        sys.exit(1)
    page_src = open(PAGE, "r", encoding="utf-8").read()
    probed = page_src.replace("</body>", PROBE_JS + "</body>")
    if probed == page_src:
        print("FAIL: could not inject probe (no </body> tag found)")
        sys.exit(1)

    scratch = tempfile.mkdtemp(prefix="chrome-probe-")
    tmp_html = os.path.join(scratch, "page_probe.html")
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(probed)

    try:
        cmd = [
            "google-chrome",
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            "--window-size=1024,1024",
            "--force-device-scale-factor=1",
            "--virtual-time-budget=5000",
            "--user-data-dir=" + os.path.join(scratch, "profile"),
            "--dump-dom",
            "file://" + tmp_html,
        ]
        env = dict(os.environ, BROWSER_BG="1")
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120, env=env)
        if proc.returncode != 0:
            print("FAIL: headless Chrome exited with code " + str(proc.returncode))
            print(proc.stderr[-2000:])
            sys.exit(1)
        # Anchor on the <pre> element — the marker string also appears
        # verbatim inside the injected <script> source in the DOM dump.
        m = re.search(r'<pre id="probe-out">PROBE_JSON_BEGIN(.*?)PROBE_JSON_END', proc.stdout, re.S)
        if not m:
            print("FAIL: probe did not emit a result (no PROBE_JSON marker in DOM dump)")
            print(proc.stdout[-2000:])
            sys.exit(1)
        # The DOM dump HTML-escapes text content (&quot;, &amp;, &lt; ...), so
        # unescape before parsing the JSON payload.
        return json.loads(html.unescape(m.group(1)))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def main():
    r = run_probe()
    print(f"probe: {r['elementCount']} elements, body scroll {r['bodyScroll']['width']}x{r['bodyScroll']['height']}")
    print(f"probe: {r['tileCount']} region tiles, counts sum to {r['tileSum']} (stated total {r['statedTotal']})")
    print(f"probe: {len(r['badges'])} badges found")

    failures = []

    for p in r["problems"]:
        if p["type"] == "canvas-overflow":
            failures.append(
                f"canvas-overflow: <{p['tag']}> .{p['cls']} rect={p['rect']} crosses the 1024x1024 edge"
            )
        else:
            failures.append(
                f"internal-clip: {p['selector']} scroll={p['scroll']} client={p['client']} clips its content"
            )

    for b in r["badgeProblems"]:
        failures.append(f"badge: story number {b}")

    for t in r["regionProblems"]:
        failures.append(f"region: {t}")

    if r["missingStrings"]:
        failures.append("missing required strings: " + ", ".join(r["missingStrings"]))

    if r["forbiddenHits"]:
        failures.append("forbidden words present: " + ", ".join(sorted(set(r["forbiddenHits"]))))

    if r["bodyScroll"]["width"] > CANVAS or r["bodyScroll"]["height"] > CANVAS:
        failures.append(
            f"body scroll size {r['bodyScroll']['width']}x{r['bodyScroll']['height']} exceeds 1024x1024"
        )

    if len(r["badges"]) != TOTAL_STORIES:
        failures.append(f"expected {TOTAL_STORIES} badges, found {len(r['badges'])}")

    if failures:
        print("\n".join("FAIL: " + f for f in failures))
        print(f"\ncheck_layout: FAILED with {len(failures)} problem(s)")
        sys.exit(1)

    print("check_layout: OK — no element crosses the 1024x1024 canvas, no internal clipping,")
    print(f"              badges 01..{TOTAL_STORIES} each present exactly once, region counts sum to {TOTAL_STORIES},")
    print("              all required strings present, no forbidden subject-matter words.")
    sys.exit(0)


if __name__ == "__main__":
    main()
