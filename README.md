# physik

> physics, but spelled by someone who is not qualified to do it

A lab for stress-testing big physics ideas without a PhD. One human with theories, one AI with a calculator, and a rule that says we write down how an idea could die *before* we run the test.

The goal is not to prove anything to the world. The goal is to take an idea, break it into claims small enough to check, and find out quickly whether each one has ground to walk on. Killing a theory counts as a win: it frees us up for the next one.

## How it works

Every theory gets its own workspace under `theories/`. Inside it:

| File | What it is |
|------|------------|
| `README.md` | The theory card: the idea in plain words, the claims it breaks down into, and where each claim stands |
| `journal.md` | The running story: what we thought, what we tried, what changed our minds. Append-only |
| `experiments/` | One folder per test. Each states its question, its prediction, and its kill condition before any code runs |

Experiments are self-contained. One might be forty lines of Python, another a symbolic tensor calculation, another a fit against public survey data. Each carries its own dependencies and its own instructions, so they never fight over tooling.

## Theories

| # | Theory | Status |
|---|--------|--------|
| 001 | [Our universe is inside a black hole](theories/001-black-hole-universe/) | open |

Statuses: **open** (still being broken into claims) · **standing** (has survived the tests so far) · **wounded** (a claim failed; the theory needs changing to survive) · **dead** (a core claim failed and no honest repair exists) · **parked** (not testable with what we have).

## Running things

Python experiments use [uv](https://docs.astral.sh/uv/) with dependencies declared at the top of each script, so there is nothing to install up front:

```
uv run theories/001-black-hole-universe/experiments/001-some-test/run.py
```

Anything that needs a different toolkit says so in its own README.

## Starting a new theory

Copy `templates/theory/` to `theories/NNN-short-name/`, write the idea down in your own words, and add a row to the table above. See `CLAUDE.md` for the ground rules the lab runs on.
