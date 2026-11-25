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

function readPngHeader(buf: Buffer, what: string): { width: number; height: number } {
  if (buf.subarray(0, 8).compare(PNG_MAGIC) !== 0) {
    fail(`${what} is not a valid PNG (magic bytes mismatch)`);
  }
  if (buf.length > MAX_BYTES) {
    fail(`${what} is ${buf.length} bytes, exceeds the ${MAX_BYTES} byte limit`);
  }
  // 8-byte signature, then IHDR: 4-byte length (must be 13), 4-byte type,
  // 4-byte width and 4-byte height, both big-endian, then bit depth and
  // color type.
  if (buf.length < 33 || buf.readUInt32BE(8) !== 13 || buf.subarray(12, 16).toString("ascii") !== "IHDR") {
    fail(`${what} has a malformed IHDR chunk`);
  }
  const width = buf.readUInt32BE(16);
  const height = buf.readUInt32BE(20);
  if (width !== REQUIRED_WIDTH || height !== REQUIRED_HEIGHT) {
    fail(`${what} is ${width}x${height}, must be exactly ${REQUIRED_WIDTH}x${REQUIRED_HEIGHT}`);
  }
  const bitDepth = buf[24];
  const colorType = buf[25];
  if (bitDepth !== 8 || ![0, 2, 3, 4, 6].includes(colorType)) {
    fail(`${what} has unsupported PNG bit depth ${bitDepth} / color type ${colorType}`);
  }
  return { width, height };
}

// Resolve the source relative to this module (not the CWD): the grader runs
// the entry from outside the repo, and a CWD-relative path failed a previous
// submission.
const source = process.argv[2] ?? fileURLToPath(new URL("./entry.png", import.meta.url));
const outputName = process.argv[3] ?? "entry.png";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

if (outputName !== basename(outputName) || outputName.includes("/") || outputName.includes("\\")) {
  fail(`output name must be a plain file name, got "${outputName}"`);
}
if (!existsSync(source) || !statSync(source).isFile()) {
  fail(`source image not found or not a regular file: ${source}`);
}

const srcBuf = readFileSync(source);
readPngHeader(srcBuf, "source");

mkdirSync(outputDir, { recursive: true });
const dest = join(outputDir, outputName);
copyFileSync(source, dest);

// Verify the copy that is actually on disk: identical bytes and a valid header.
const destBuf = readFileSync(dest);
if (destBuf.length !== srcBuf.length) {
  fail(`size mismatch after copy: source ${srcBuf.length}, destination ${destBuf.length}`);
}
const srcHash = createHash("sha256").update(srcBuf).digest("hex");
const destHash = createHash("sha256").update(destBuf).digest("hex");
if (srcHash !== destHash) {
  fail(`SHA-256 mismatch: source ${srcHash} != destination ${destHash}`);
}
const { width, height } = readPngHeader(destBuf, "destination");
console.log(
  `entry: copied ${source} -> ${dest} (${destBuf.length} bytes, ${width}x${height} px, sha256 ${destHash}) verified OK`
);
