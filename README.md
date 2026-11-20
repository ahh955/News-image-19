[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/ahh955/News-image-19/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard)
[![reward](https://make.fun/badge/news-image-20261119/ahh955/News-image-19/reward.svg)](https://make.fun/bounty/news-image-20261119)

# Thursday 19 November 2026 — The World in One Day

A dense one-page newspaper front page summing up 19 November 2026's world
news in a single 1024×1024 image: **31 stories, every continent, all from
this one day**.

## What is on the page

- **Masthead + stat strip** — six numbers that define the day: 3 presidents
  at one table, the 9–6 World Court vote, the $81.3bn record IPO, 13 years
  since GTA V, 551,864 Suneung candidates, and Australia's 4.9% jobless rate.
- **Three lead stories**, each with a flat-vector illustration:
  1. Trump, Xi and Putin hold their first three-way summit in Shenzhen and
     sign a "Declaration on Peace" on nuclear risk.
  2. The World Court rules 9–6 that Myanmar committed genocide against the
     Rohingya and orders reparations.
  3. COP31's draft text drops fossil fuels; the $120bn adaptation-aid goal
     is still open.
- **Ten numbered stories** — Cyclone Akvan, Anthropic's Nasdaq debut,
  GTA VI's worldwide launch, the Kerch bridge strike, Houthi missiles over
  Riyadh, Korea's Suneung exam, Colombia's national strike, Australia's
  jobless rate, ex-PM Han's acquittal, and Denmark's 109–0 Arctic pact vote.
- **A world map** with numbered pins matching stories 1–13, plus 18 more
  one-line briefs from Rome to Tonga to deep space.
- **A DATE CHECK box** listing stories deliberately left out because they
  are not 19 November news: the EU's €45bn Ukraine loan plan, Voyager 1's
  one-light-day milestone and Iran firing on Kuwait and Bahrain (18 Nov),
  and the US strikes on Iran's Qeshm Island (17 Nov).

Every story is attributed to its source (Reuters, AP, AFP, BBC, Al Jazeera,
UN News, Euronews, ABC, RNZ, Xinhua, Nature). All pictures and the map are
original, drawn in code — no photographs.

## How it is built

`compose.py` draws the whole page procedurally with PIL (DejaVu fonts) and
is deterministic: running it twice produces a byte-identical `entry.png`
(80 KB palette PNG). `main.ts` (Node 22 stdlib only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR` (default `/output`).

```sh
python3 compose.py   # regenerates entry.png
```

## License

MIT — see [LICENSE](LICENSE).
