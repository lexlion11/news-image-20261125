/**
 * news-image-20261125 — entrypoint
 *
 * Copies entry.png to $MAKEFUN_OUTPUT_DIR/entry.png (default /output),
 * creating the output directory if needed.
 *
 * The entry is a 1024x1024 PNG digest of the world news of 25 November 2026,
 * rendered ahead of time from page.html. The harness runs this twice and both
 * runs must write identical bytes, so the copy is byte-verified.
 *
 * Node 22 stdlib only. Run with: node main.ts
 */

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { basename, join, resolve } from "node:path";
import { createHash } from "node:crypto";

/** The gate: a whole PNG (or JPEG) of at most 1 MiB and 1024x1024 pixels. */
const MAX_BYTES = 1048576;
const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

/** Read the width and height out of a PNG IHDR chunk. */
function pngDimensions(buffer: Buffer): { width: number; height: number } | null {
  // 8-byte signature, then an IHDR chunk: 4-byte length, "IHDR", then width/height.
  if (buffer.length < 24) return null;
  if (buffer.subarray(12, 16).toString("latin1") !== "IHDR") return null;
  return { width: buffer.readUInt32BE(16), height: buffer.readUInt32BE(20) };
}

const SOURCE_FILE = resolve(import.meta.dirname ?? ".", "entry.png");
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const OUTPUT_NAME = process.env.MAKEFUN_OUTPUT_NAME ?? "entry.png";
const OUTPUT_FILE = join(OUTPUT_DIR, OUTPUT_NAME);

function fail(message: string): never {
  console.error(`ERROR: ${message}`);
  process.exit(1);
}

// Source must exist and be a real file.
if (!existsSync(SOURCE_FILE)) {
  fail(`source image not found: ${SOURCE_FILE}`);
}

const sourceStat = statSync(SOURCE_FILE);
if (!sourceStat.isFile()) {
  fail(`source path is not a regular file: ${SOURCE_FILE}`);
}
if (sourceStat.size === 0) {
  fail(`source image is empty (0 bytes): ${SOURCE_FILE}`);
}

// Create output dir (recursive) if missing.
if (!existsSync(OUTPUT_DIR)) {
  mkdirSync(OUTPUT_DIR, { recursive: true });
} else {
  const dirStat = statSync(OUTPUT_DIR);
  if (!dirStat.isDirectory()) {
    fail(`output path exists but is not a directory: ${OUTPUT_DIR}`);
  }
}

// Refuse to clobber a path that is not a plain file name: the output name
// must stay inside the output directory.
if (OUTPUT_NAME !== basename(OUTPUT_NAME) || OUTPUT_NAME === "." || OUTPUT_NAME === "..") {
  fail(`MAKEFUN_OUTPUT_NAME must be a plain file name, got: ${OUTPUT_NAME}`);
}

copyFileSync(SOURCE_FILE, OUTPUT_FILE);

// Post-copy verification: destination must be a file of the same size,
// and its SHA-256 must match the source (guards against partial copies).
const outStat = statSync(OUTPUT_FILE);
if (!outStat.isFile()) {
  fail(`output is not a regular file: ${OUTPUT_FILE}`);
}
if (outStat.size !== sourceStat.size) {
  fail(`size mismatch after copy: source=${sourceStat.size} dest=${outStat.size}`);
}

const fileHash = (p: string): string => {
  const h = createHash("sha256");
  h.update(readFileSync(p));
  return h.digest("hex");
};

if (fileHash(SOURCE_FILE) !== fileHash(OUTPUT_FILE)) {
  fail(`SHA-256 mismatch between source and ${OUTPUT_FILE}`);
}

// Gate preconditions, checked on the bytes that were actually written.
const written = readFileSync(OUTPUT_FILE);
if (written.length > MAX_BYTES) {
  fail(`entry image is ${written.length} bytes, over the ${MAX_BYTES}-byte limit`);
}
if (!written.subarray(0, 8).equals(PNG_MAGIC)) {
  fail("entry image is not a PNG");
}
const dims = pngDimensions(written);
if (!dims) {
  fail("entry image has no readable PNG IHDR header");
}
if (dims.width !== EXPECTED_WIDTH || dims.height !== EXPECTED_HEIGHT) {
  fail(`entry image is ${dims.width}x${dims.height}, expected ${EXPECTED_WIDTH}x${EXPECTED_HEIGHT}`);
}

console.log(
  `OK: copied ${SOURCE_FILE} -> ${OUTPUT_FILE} (${outStat.size} bytes, ` +
    `${dims.width}x${dims.height}, sha256 verified)`,
);
