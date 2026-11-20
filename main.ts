// News-image-19 v2 entrypoint: copies the composed front page to /output.
//
// Node 22, standard library only, no network. Deterministic: the same
// entry.png bytes are copied on every run, so both grader runs agree.
// The image itself is built ahead of time by compose.py (Pillow); this
// program only verifies it and copies it into place.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1048576; // 1 MiB
const MAX_DIM = 1024; // pixels per side

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

const stat = statSync(source);
if (stat.size > MAX_BYTES) {
  throw new Error(
    `entry.png is ${stat.size} bytes, over the ${MAX_BYTES} byte limit`,
  );
}

const data = readFileSync(source);
if (data.length < 33) {
  throw new Error("entry.png is truncated: too short to hold a PNG header");
}
const head = data.subarray(0, 33);
const PNG_SIG = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
if (!head.subarray(0, 8).equals(PNG_SIG)) {
  throw new Error("entry.png is not a PNG file");
}
const width = head.readUInt32BE(16);
const height = head.readUInt32BE(20);
if (width > MAX_DIM || height > MAX_DIM) {
  throw new Error(
    `entry.png is ${width}x${height}, over the ${MAX_DIM}x${MAX_DIM} limit`,
  );
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
console.log(
  `copied entry.png (${stat.size} bytes, ${width}x${height}) to ${target}`,
);
