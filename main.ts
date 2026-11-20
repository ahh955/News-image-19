// Entry point for the make.fun news-image-20261119 bounty.
// Copies the pre-built entry.png (1024x1024, drawn procedurally by
// compose.py) into the output directory. Node 22 stdlib only.
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const dest = join(outDir, "entry.png");

if (!existsSync(src)) {
  console.error(`entry.png not found at ${src}`);
  process.exit(1);
}

// Validate the PNG before copying: 8-byte signature, then the IHDR chunk
// must declare a 1024x1024 image.
const buf = readFileSync(src);
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (buf.length < 33 || !buf.subarray(0, 8).equals(PNG_SIG)) {
  console.error("entry.png is not a valid PNG (bad signature)");
  process.exit(1);
}
if (buf.toString("ascii", 12, 16) !== "IHDR") {
  console.error("entry.png has no IHDR chunk where expected");
  process.exit(1);
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  console.error(`entry.png is ${width}x${height}, expected 1024x1024`);
  process.exit(1);
}
console.log(`entry.png validated: 1024x1024, ${buf.length} bytes`);
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);
console.log(`copied entry.png -> ${dest}`);
