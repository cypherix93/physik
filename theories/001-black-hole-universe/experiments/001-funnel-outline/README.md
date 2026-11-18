# Experiment 001: funnel outline

**Tests claim:** C3 of [theory 001](../../README.md), with a side check on C1
**Status:** planned
**Date:** 2026-11-17

## Question

Does the inside of a black hole, flipped in time, grow the way our universe has grown: slowing down at first, then speeding up?

## Background in one paragraph

The theory pictures the universe as the wall of a funnel, with depth as time. The width of the funnel at each depth is the size of the universe at that time, so the funnel's outline is the expansion history. Claim C3 says the funnel flares toward the mouth, and that this flare is the accelerating expansion astronomers measure. General relativity gives a definite outline for a black hole's inside, so we can draw it and compare.

## The outlines being compared

| Name | What it is |
|------|------------|
| Measured universe | The expansion history that fits the observations: the standard model with the Planck 2018 parameter set, taken from `astropy`. This stands in for the data |
| Empty black hole | The inside of a black hole with nothing in it (the Schwarzschild solution), run backwards in time. Space here has two directions that follow the radius and a third that behaves differently |
| Matter-filled black hole | The inside of a collapsing ball of pressureless matter (the Oppenheimer–Snyder model), run backwards in time. Three variants, depending on whether the ball started at rest, fell from far away, or fell with extra speed |

## Measures

- **Flare.** The deceleration parameter q, which is positive when expansion is slowing and negative when it is speeding up. The measured universe has q below zero today.
- **Evenness.** The expansion rate along the odd direction divided by the rate along the other two. An even expansion gives exactly 1. Our universe is even to far better than 1%.
- **Implied age.** How old each model says the universe is, once it is matched to today's measured expansion rate. Recorded for interest; not a kill condition.

## Prediction

Written before any code was run.

If C3 is true, at least one black hole outline has a stretch where q is negative, following a stretch where it is positive.

Claude's own expectation, recorded so it can be held to account: no version will show this. The reason is a general result in relativity, that ordinary matter and empty space can only slow an expansion down. By-hand working (journal, 2026-11-17 entry 2) gives q of at least 1/2 for the empty black hole and for two of the matter-filled variants, and between 0 and 1/2 for the third. Claude also expects the empty black hole's odd direction to shrink while the other two grow.

## Kill conditions

Written before any code was run.

- **K1, flare.** A version is ruled out as the source of the acceleration if q is never negative anywhere in its history. This does not depend on the black hole's size or on where "today" sits in the funnel, so no tuning can save a version that fails it.
- **K2, evenness.** A version is ruled out as a description of our universe if its evenness ratio is further than 1% from 1 at every point in its history.

If every version fails K1, claim C3 is refuted in its plain form: a black hole described by standard relativity alone does not produce the flare. The theory would then need an extra ingredient, and the next step is to look at proposals for what that ingredient is.

A single version with a negative-q stretch would count as support for C3 and would be a surprise worth checking hard.

## Method

To be completed when the code is written.

## Calibration

To be completed when the code is written.

## How to run

```
uv run run.py
```

## Result

Not yet run.

## Verdict

Not yet run.
