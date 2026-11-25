// main.ts — news-image-20261124 entrypoint (Node 22, stdlib only).
// COPY-ONLY: it copies the committed entry.png into the output directory.
// It never runs draw.py: the grader runs this file read-only as user 65534,
// so any write beside the repo (or any attempt to regenerate the image)
// would fail. draw.py is a local build tool only.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
const bytes = readFileSync(src);
if (bytes.length < 8 || bytes[0] !== 0x89 || bytes[1] !== 0x50 ||
    bytes[2] !== 0x4e || bytes[3] !== 0x47) {
  throw new Error("entry.png is not a PNG file");
}
if (bytes.length > 1024 * 1024) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
copyFileSync(src, join(outDir, "entry.png"));
const hash = createHash("sha256").update(bytes).digest("hex");
console.log(`entry.png ${bytes.length} bytes sha256 ${hash}`);
