// news-image-20261125 — deliverable runner (Node stdlib only).
// Copies this entry's rendered image to the output directory the grader asks for.
// The source image is resolved relative to THIS module, never the CWD, so the
// entry works no matter where it is run from.

import { createHash } from "node:crypto";
import { copyFile, mkdir, open, readFile, stat } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MODULE_DIR = dirname(fileURLToPath(import.meta.url));
const SOURCE = join(MODULE_DIR, "entry.png");
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

async function fail(message) {
  console.error(`main.ts: ${message}`);
  process.exitCode = 1;
}

async function main() {
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  let sourceStat;
  try {
    sourceStat = await stat(SOURCE);
  } catch (err) {
    await fail(`source image missing or unreadable: ${SOURCE} (${err.code})`);
    return;
  }
  if (!sourceStat.isFile()) {
    await fail(`source image is not a regular file: ${SOURCE}`);
    return;
  }

  // Read the header and validate it is a whole PNG of exactly 1024x1024.
  let header;
  try {
    const handle = await open(SOURCE, "r");
    try {
      header = Buffer.alloc(24);
      await handle.read(header, 0, 24, 0);
    } finally {
      await handle.close();
    }
  } catch (err) {
    await fail(`could not read image header: ${err.code}`);
    return;
  }
  if (header.subarray(0, 8).equals(PNG_MAGIC) === false) {
    await fail("source image is not a valid PNG (bad magic bytes)");
    return;
  }
  const width = header.readUInt32BE(16);
  const height = header.readUInt32BE(20);
  if (width !== 1024 || height !== 1024) {
    await fail(`source image must be 1024x1024, found ${width}x${height}`);
    return;
  }

  try {
    await mkdir(outputDir, { recursive: true });
  } catch (err) {
    await fail(`could not create output directory ${outputDir} (${err.code})`);
    return;
  }

  const destination = join(outputDir, "entry.png");
  try {
    await copyFile(SOURCE, destination);
  } catch (err) {
    await fail(`could not copy image to ${destination} (${err.code})`);
    return;
  }

  const destHash = createHash("sha256").update(await readFile(destination)).digest("hex");
  const srcHash = createHash("sha256").update(await readFile(SOURCE)).digest("hex");
  if (srcHash !== destHash) {
    await fail("copied image does not match the source image");
    return;
  }
  console.log(`entry.png copied to ${destination} (${sourceStat.size} bytes, 1024x1024, sha256 ${srcHash.slice(0, 16)}…)`);
}

main();
