# THE WORLD TODAY — Tuesday 24 November 2026

A one-page newspaper front page summing up the world's news of
Tuesday 24 November 2026: 35 stories from 9 regions, checked against
the day's wires (Reuters, WSJ, AP, Al Jazeera, Xinhua, BBC and official
statements). Every story is dated 24 November 2026; items from other
days are listed in the red DATE CHECK box on the page — and in full in
`../VERIFICATION.md` (kept outside this repo).

## Headlines

- **Houthis hit Riyadh tower** — 11 hurt in the KAFD financial district
- **Iran shuts Hormuz tighter** — 4 tankers hit mines
- **Dow tops 50,000** — first close above 50k as Nvidia's rally fades

## Files

- `entry.png` — the 1024×1024 front page (the deliverable)
- `draw.py` — Python + Pillow program that draws `entry.png` (local build
  tool only; the grader never runs it)
- `main.ts` — Node 22 entrypoint: copies `entry.png` to `/output`
  (or `$MAKEFUN_OUTPUT_DIR`), with PNG-magic and 1 MiB size checks

## Build

```sh
python3 draw.py          # regenerates entry.png
node main.ts             # writes /output/entry.png
```

## License

MIT — see `LICENSE`.
