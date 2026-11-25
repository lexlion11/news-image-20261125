#!/usr/bin/env node
// news-image-20261125 entrypoint: copies the rendered entry.png into the
// competition output directory and verifies the bytes that were actually written.
// Node standard library only — no dependencies.
import { createHash } from "node:crypto";
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { basename, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1048576;
const REQUIRED_WIDTH = 1024;
const REQUIRED_HEIGHT = 1024;

function fail(msg: string): never {
  console.error(`entry: ${msg}`);
  process.exit(1);
}

// Default source is resolved relative to this module (not CWD), so the entry
// works no matter what directory the grader invokes node from.
const source = process.argv[2] ?? fileURLToPath(new URL("./entry.png", import.meta.url));
const outputName = process.argv[3] ?? "entry.png";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// The output name must be a plain file name — no path traversal, no separators.
if (
  outputName !== basename(outputName) ||
  outputName.includes("/") ||
  outputName.includes("\\") ||
  outputName === "." ||
  outputName === ".."
) {
  fail(`output name must be a plain file name, got "${outputName}"`);
}

// Source must exist, be a regular file, and be non-empty.
if (!existsSync(source)) {
  fail(`source image not found: ${source}`);
}
const srcStat = statSync(source);
if (!srcStat.isFile()) {
  fail(`source is not a regular file: ${source}`);
}
if (srcStat.size === 0) {
  fail(`source image is empty: ${source}`);
}

// Validate the source bytes against the competition gate before copying.
const srcBuf = readFileSync(source);
checkPng(srcBuf, "source");

function checkPng(buf: Buffer, what: string): void {
  if (buf.subarray(0, 8).compare(PNG_MAGIC) !== 0) {
    fail(`${what} is not a valid PNG (magic bytes mismatch)`);
  }
  if (buf.length > MAX_BYTES) {
    fail(`${what} is ${buf.length} bytes, exceeds the ${MAX_BYTES} byte limit`);
  }
  // PNG layout: 8-byte signature, then IHDR chunk: 4-byte length, 4-byte type,
  // then 4-byte width and 4-byte height (big-endian).
  if (buf.length < 33 || buf.readUInt32BE(8) !== 13 || buf.subarray(12, 16).toString("ascii") !== "IHDR") {
    fail(`${what} has a malformed IHDR chunk`);
  }
  const width = buf.readUInt32BE(16);
  const height = buf.readUInt32BE(20);
  if (width !== REQUIRED_WIDTH || height !== REQUIRED_HEIGHT) {
    fail(`${what} is ${width}x${height}, must be exactly ${REQUIRED_WIDTH}x${REQUIRED_HEIGHT}`);
  }
}

mkdirSync(outputDir, { recursive: true });
const dest = join(outputDir, outputName);
copyFileSync(source, dest);

// Verify the copy: same size, matching SHA-256, and gate-valid bytes on disk.
const destBuf = readFileSync(dest);
if (destBuf.length !== srcBuf.length) {
  fail(`size mismatch after copy: source ${srcBuf.length} bytes, destination ${destBuf.length} bytes`);
}
const srcHash = createHash("sha256").update(srcBuf).digest("hex");
const destHash = createHash("sha256").update(destBuf).digest("hex");
if (srcHash !== destHash) {
  fail(`SHA-256 mismatch: source ${srcHash} != destination ${destHash}`);
}
checkPng(destBuf, "destination");

const finalWidth = destBuf.readUInt32BE(16);
const finalHeight = destBuf.readUInt32BE(20);
console.log(
  `entry: copied ${source} -> ${dest} (${destBuf.length} bytes, ${finalWidth}x${finalHeight} px, sha256 ${destHash}) verified OK`
);
