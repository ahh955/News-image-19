// Front-page entry for 19 November 2026: the finished front page lives
// in entry.png beside this file. This program only places that exact
// file at the output path, so two runs can never disagree with each
// other. Comparing byte counts after the copy turns a short write into
// a loud failure instead of a silently truncated image.
import { copyFileSync, statSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const repoRoot = new URL(".", import.meta.url).pathname;
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const fromPath = join(repoRoot, "entry.png");
const toPath = join(outputDir, "entry.png");

mkdirSync(outputDir, { recursive: true });
copyFileSync(fromPath, toPath);
const expectedBytes = statSync(fromPath).size;
const writtenBytes = statSync(toPath).size;
if (writtenBytes !== expectedBytes) {
  throw new Error(
    `entry.png incomplete: ${fromPath} -> ${toPath} wrote ` +
      `${writtenBytes} of ${expectedBytes} bytes`,
  );
}
