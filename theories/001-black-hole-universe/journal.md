# Journal: Our universe is inside a black hole

Newest entry at the bottom. Never rewrite old entries; add a new one that corrects them.

## 2026-11-17: the theory lands

The human stated the theory (see the theory card). No experiments yet, on purpose. Claude's opening notes, to be discussed:

**The famous coincidence is not a coincidence.** `[derived]` The usual hook for this theory is that the mass inside the Hubble radius has a Schwarzschild radius equal to the Hubble radius. For a spatially flat universe this is an identity. The Friedmann equation fixes the density of a flat universe at ρ = 3H²/(8πG). Put the mass of a ball of radius r at that density into r_s = 2GM/c² and the result is r_s = H²r³/c². Setting r = c/H gives r_s = c/H exactly. So any flat universe, at any time, passes this test. It cannot count as evidence that ours is special. Assumption: the Schwarzschild formula is being applied to a setting (a universe filled with matter, with no empty space outside) where it was not derived.

**Back-of-envelope sizes.** `[guess]` until run as an experiment. With H₀ near 67.7 km/s/Mpc the Hubble radius is about 14.4 billion light-years. A black hole with that Schwarzschild radius gives an infalling observer at most (π/2)·r_s/c, about 23 billion years, before the singularity. The same order as the universe's age of 13.8 billion years, which follows from both timescales being built from the same GM/c³.

**Three ideas, not one.** Claude split the statement into the edge idea, the inside-out idea, and the inheritance idea (theory card). Waiting on the human to confirm the split and share the deeper version.

**Known difficulties to face early.** `[known]`, sources to be verified in a literature pass:
- Inside a standard black hole the singularity lies in every observer's future, and space squeezes in two directions while stretching in the third. Our universe has its singularity in the past and expands the same in all directions.
- A black hole's horizon is one fixed surface. The cosmic horizon is different for every observer; each galaxy has its own.
- A black hole formed in a parent universe has a centre and probably spin. Our universe shows no centre and very tight limits on overall rotation.

Next: hear the human's fuller version, agree the claims, then pick the first experiment.

## 2026-11-17 (2): the funnel picture

The human gave the fuller version (quoted on the theory card): a black hole drawn as a funnel in a 2D sheet, singularity at the bottom, the wall of the funnel being the universe, flipped in time so the universe begins at the bottom and its future lies toward the mouth. A sketch is coming. Claude's response, all working done by hand and not yet run:

**The funnel drawing is not the black hole's real shape, but reading depth as time is the right repair.** `[known]`, sources unverified. The popular funnel plots gravitational pull, which is why it looks bottomless. The true shape of space around a black hole (Flamm's paraboloid) stops at a throat at the horizon and has no bottom. Inside the horizon the roles swap: the radius stops being a direction you can move in and becomes time. The singularity is a moment, not a place. So "depth is time" (C1) is what general relativity says about the inside.

**Counting dimensions.** `[derived]` If depth is time, a horizontal slice of the funnel is space at one moment. The wall of a funnel drawn in 3D has circles for slices, so it is a universe with one dimension of space. A 2D universe needs spheres for slices, and ours needs 3-spheres. Carried up to our dimension, the picture is a closed universe that starts at a point and grows. That is the standard closed Big Bang model, drawn as a trumpet, with the outline of the trumpet being the size of the universe over time. So the picture alone is not new. What would be new is the black hole dictating the outline.

**What outline does a black hole give?** `[derived]` For an empty black hole flipped in time, the radius r of the spheres grows with clock time τ as dr/dτ = c·sqrt(r_s/r − 1). Early on that gives r growing as τ^(2/3), the same law as our universe's matter era. After that it slows down and stops at the horizon, at τ = (π/2)·r_s/c. Meanwhile the third direction of space shrinks. So the plain version of C3 fails twice: expansion slows toward the mouth instead of speeding up, and it is not the same in all directions.

**Possible rescue.** `[known]`, unverified. A black hole filled with matter (Oppenheimer–Snyder) has an inside that expands evenly in all directions. Gaztañaga argues that in such a model the horizon acts like dark energy. That is C3 in professional form and the first thing to look up.

**Eating versus spitting.** `[known]` A time-flipped black hole is a white hole: things come out and nothing goes in. C4 (the parent feeds, the inside gains future) needs the black hole not flipped. The toy version does have the right flavour: the inside's total lifetime is (π/2)·r_s/c, which is proportional to the mass.

**Mass and area.** `[known]` Mass is proportional to radius, so area goes as mass squared. What is proportional to area is entropy, the amount of information a black hole can hold (Bekenstein–Hawking). That is the root of the holographic principle, which says a region's information fits on its boundary, one dimension down. The human's picture keeps the same number of dimensions, so the two ideas are different and C6 needs restating.

**Proposed first experiment (not built).** Plot the black hole outline against the measured expansion history of our universe and see whether any version of the funnel flares the way the data does.

## 2026-11-17 (3): first experiment, the funnel outline

The human confirmed Claude's reading of the picture and asked for the first test. They also said the standard model and the holographic principle are close to their heart, so overlap with those is welcome.

[Experiment 001](experiments/001-funnel-outline/) compared the expansion history of a time-flipped black hole interior with the measured one. The prediction and kill conditions were committed before any code existed (commit 2807d7a).

**Result.** `[numeric]` No black hole outline ever speeds up. The empty black hole and two of the matter-filled variants have a deceleration parameter of at least 0.5 throughout; the third stays above zero. The measured universe has been speeding up for 6.1 billion years and sits at −0.53 today. The empty black hole also grows unevenly: one direction of space shrinks while the other two grow. All 25 calibration checks passed.

**What it means.** C3 is refuted in its plain form, and the theory moves from open to wounded. The black hole's shape is not what makes the expansion accelerate, as long as only standard relativity and ordinary matter are involved. This was Claude's expectation going in, so the test confirmed a known piece of physics more than it discovered anything.

**What survived.** C1 came out partly supported: inside an empty black hole the radius does act as time, free-falling clocks do start at the singularity, and the early growth follows the same law as our universe's matter era.

**The pointer.** `[derived]` In the matter-filled version the equations for the inside do not contain the horizon at all. The inside cannot feel how near the mouth is. So the surviving form of C3 is: something beyond standard relativity links the horizon to the expansion inside. That is where the holographic principle could enter the theory.

**Side findings.** The empty black hole's outline is exactly the outline of a matter-filled ball that started at rest. Every black hole outline implies a universe younger than 13.8 billion years (8.2 to 11.7 in the examples run).

Next: a literature pass on proposals that tie dark energy to a horizon, then a second experiment testing one such rule against the measured expansion history.
