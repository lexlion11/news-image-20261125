/**
 * news-image-20261125 — entrypoint
 *
 * Copies entry.png to $MAKEFUN_OUTPUT_DIR/entry.png (default /output),
 * creating the output directory if needed.
 *
 * Node 22 stdlib only. Run with: node main.ts
 */

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { createHash } from "node:crypto";

const SOURCE_FILE = resolve(import.meta.dirname ?? ".", "entry.png");
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const OUTPUT_FILE = join(OUTPUT_DIR, "entry.png");

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

console.log(`OK: copied ${SOURCE_FILE} -> ${OUTPUT_FILE} (${outStat.size} bytes, sha256 verified)`);
