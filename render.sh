#!/bin/bash
# Render the 25 November 2026 world-news digest page to a 1024x1024 PNG.
# Headless only, run in the background (BROWSER_BG=1) per the browser-automation rule.
set -euo pipefail

DIR=/home/lex/.openclaw/workspace/tmp/makefun/news-image-25
CHROME=/usr/bin/google-chrome

# Chrome must never reuse an existing profile; keep it in a scratch dir under workspace/tmp.
PROFILE="$DIR/.chrome-profile"
rm -rf "$PROFILE"
mkdir -p "$PROFILE"

COMMON=(
  --headless=new
  --disable-gpu
  --no-sandbox
  --hide-scrollbars
  --window-size=1024,1024
  --force-device-scale-factor=1
  --virtual-time-budget=6000
  --user-data-dir="$PROFILE"
  --screenshot="$DIR/entry.png"
  "file://$DIR/page.html"
)

"$CHROME" "${COMMON[@]}" 2>&1 | tail -3

rm -rf "$PROFILE"

python3 - "$DIR/entry.png" <<'PY'
import sys, struct
p = sys.argv[1]
with open(p, 'rb') as f:
    data = f.read()
assert data[:8] == b'\x89PNG\r\n\x1a\n', 'not a PNG'
w, h = struct.unpack('>II', data[16:24])
size = len(data)
print(f'entry.png {w}x{h} {size} bytes ({size/1048576:.3f} MiB)')
assert (w, h) == (1024, 1024), 'wrong dimensions'
assert size <= 1048576, 'over 1 MiB'
print('OK: within limits')
PY
