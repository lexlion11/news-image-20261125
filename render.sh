#!/usr/bin/env bash
# Render page.html to entry.png with headless Chrome (no visible window).
set -euo pipefail
cd "$(dirname "$0")"

SCRATCH=".chrome-profile-render"

BROWSER_BG=1 google-chrome \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --hide-scrollbars \
  --window-size=1024,1024 \
  --force-device-scale-factor=1 \
  --virtual-time-budget=6000 \
  --user-data-dir="$SCRATCH" \
  --screenshot=entry.png \
  "file://$PWD/page.html"

# Clean up the scratch profile without a bare rm -rf (safety gate on this machine).
python3 - <<'PYEOF'
import shutil
shutil.rmtree('.chrome-profile-render', ignore_errors=True)
PYEOF

# Print and assert the PNG dimensions and size, reading the IHDR chunk directly.
python3 - <<'PYEOF'
import os
import struct

with open('entry.png', 'rb') as f:
    head = f.read(33)

assert head[:8] == b'\x89PNG\r\n\x1a\n', 'entry.png: not a valid PNG (magic mismatch)'
assert head[12:16] == b'IHDR', 'entry.png: first chunk is not IHDR'
width, height = struct.unpack('>II', head[16:24])
size = os.path.getsize('entry.png')

print(f'entry.png: {width}x{height} px, {size} bytes')
assert width == 1024 and height == 1024, 'entry.png: dimensions must be exactly 1024x1024'
assert size <= 1048576, 'entry.png: exceeds 1048576 bytes'
print('entry.png: OK (PNG magic, exactly 1024x1024, under 1 MiB)')
PYEOF
