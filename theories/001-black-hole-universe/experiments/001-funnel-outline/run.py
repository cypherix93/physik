# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy", "sympy", "astropy", "matplotlib"]
# ///
"""Experiment 001: funnel outline. Question, prediction and kill conditions are in README.md.

Compares the expansion history of a time-flipped black hole interior (empty and
matter-filled) with the measured expansion history of our universe.

Units inside the maths: c = 1, and time is counted in Hubble times (1 / H0) once a
model has been matched to today's size and expansion rate.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from astropy import units as u
from astropy.cosmology import Planck18
from scipy.integrate import cumulative_trapezoid, quad
from scipy.optimize import brentq

RESULTS = Path(__file__).parent / "results"
checks: list[dict] = []


def check(name: str, got: float, want: float, tol: float) -> None:
    """Record a calibration check and stop the run if it fails."""
    got, want = float(got), float(want)
    ok = bool(abs(got - want) <= tol)
    checks.append({"check": name, "got": got, "expected": want, "tolerance": tol, "pass": ok})
    if not ok:
        raise SystemExit(f"CALIBRATION FAILED: {name}: got {got}, expected {want} (tol {tol})")


def check_true(name: str, ok: bool) -> None:
    checks.append({"check": name, "pass": bool(ok)})
    if not ok:
        raise SystemExit(f"CALIBRATION FAILED: {name}")


# --------------------------------------------------------------------------
# Symbolic part: get the equations from the geometry, not from memory
# --------------------------------------------------------------------------

def christoffel(g: sp.Matrix, x: list) -> list:
    ginv, n = g.inv(), len(x)
    return [[[sum(ginv[m, l] * (sp.diff(g[l, j], x[k]) + sp.diff(g[l, k], x[j]) - sp.diff(g[j, k], x[l]))
                  for l in range(n)) / 2
              for k in range(n)] for j in range(n)] for m in range(n)]


def ricci(g: sp.Matrix, x: list) -> sp.Matrix:
    G, n = christoffel(g, x), len(x)
    R = sp.zeros(n, n)
    for j in range(n):
        for k in range(n):
            R[j, k] = sum(
                sp.diff(G[m][j][k], x[m]) - sp.diff(G[m][j][m], x[k])
                + sum(G[m][m][l] * G[l][j][k] - G[m][k][l] * G[l][j][m] for l in range(n))
                for m in range(n))
    return R.applyfunc(sp.simplify)


def einstein_mixed(g: sp.Matrix, x: list) -> sp.Matrix:
    R = ricci(g, x)
    ginv = g.inv()
    scalar = sp.simplify(sum(ginv[i, j] * R[i, j] for i in range(len(x)) for j in range(len(x))))
    return (ginv * (R - g * scalar / 2)).applyfunc(sp.simplify)


def symbolic_empty_black_hole() -> dict:
    """Inside the horizon of an empty (Schwarzschild) black hole, r is the time coordinate."""
    r, rs, th, ph, t = sp.symbols("r r_s theta phi t", positive=True)
    f = rs / r - 1  # positive inside the horizon
    coords = [r, t, th, ph]
    g = sp.diag(-1 / f, f, r**2, r**2 * sp.sin(th) ** 2)

    # 1. It really is empty space: every component of the Ricci tensor vanishes.
    check_true("empty black hole interior solves the vacuum equations (Ricci = 0)",
               ricci(g, coords) == sp.zeros(4, 4))

    # 2. Observers who sit at fixed t, theta, phi are in free fall, so their clocks
    #    are a fair definition of "time since the beginning".
    G = christoffel(g, coords)
    uvec = [sp.sqrt(f), 0, 0, 0]
    accel = [sp.simplify(sum(uvec[n] * sp.diff(uvec[m], coords[n]) for n in range(4))
                         + sum(G[m][a][b] * uvec[a] * uvec[b] for a in range(4) for b in range(4)))
             for m in range(4)]
    check_true("fixed-position observers inside are in free fall (zero acceleration)",
               all(a == 0 for a in accel))

    # 3. Expansion measures, with x = r / r_s and d/d(clock time) = sqrt(1/x - 1) d/dx.
    x = sp.symbols("x", positive=True)
    fx = 1 / x - 1
    ddT = lambda F: sp.sqrt(fx) * sp.diff(F, x)  # noqa: E731
    b = x                    # scale of the two directions that follow the radius
    a_par = sp.sqrt(fx)      # scale of the third direction
    a_bar = (b**2 * a_par) ** sp.Rational(1, 3)  # volume-averaged scale

    q_perp = sp.simplify(-ddT(ddT(b)) * b / ddT(b) ** 2)
    evenness = sp.simplify((ddT(a_par) / a_par) / (ddT(b) / b))
    acc_avg = sp.simplify(ddT(ddT(a_bar)) / a_bar)

    check_true("symbolic q for the empty black hole equals 1 / (2 (1 - x))",
               sp.simplify(q_perp - 1 / (2 * (1 - x))) == 0)
    check_true("symbolic evenness ratio equals -1 / (2 (1 - x))",
               sp.simplify(evenness + 1 / (2 * (1 - x))) == 0)

    return {"x": x, "q_perp": q_perp, "evenness": evenness, "acc_avg": acc_avg}


def symbolic_matter_filled() -> None:
    """A uniform ball of pressureless matter: the inside is a Friedmann universe (Oppenheimer-Snyder)."""
    t, chi, th, ph = sp.symbols("t chi theta phi", positive=True)
    a = sp.Function("a")(t)
    coords = [t, chi, th, ph]
    for k, S in ((1, sp.sin(chi)), (0, chi), (-1, sp.sinh(chi))):
        g = sp.diag(-1, a**2, a**2 * S**2, a**2 * S**2 * sp.sin(th) ** 2)
        E = einstein_mixed(g, coords)
        ad, add = sp.diff(a, t), sp.diff(a, t, 2)
        # Zero pressure means the space-space part of the Einstein tensor vanishes:
        #   2 a a'' + a'^2 + k = 0, which gives q = (1 + k / a'^2) / 2.
        check_true(f"matter-filled, k={k:+d}: pressure equation is 2 a a'' + a'^2 + k = 0",
                   sp.simplify(E[1, 1] + (2 * a * add + ad**2 + k) / a**2) == 0)
        check_true(f"matter-filled, k={k:+d}: density equation is 3 (a'^2 + k) / a^2",
                   sp.simplify(E[0, 0] + 3 * (ad**2 + k) / a**2) == 0)


# --------------------------------------------------------------------------
# Numeric part
# --------------------------------------------------------------------------

def measured_universe() -> dict:
    """The standard model with Planck 2018 parameters, standing in for the data."""
    cosmo = Planck18
    hubble_time = (1 / cosmo.H0).to(u.Gyr).value
    E = lambda a: cosmo.efunc(1 / np.asarray(a) - 1)  # noqa: E731  H(a) / H0

    ln_a = np.linspace(np.log(1e-7), np.log(12.0), 400_001)
    a = np.exp(ln_a)
    Ea = E(a)
    # dt = d(ln a) / (H0 E). The sliver before a = 1e-7 is radiation-era: t = 1 / (2 H).
    t = 1 / (2 * Ea[0]) + cumulative_trapezoid(1 / Ea, ln_a, initial=0)
    q = -1 - np.gradient(np.log(Ea), ln_a)

    age = float(np.interp(0.0, ln_a, t)) * hubble_time
    check("measured universe: age from our integrator vs astropy (Gyr)",
          age, cosmo.age(0).to(u.Gyr).value, 0.005)

    q0 = float(np.interp(0.0, ln_a, q))
    Om, Ode = cosmo.Om0, cosmo.Ode0
    check("measured universe: q today vs textbook formula Om/2 + Or - OL",
          q0, Om / 2 + (1 - Om - Ode) - Ode, 2e-3)

    i = np.where((q[:-1] > 0) & (q[1:] <= 0))[0][0]
    ln_a_acc = np.interp(0.0, [q[i + 1], q[i]], [ln_a[i + 1], ln_a[i]])
    a_acc = float(np.exp(ln_a_acc))
    check("measured universe: redshift where speeding-up began vs (2 OL / Om)^(1/3) - 1",
          1 / a_acc - 1, (2 * Ode / Om) ** (1 / 3) - 1, 5e-3)
    t_acc = float(np.interp(ln_a_acc, ln_a, t)) * hubble_time

    return {
        "parameter_set": "astropy.cosmology.Planck18",
        "H0_km_s_Mpc": cosmo.H0.value, "hubble_time_Gyr": hubble_time,
        "age_Gyr": age, "q_today": q0, "H0_times_age": age / hubble_time,
        "speeding_up_since_size": a_acc, "speeding_up_since_redshift": 1 / a_acc - 1,
        "speeding_up_since_Gyr_ago": age - t_acc,
        "q_min": float(q.min()), "q_max": float(q.max()),
        "_a": a, "_t_Gyr": t * hubble_time, "_q": q,
    }


def dust_age(omega: float, a_end: float = 1.0) -> float:
    """Clock time, in Hubble times, for a matter-only model to grow from 0 to a_end.

    The model is matched to today: size 1 and expansion rate 1 at a = 1.
    omega > 1 is the bound ball (closed), 1 the marginal one (flat), < 1 the unbound one (open).
    """
    # Substituting a = s^2 removes the square-root blow-up at the start.
    return quad(lambda s: 2 * s**2 / np.sqrt(omega + (1 - omega) * s**2), 0, np.sqrt(a_end))[0]


def dust_q(a, omega: float):
    return omega / (2 * (omega + (1 - omega) * np.asarray(a)))


def dust_age_closed_form(omega: float) -> float:
    if omega == 1:
        return 2 / 3
    if omega > 1:
        eta = np.arccos((2 - omega) / omega)
        return omega / (2 * (omega - 1) ** 1.5) * (eta - np.sin(eta))
    eta = np.arccosh((2 - omega) / omega)
    return omega / (2 * (1 - omega) ** 1.5) * (np.sinh(eta) - eta)


def matter_filled(hubble_time: float) -> dict:
    for om in (0.3, 1.0, 2.0, 5.0):
        check(f"matter-filled, omega={om}: numeric age vs textbook closed form (Hubble times)",
              dust_age(om), dust_age_closed_form(om), 1e-8)

    # Scan every variant over its whole history for the smallest q.
    worst = np.inf
    for om in np.logspace(-3, 2, 501):
        a_top = om / (om - 1) * (1 - 1e-9) if om > 1 else 1e6
        worst = min(worst, float(dust_q(np.geomspace(1e-9, a_top, 4001), om).min()))

    def row(om, label):
        a_top = om / (om - 1) if om > 1 else "no limit"
        return {"variant": label, "omega": om,
                "q_start": 0.5, "q_today": float(dust_q(1.0, om)),
                "q_far_future": ("grows without limit" if om > 1 else float(dust_q(1e12, om))),
                "largest_size_reached": a_top,
                "implied_age_Gyr": dust_age(om) * hubble_time}

    return {
        "smallest_q_over_all_variants_and_all_time": worst,
        "ever_speeds_up": bool(worst < 0),
        "evenness_ratio": 1.0,
        "examples": [row(2.0, "ball that started at rest (bound)"),
                     row(1.0, "ball that fell from far away (marginal)"),
                     row(0.3, "ball that fell with extra speed (unbound)")],
    }


def empty_black_hole(sym: dict, hubble_time: float) -> dict:
    x = sym["x"]
    q_perp = sp.lambdify(x, sym["q_perp"], "numpy")
    evenness = sp.lambdify(x, sym["evenness"], "numpy")
    acc_avg = sp.lambdify(x, sym["acc_avg"], "numpy")
    xs = np.linspace(1e-6, 1 - 1e-6, 400_001)

    # Clock time from the singularity to radius x, in units of r_s / c.
    T = lambda xe: quad(lambda s: 2 * s**2 / np.sqrt(1 - s**2), 0, np.sqrt(xe))[0]  # noqa: E731
    for xe in (0.1, 0.5, 0.9):
        check(f"empty black hole: numeric clock time to x={xe} vs cycloid formula",
              T(xe), np.arcsin(np.sqrt(xe)) - np.sqrt(xe * (1 - xe)), 1e-9)
    check("empty black hole: lifetime from singularity to horizon vs pi/2 (units r_s / c)",
          T(1.0), np.pi / 2, 1e-8)

    # Finite-difference spot check of the symbolic q, straight from the outline x(T).
    for xe in (0.2, 0.5, 0.8):
        h = 1e-4
        Tm, T0, Tp = T(xe - h), T(xe), T(xe + h)
        d1 = 2 * h / (Tp - Tm)
        d2 = 2 * (h / (Tp - T0) - h / (T0 - Tm)) / (Tp - Tm)
        check(f"empty black hole: q at x={xe}, finite differences vs symbolic",
              -d2 * xe / d1**2, float(q_perp(xe)), 1e-4)

    # The two radius-following directions trace the same curve as the bound matter-filled ball.
    x0 = 0.5
    H0 = np.sqrt(1 / x0 - 1) / x0
    om = 1 / (1 - x0)
    gap = max(abs((T(x0 * a) - T(x0)) * H0 - (dust_age(om, a) - dust_age(om)))
              for a in np.linspace(0.05, 1.95, 39))
    check("empty black hole outline equals bound matter-filled outline (max gap, Hubble times)",
          gap, 0.0, 1e-8)

    ev = evenness(xs)
    return {
        "q_min": float(q_perp(xs).min()), "q_at_start": float(q_perp(xs[0])),
        "q_at_horizon": "grows without limit",
        "ever_speeds_up": bool(q_perp(xs).min() < 0),
        "volume_average_ever_speeds_up": bool(acc_avg(xs).max() > 0),
        "evenness_ratio_closest_to_1": float(ev.max()),
        "evenness_ratio_range": [float(ev.min()), float(ev.max())],
        "third_direction": "shrinks throughout while the other two grow",
        "lifetime_in_units_of_rs_over_c": T(1.0),
        "example_today_halfway_to_horizon": {
            "implied_age_Gyr": T(x0) * H0 * hubble_time,
            "time_left_until_horizon_Gyr": (T(1.0) - T(x0)) * H0 * hubble_time,
        },
    }


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------

SURFACE, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"


def style(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)
    ax.tick_params(colors=MUTED, labelsize=9, length=3)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)


def outlines(meas: dict, hubble_time: float):
    """Each history drawn as the funnel the theory pictures: time runs upward, width is size."""
    t_lo, t_hi, half = -19.0, 40.0, 6.0

    def flat():
        age = 2 / 3 * hubble_time
        t = np.linspace(0, age + t_hi, 3000)
        return t - age, (t / age) ** (2 / 3), age

    def bound(om=2.0):
        eta = np.linspace(0, np.pi, 3000)
        a = om / (om - 1) / 2 * (1 - np.cos(eta))
        t = om / (2 * (om - 1) ** 1.5) * (eta - np.sin(eta)) * hubble_time
        age = dust_age(om) * hubble_time
        return t - age, a, age

    panels = [
        ("Measured universe", "slows down at first,\nthen speeds up", BLUE,
         (meas["_t_Gyr"] - meas["age_Gyr"], meas["_a"], meas["age_Gyr"])),
        ("Black hole, matter-filled", "ball that fell from far away:\nalways slowing down", ORANGE, flat()),
        ("Black hole, empty", "also the matter-filled ball that\nstarted at rest: slows to a halt", AQUA, bound()),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(11.5, 7.2), sharey=True, facecolor=SURFACE)
    for ax, (title, sub, color, (t, a, age)) in zip(axes, panels):
        style(ax)
        keep = (t <= t_hi) & (a <= half * 1.02)
        t, a = t[keep], a[keep]
        ax.fill_betweenx(t, -a, a, color=color, alpha=0.12, linewidth=0)
        ax.plot(a, t, color=color, linewidth=2)
        ax.plot(-a, t, color=color, linewidth=2)
        ax.axhline(0, color=MUTED, linewidth=0.9, linestyle=(0, (4, 3)))
        ax.plot([0], [-age], marker="o", markersize=6, color=color,
                markeredgecolor=SURFACE, markeredgewidth=1.5, zorder=5)
        ax.annotate(f"begins {age:.1f} billion\nyears ago", (0, -age), xytext=(12, -2),
                    textcoords="offset points", fontsize=9, color=INK2, va="center")
        ax.set_title(title, loc="left", fontsize=12, color=INK, fontweight="bold", pad=34)
        ax.text(0, 1.02, sub, transform=ax.transAxes, fontsize=9.5, color=INK2, va="bottom")
        ax.set_xlim(-half, half)
        ax.set_ylim(t_lo, t_hi)
        ax.set_xticks([-4, -2, 0, 2, 4], ["4", "2", "0", "2", "4"])
        ax.set_xlabel("size of the universe (today = 1)", fontsize=9.5, color=INK2)

    axes[0].set_ylabel("billions of years from today", fontsize=9.5, color=INK2)
    axes[0].text(-half + 0.2, 0.8, "today", fontsize=9, color=INK2, va="bottom")
    axes[0].annotate("speeding up since\n" f"{meas['speeding_up_since_Gyr_ago']:.1f} billion years ago",
                     (meas["speeding_up_since_size"], -meas["speeding_up_since_Gyr_ago"]),
                     xytext=(2.0, -5.5), fontsize=9, color=INK2, va="center",
                     arrowprops={"arrowstyle": "-", "color": MUTED, "linewidth": 0.8})
    axes[2].text(2.35, 36.0, "stops growing\nat twice\ntoday's size", fontsize=9, color=INK2, va="top")
    fig.suptitle("Only the measured universe flares at the mouth", x=0.065, ha="left",
                 fontsize=15, color=INK, fontweight="bold", y=0.985)
    fig.tight_layout(rect=(0, 0, 1, 0.95), w_pad=2.0)
    fig.savefig(RESULTS / "outlines.png", dpi=160, facecolor=SURFACE)
    plt.close(fig)


def flare(meas: dict):
    """The deceleration parameter q against size: below zero means speeding up."""
    fig, ax = plt.subplots(figsize=(10, 5.8), facecolor=SURFACE)
    style(ax)
    lo, hi = 0.02, 10.0
    a = np.geomspace(lo, hi, 2000)
    m = (meas["_a"] >= lo) & (meas["_a"] <= hi)
    a_bound = a[a < 1.995]

    ax.axhspan(-1.25, 0, color=BLUE, alpha=0.05, linewidth=0)
    ax.axhline(0, color=AXIS, linewidth=1.2)
    series = [
        ("Measured universe", BLUE, meas["_a"][m], meas["_q"][m], (hi, meas["_q"][m][-1]), "left", (6, 0)),
        ("Black hole, matter-filled: fell from far away", ORANGE, a, dust_q(a, 1.0), (hi, 0.5), "left", (6, 0)),
        ("Black hole, empty (or matter-filled from rest)", AQUA, a_bound, dust_q(a_bound, 2.0),
         (1.75, 1.6), "left", (0, 0)),
        ("Black hole, matter-filled: fell with extra speed", YELLOW, a, dust_q(a, 0.3),
         (hi, float(dust_q(hi, 0.3))), "left", (6, 0)),
    ]
    short = ["measured", "fell from far away", "empty / from rest", "extra speed"]
    for (label, color, xs, ys, at, ha, off), name in zip(series, short):
        ax.plot(xs, ys, color=color, linewidth=2, label=label)
        ax.annotate(name, at, xytext=off, textcoords="offset points", fontsize=9, color=INK2,
                    va="center", ha=ha)
    ax.axvline(1.0, color=MUTED, linewidth=0.9, linestyle=(0, (4, 3)))
    ax.text(1.04, -1.17, "today", fontsize=9, color=INK2, va="bottom")
    ax.text(0.0215, 0.07, "above the line: slowing down", fontsize=9, color=INK2, va="bottom")
    ax.text(0.0215, -0.07, "below the line: speeding up", fontsize=9, color=INK2, va="top")

    ax.set_xscale("log")
    ax.set_xlim(lo, hi * 3.4)
    ax.set_ylim(-1.25, 2.4)
    ax.set_xticks([0.03, 0.1, 0.3, 1, 3, 10], ["0.03", "0.1", "0.3", "1", "3", "10"])
    ax.minorticks_off()
    ax.set_xlabel("size of the universe (today = 1)", fontsize=9.5, color=INK2)
    ax.set_ylabel("deceleration parameter q", fontsize=9.5, color=INK2)
    ax.set_title("No black hole outline ever dips below the line", loc="left", fontsize=14,
                 color=INK, fontweight="bold", pad=12)
    leg = ax.legend(loc="upper left", fontsize=9, frameon=False, labelcolor=INK2,
                    bbox_to_anchor=(0.0, 1.0))
    for line in leg.get_lines():
        line.set_linewidth(2.5)
    fig.tight_layout()
    fig.savefig(RESULTS / "flare.png", dpi=160, facecolor=SURFACE)
    plt.close(fig)


# --------------------------------------------------------------------------

def main() -> None:
    RESULTS.mkdir(exist_ok=True)

    sym = symbolic_empty_black_hole()
    symbolic_matter_filled()
    meas = measured_universe()
    tH = meas["hubble_time_Gyr"]
    filled = matter_filled(tH)
    empty = empty_black_hole(sym, tH)

    verdicts = {
        "empty_black_hole": {
            "K1_flare": "FAILS" if not empty["ever_speeds_up"] else "passes",
            "K2_evenness": "FAILS" if abs(empty["evenness_ratio_closest_to_1"] - 1) > 0.01 else "passes",
        },
        "matter_filled_black_hole": {
            "K1_flare": "FAILS" if not filled["ever_speeds_up"] else "passes",
            "K2_evenness": "FAILS" if abs(filled["evenness_ratio"] - 1) > 0.01 else "passes",
        },
    }

    outlines(meas, tH)
    flare(meas)

    summary = {
        "measured_universe": {k: v for k, v in meas.items() if not k.startswith("_")},
        "empty_black_hole": empty,
        "matter_filled_black_hole": filled,
        "verdicts": verdicts,
        "calibration_checks": checks,
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"{len(checks)} calibration checks passed")
    print(json.dumps({k: summary[k] for k in summary if k != "calibration_checks"}, indent=2))


if __name__ == "__main__":
    main()
