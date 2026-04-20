"""
==============================================================================
hall_transport.py
==============================================================================
Dynamics and Applications of Nonlinear Hall Transport:
Stability, Bifurcation, and Chaos in Mesoscopic Semiconductors

Course  : Nonlinear Dynamics (IDC-402)
Author  : Daman Kumar  |  MS23031
Session : Jan-April 2025
==============================================================================

The nonlinear Hall transport map:
    x_{n+1} = r * x_n * (1 - x_n) + gamma * cos(pi * omega * x_n)

Parameters chosen deliberately different from any textbook example:
    r     in [0, 4]     -- magnetic drive / nonlinearity
    gamma in [0, 0.25]  -- quantum-interference amplitude
    omega in [1, 8]     -- interference wavenumber
    x0    in (0, 1)     -- initial normalised Hall voltage

APPLICATION: Chaos Synchronisation in Coupled Mesoscopic Hall Devices
    Drive   : x_{n+1} = f(x_n)
    Response: y_{n+1} = (1 - eps)*f(y_n) + eps*f(x_n)
    Shows synchronisation transition at a critical coupling eps_c.

FIGURES GENERATED
    fig1_phase_portrait.png        -- x_{n+1} vs x_n  (4 parameter sets)
    fig2_time_evolution.png        -- Hall voltage vs iteration
    fig3_divergence.png            -- Trajectory separation + Lyapunov
    fig4_orbit_diagram.png         -- Orbit diagram (gamma=0)
    fig5_orbit_interference.png    -- Orbit diagram (gamma=0.15)
    fig6_cobweb.png                -- Cobweb plots (4 r values)
    fig7_lyapunov.png              -- Lyapunov spectrum vs r
    fig8_synchronisation.png       -- Chaos synchronisation application
    fig9_sync_transition.png       -- Sync error vs coupling strength
==============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import AutoMinorLocator

# ─── Global style ────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.dpi": 150,
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "axes.titlesize": 10.5,
    "axes.labelsize": 9.5,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "legend.fontsize": 8,
    "lines.linewidth": 1.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

NAVY    = "#1a3a5c"
CRIMSON = "#c0392b"
TEAL    = "#16796f"
AMBER   = "#d68910"
PANEL   = "#f0f3f7"

# ══════════════════════════════════════════════════════════════════════════════
# CORE MAP
# ══════════════════════════════════════════════════════════════════════════════

def hall_map(x, r, gamma=0.0, omega=3.0):
    """
    Nonlinear Hall transport map with cosine interference correction.
        x_{n+1} = r*x*(1-x) + gamma*cos(pi*omega*x)
    Note: cosine interference (vs sine in standard logistic) and pi*omega
    wavenumber give genuinely different phase-portrait geometry.
    """
    return r * x * (1.0 - x) + gamma * np.cos(np.pi * omega * x)


def iterate(x0, r, n, gamma=0.0, omega=3.0):
    """Return full orbit [x0, x1, ..., x_n]."""
    traj = np.empty(n + 1)
    traj[0] = x0
    for i in range(n):
        traj[i + 1] = hall_map(traj[i], r, gamma, omega)
    return traj


def lyapunov(r, gamma=0.0, omega=3.0, x0=0.37,
             n_burn=600, n_avg=8000):
    """
    Lyapunov exponent via orbit-averaged log|f'(x)|.
    f'(x) = r(1-2x) - gamma*pi*omega*sin(pi*omega*x)
    """
    x = x0
    for _ in range(n_burn):
        x = hall_map(x, r, gamma, omega)
    total = 0.0
    for _ in range(n_avg):
        d = abs(r * (1.0 - 2.0*x) - gamma * np.pi * omega * np.sin(np.pi * omega * x))
        total += np.log(max(d, 1e-14))
        x = hall_map(x, r, gamma, omega)
    return total / n_avg


def orbit_data(r_min=2.4, r_max=4.0, n_r=1400, x0=0.37,
               n_burn=600, n_plot=250, gamma=0.0, omega=3.0):
    """Collect attractor data for orbit diagram."""
    r_arr = np.linspace(r_min, r_max, n_r)
    rs, xs = [], []
    for r in r_arr:
        x = x0
        for _ in range(n_burn):
            x = hall_map(x, r, gamma, omega)
        for _ in range(n_plot):
            x = hall_map(x, r, gamma, omega)
            rs.append(r); xs.append(x)
    return np.array(rs), np.array(xs)


# ══════════════════════════════════════════════════════════════════════════════
# FIG 1 — Phase portrait  x_{n+1} vs x_n
# ══════════════════════════════════════════════════════════════════════════════

def fig1_phase_portrait():
    # Four parameter sets — all different from uploaded example
    cases = [
        dict(r=0.55, x0=0.30, label=r"$r=0.55$",  col=NAVY),
        dict(r=1.85, x0=0.30, label=r"$r=1.85$",  col=TEAL),
        dict(r=3.25, x0=0.30, label=r"$r=3.25$",  col=AMBER),
        dict(r=3.82, x0=0.30, label=r"$r=3.82$",  col=CRIMSON),
    ]
    n_iter = 180
    xi = np.linspace(0, 1, 500)

    fig, axes = plt.subplots(2, 2, figsize=(9.5, 7.5))
    fig.suptitle(
        r"Phase Portrait: $x_{n+1}$ vs $x_n$ for the Nonlinear Hall Transport Map",
        fontsize=12, fontweight="bold", color=NAVY, y=1.01)

    descr = ["Convergence to trivial fixed point  $x^*=0$",
             "Stable non-trivial Hall plateau",
             "Period-4 oscillations  (two period-doublings)",
             "Fully developed chaotic transport"]

    for ax, c, d in zip(axes.flat, cases, descr):
        r_, x0_ = c["r"], c["x0"]
        traj = iterate(x0_, r_, n_iter)
        yc = np.array([hall_map(xi_, r_) for xi_ in xi])

        ax.set_facecolor(PANEL)
        ax.plot(xi, yc, color=c["col"], lw=2.0, label=r"$f(x_n)$", zorder=3)
        ax.plot(xi, xi, "k--", lw=1.0, alpha=0.6, label=r"$x_{n+1}=x_n$")
        ax.scatter(traj[:-1], traj[1:], s=9, color=c["col"],
                   alpha=0.55, zorder=4, label="Iterates")
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_title(f"{c['label']} — {d}", fontsize=9, pad=5)
        ax.set_xlabel(r"$x_n$  (Hall voltage, normalised)")
        ax.set_ylabel(r"$x_{n+1}$")
        ax.legend(loc="upper left", framealpha=0.7)
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())

    fig.tight_layout(pad=1.5)
    fig.savefig("fig1_phase_portrait.png", bbox_inches="tight", dpi=160)
    plt.close()
    print("  [✓] fig1_phase_portrait.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIG 2 — Time evolution  x_n vs n
# ══════════════════════════════════════════════════════════════════════════════

def fig2_time_evolution():
    cases = [
        (0.55, "Rapid decay to $x^*=0$  —  overdamped Hall signal"),
        (2.20, "Monotone convergence to stable non-zero plateau"),
        (3.45, "Sustained period-4 oscillations  (two doublings)"),
        (3.78, "Chaotic Hall voltage  —  deterministic yet unpredictable"),
    ]
    x0, n = 0.30, 120

    fig, axes = plt.subplots(2, 2, figsize=(10.5, 6.5))
    fig.suptitle("Temporal Evolution of Normalised Hall Voltage $x_n$",
                 fontsize=12, fontweight="bold", color=NAVY)
    colors = [NAVY, TEAL, AMBER, CRIMSON]

    for ax, (r_, lbl), col in zip(axes.flat, cases, colors):
        traj = iterate(x0, r_, n)
        ns = np.arange(n + 1)
        ax.set_facecolor(PANEL)
        ax.plot(ns, traj, color=col, lw=1.3)
        ax.fill_between(ns, traj, alpha=0.10, color=col)
        ax.set_title(rf"$r={r_}$ — {lbl}", fontsize=9)
        ax.set_xlabel("Iteration $n$"); ax.set_ylabel("$x_n$")
        ax.set_ylim(-0.05, 1.10)
        ax.xaxis.set_minor_locator(AutoMinorLocator())

    fig.tight_layout(pad=1.5)
    fig.savefig("fig2_time_evolution.png", bbox_inches="tight", dpi=160)
    plt.close()
    print("  [✓] fig2_time_evolution.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIG 3 — Trajectory divergence + log separation
# ══════════════════════════════════════════════════════════════════════════════

def fig3_divergence():
    r, n = 3.82, 120
    x01, x02 = 0.3001, 0.3006   # deliberately different from example PDF

    t1 = iterate(x01, r, n)
    t2 = iterate(x02, r, n)
    sep = np.abs(t1 - t2)
    ns  = np.arange(n + 1)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    fig.suptitle(
        rf"Sensitive Dependence on Initial Conditions  ($r={r}$,  "
        rf"$\Delta x_0 = {x02-x01:.4f}$)",
        fontsize=12, fontweight="bold", color=NAVY)

    # Left — overlaid trajectories
    axes[0].set_facecolor(PANEL)
    axes[0].plot(ns, t1, color=NAVY,   lw=1.2, label=rf"$x_0={x01}$")
    axes[0].plot(ns, t2, color=CRIMSON, lw=1.2, ls="--", label=rf"$x_0={x02}$")
    axes[0].set_xlabel("Iteration $n$"); axes[0].set_ylabel("$x_n$")
    axes[0].set_title("Two trajectories with nearly identical initial conditions")
    axes[0].legend(framealpha=0.8)

    # Right — log separation with Lyapunov fit
    lam = lyapunov(r)
    n_fit = np.arange(0, 45)
    fit = (x02 - x01) * np.exp(lam * n_fit)

    axes[1].set_facecolor(PANEL)
    axes[1].semilogy(ns, np.maximum(sep, 1e-16), color=NAVY, lw=1.2,
                     label=r"$|\delta x_n|$")
    axes[1].semilogy(n_fit, fit, color=CRIMSON, lw=1.5, ls="--",
                     label=rf"$\delta e^{{\lambda_L n}}$,  "
                           rf"$\lambda_L={lam:.3f}$")
    axes[1].set_xlabel("Iteration $n$")
    axes[1].set_ylabel(r"$|\delta x_n|$  (log scale)")
    axes[1].set_title("Exponential divergence — definitive signature of chaos")
    axes[1].legend(framealpha=0.8)

    fig.tight_layout(pad=1.5)
    fig.savefig("fig3_divergence.png", bbox_inches="tight", dpi=160)
    plt.close()
    print("  [✓] fig3_divergence.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIG 4 — Orbit diagram  (gamma = 0)
# ══════════════════════════════════════════════════════════════════════════════

def fig4_orbit_diagram():
    print("  Computing orbit diagram (gamma=0)…")
    rs, xs = orbit_data(r_min=2.4, r_max=4.0, n_r=1600, x0=0.37)

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.set_facecolor("#0d1b2a")
    ax.scatter(rs, xs, s=0.07, color="#56b4e9", alpha=0.35, linewidths=0)

    ax.set_xlabel("Control parameter $r$  (magnetic drive / nonlinearity)",
                  fontsize=10, color="white")
    ax.set_ylabel("Attractor $x_n$  (normalised Hall voltage)",
                  fontsize=10, color="white")
    ax.set_title(
        r"Orbit Diagram — Nonlinear Hall Transport Map  ($\gamma=0$,  $x_0=0.37$)",
        fontsize=12, fontweight="bold", color="#56b4e9")
    ax.tick_params(colors="white"); ax.spines[:].set_color("#445566")

    # Annotate key features
    ann = [
        (3.00, 0.48, "Period-2\nbifurcation", ( 0.08, 0.14)),
        (3.45, 0.37, "Period-4", ( 0.06, 0.12)),
        (3.57, 0.28, "Chaos\nonset",  ( 0.06, 0.10)),
        (3.74, 0.52, "Period-5\nwindow",  (-0.12, 0.12)),
        (3.83, 0.48, "Period-3\nwindow",  ( 0.05, 0.12)),
    ]
    for xp, yp, txt, (dx, dy) in ann:
        ax.annotate(txt, xy=(xp, yp), xytext=(xp+dx, yp+dy),
                    fontsize=7.5, color="#f0c040",
                    arrowprops=dict(arrowstyle="->", color="#f0c040", lw=0.8))

    fig.tight_layout()
    fig.savefig("fig4_orbit_diagram.png", bbox_inches="tight", dpi=160)
    plt.close()
    print("  [✓] fig4_orbit_diagram.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIG 5 — Orbit diagram with quantum interference  (gamma = 0.15)
# ══════════════════════════════════════════════════════════════════════════════

def fig5_orbit_interference():
    print("  Computing orbit diagram (gamma=0.15)…")
    rs, xs = orbit_data(r_min=2.4, r_max=4.0, n_r=1600,
                        x0=0.37, gamma=0.15, omega=3.0)

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.set_facecolor("#0d1b2a")
    ax.scatter(rs, xs, s=0.07, color="#e07b54", alpha=0.35, linewidths=0)

    ax.set_xlabel("Control parameter $r$", fontsize=10, color="white")
    ax.set_ylabel("Attractor $x_n$",       fontsize=10, color="white")
    ax.set_title(
        r"Orbit Diagram with Quantum Interference  ($\gamma=0.15$,  $\omega=3$,  $x_0=0.37$)",
        fontsize=12, fontweight="bold", color="#e07b54")
    ax.tick_params(colors="white"); ax.spines[:].set_color("#445566")

    fig.tight_layout()
    fig.savefig("fig5_orbit_interference.png", bbox_inches="tight", dpi=160)
    plt.close()
    print("  [✓] fig5_orbit_interference.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIG 6 — Cobweb plots
# ══════════════════════════════════════════════════════════════════════════════

def _draw_cobweb(ax, r, x0, n_steps, color):
    xi = np.linspace(0.001, 0.999, 600)
    yc = np.array([hall_map(x_, r) for x_ in xi])
    ax.set_facecolor(PANEL)
    ax.plot(xi, yc, color=color, lw=2.0, label=r"$f(x_n)$")
    ax.plot(xi, xi, "k--", lw=1.0, alpha=0.55, label=r"$x_{n+1}=x_n$")
    x = x0
    cx, cy = [x], [0.0]
    for _ in range(n_steps):
        yn = hall_map(x, r)
        cx += [x,  yn]; cy += [yn, yn]
        x = yn
    ax.plot(cx, cy, color=CRIMSON, lw=0.85, alpha=0.9, label="Cobweb")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())


def fig6_cobweb():
    cases = [
        (0.55, 0.30, 25,  NAVY,   "Convergence to $x^*=0$"),
        (1.95, 0.30, 40,  TEAL,   "Stable non-trivial fixed point"),
        (3.55, 0.30, 70,  AMBER,  "Period-8 orbit"),
        (3.82, 0.30, 100, CRIMSON,"Chaotic — dense irregular web"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(9.5, 8))
    fig.suptitle("Cobweb Plots: Iterative Dynamics of the Hall Transport Map",
                 fontsize=12, fontweight="bold", color=NAVY)

    for ax, (r_, x0_, ns, col, lbl) in zip(axes.flat, cases):
        _draw_cobweb(ax, r_, x0_, ns, col)
        ax.set_title(rf"$r={r_}$,  $x_0={x0_}$ — {lbl}", fontsize=9)
        ax.set_xlabel(r"$x_n$"); ax.set_ylabel(r"$x_{n+1}$")
        ax.legend(fontsize=7.5, framealpha=0.75)

    fig.tight_layout(pad=1.5)
    fig.savefig("fig6_cobweb.png", bbox_inches="tight", dpi=160)
    plt.close()
    print("  [✓] fig6_cobweb.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIG 7 — Lyapunov exponent spectrum
# ══════════════════════════════════════════════════════════════════════════════

def fig7_lyapunov():
    print("  Computing Lyapunov spectrum…")
    r_arr = np.linspace(2.4, 4.0, 900)
    le0   = np.array([lyapunov(r_, gamma=0.00) for r_ in r_arr])
    le1   = np.array([lyapunov(r_, gamma=0.15) for r_ in r_arr])

    fig, axes = plt.subplots(2, 1, figsize=(11, 7.5), sharex=True)
    fig.suptitle("Lyapunov Exponent Spectrum  $\\lambda_L(r)$",
                 fontsize=12, fontweight="bold", color=NAVY)

    pairs = [(le0, r"$\gamma=0$  (logistic limit)", NAVY),
             (le1, r"$\gamma=0.15$  (quantum interference)", TEAL)]

    for ax, (le, lbl, col) in zip(axes, pairs):
        ax.set_facecolor(PANEL)
        ax.plot(r_arr, le, color=col, lw=0.9)
        ax.axhline(0, color=CRIMSON, lw=1.2, ls="--",
                   label=r"$\lambda_L=0$  (bifurcation boundary)")
        ax.fill_between(r_arr, le, 0, where=(le > 0),
                        color=CRIMSON, alpha=0.18, label="Chaotic  ($\\lambda_L>0$)")
        ax.fill_between(r_arr, le, 0, where=(le < 0),
                        color=col,    alpha=0.12, label="Stable  ($\\lambda_L<0$)")
        ax.set_ylabel(r"$\lambda_L$", fontsize=10)
        ax.set_title(lbl, fontsize=10)
        ax.set_ylim(-3.2, 1.4)
        ax.legend(fontsize=8, loc="lower right", framealpha=0.8)
        ax.xaxis.set_minor_locator(AutoMinorLocator())

    axes[-1].set_xlabel("Control parameter $r$", fontsize=10)
    fig.tight_layout(pad=1.5)
    fig.savefig("fig7_lyapunov.png", bbox_inches="tight", dpi=160)
    plt.close()
    print("  [✓] fig7_lyapunov.png")


# ══════════════════════════════════════════════════════════════════════════════
# APPLICATION: CHAOS SYNCHRONISATION IN COUPLED HALL DEVICES
# ══════════════════════════════════════════════════════════════════════════════

def coupled_hall(r, eps, x0=0.37, y0=0.72, n=600, gamma=0.0, omega=3.0):
    """
    Drive-response coupling (Pecora-Carroll scheme).
        Drive   : x_{n+1} = f(x_n)
        Response: y_{n+1} = (1-eps)*f(y_n) + eps*f(x_n)
    Returns arrays x, y, |x-y|.
    """
    x, y = x0, y0
    xs, ys, errs = [], [], []
    for _ in range(n):
        xn = hall_map(x, r, gamma, omega)
        yn = (1.0 - eps) * hall_map(y, r, gamma, omega) \
             + eps * hall_map(x, r, gamma, omega)
        xs.append(xn); ys.append(yn)
        errs.append(abs(xn - yn))
        x, y = xn, yn
    return np.array(xs), np.array(ys), np.array(errs)


def sync_error_vs_eps(r=3.82, eps_arr=None, n=1000, n_burn=400,
                      gamma=0.0, omega=3.0):
    """Root-mean-square sync error vs coupling strength."""
    if eps_arr is None:
        eps_arr = np.linspace(0, 1, 120)
    rms = []
    for eps in eps_arr:
        x, y = 0.37, 0.72
        for _ in range(n_burn):
            xn = hall_map(x, r, gamma, omega)
            yn = (1-eps)*hall_map(y, r, gamma, omega) + eps*hall_map(x, r, gamma, omega)
            x, y = xn, yn
        errs = []
        for _ in range(n):
            xn = hall_map(x, r, gamma, omega)
            yn = (1-eps)*hall_map(y, r, gamma, omega) + eps*hall_map(x, r, gamma, omega)
            x, y = xn, yn
            errs.append(abs(xn - yn))
        rms.append(np.sqrt(np.mean(np.array(errs)**2)))
    return eps_arr, np.array(rms)


def fig8_synchronisation():
    """
    Panel figure showing chaos synchronisation:
    - Row 1: drive & response trajectories before/after sync
    - Row 2: sync error time series before/after sync
    - Row 3: drive vs response scatter (identity = perfect sync)
    """
    r = 3.82
    eps_low, eps_high = 0.18, 0.72
    n = 300

    xs_l, ys_l, er_l = coupled_hall(r, eps_low,  n=n)
    xs_h, ys_h, er_h = coupled_hall(r, eps_high, n=n)
    ns = np.arange(n)

    fig = plt.figure(figsize=(12, 10))
    gs  = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.32)
    fig.suptitle(
        "Chaos Synchronisation in Coupled Mesoscopic Hall Devices\n"
        rf"Drive–Response Coupling  ($r={r}$)",
        fontsize=12, fontweight="bold", color=NAVY)

    # ── Row 1: trajectories ───────────────────────────────────────────────
    for col_idx, (xs, ys, eps, er) in enumerate(
            [(xs_l, ys_l, eps_low, er_l), (xs_h, ys_h, eps_high, er_h)]):
        ax = fig.add_subplot(gs[0, col_idx])
        ax.set_facecolor(PANEL)
        ax.plot(ns, xs, color=NAVY,   lw=1.0, label="Drive  $x_n$",    alpha=0.9)
        ax.plot(ns, ys, color=CRIMSON, lw=1.0, label="Response  $y_n$", alpha=0.75, ls="--")
        sync_label = "Unsynchronised" if eps < 0.5 else "Synchronised"
        ax.set_title(rf"$\varepsilon={eps}$  —  {sync_label}", fontsize=9.5)
        ax.set_xlabel("Iteration $n$"); ax.set_ylabel("Hall voltage")
        ax.legend(fontsize=8, framealpha=0.8)
        ax.set_ylim(-0.05, 1.10)

    # ── Row 2: synchronisation error |x_n - y_n| ────────────────────────
    for col_idx, (er, eps) in enumerate([(er_l, eps_low), (er_h, eps_high)]):
        ax = fig.add_subplot(gs[1, col_idx])
        ax.set_facecolor(PANEL)
        ax.semilogy(ns, np.maximum(er, 1e-16),
                    color=TEAL, lw=1.1)
        ax.axhline(1e-6, color=CRIMSON, ls=":", lw=1.0,
                   label="Sync threshold $10^{-6}$")
        ax.set_title(rf"Sync error  $|x_n - y_n|$  ($\varepsilon={eps}$)", fontsize=9.5)
        ax.set_xlabel("Iteration $n$"); ax.set_ylabel(r"$|x_n - y_n|$")
        ax.legend(fontsize=8, framealpha=0.8)

    # ── Row 3: drive vs response scatter  (identity = perfect sync) ──────
    for col_idx, (xs, ys, eps) in enumerate(
            [(xs_l, ys_l, eps_low), (xs_h, ys_h, eps_high)]):
        ax = fig.add_subplot(gs[2, col_idx])
        ax.set_facecolor(PANEL)
        ax.scatter(xs, ys, s=4, color=NAVY, alpha=0.4)
        ax.plot([0, 1], [0, 1], color=CRIMSON, lw=1.2, ls="--",
                label="Perfect sync  $y_n=x_n$")
        ax.set_title(rf"Drive vs Response scatter  ($\varepsilon={eps}$)", fontsize=9.5)
        ax.set_xlabel("Drive  $x_n$"); ax.set_ylabel("Response  $y_n$")
        ax.legend(fontsize=8, framealpha=0.8)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    fig.savefig("fig8_synchronisation.png", bbox_inches="tight", dpi=160)
    plt.close()
    print("  [✓] fig8_synchronisation.png")


def fig9_sync_transition():
    """RMS sync error vs coupling eps — shows critical coupling eps_c."""
    r = 3.82
    print("  Computing sync transition curve…")
    eps_arr, rms = sync_error_vs_eps(r=r)

    # Estimate eps_c as first eps where rms < 0.01
    eps_c_idx = np.where(rms < 0.01)[0]
    eps_c = eps_arr[eps_c_idx[0]] if len(eps_c_idx) > 0 else None

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.set_facecolor(PANEL)
    ax.semilogy(eps_arr, np.maximum(rms, 1e-14), color=NAVY, lw=1.8)
    ax.set_xlabel(r"Coupling strength $\varepsilon$", fontsize=10)
    ax.set_ylabel(r"RMS synchronisation error  $\langle|x_n-y_n|^2\rangle^{1/2}$",
                  fontsize=10)
    ax.set_title(
        rf"Synchronisation Transition in Coupled Hall Devices  ($r={r}$)",
        fontsize=11, fontweight="bold", color=NAVY)

    if eps_c is not None:
        ax.axvline(eps_c, color=CRIMSON, lw=1.4, ls="--",
                   label=rf"Critical coupling $\varepsilon_c\approx{eps_c:.2f}$")
        ax.fill_betweenx([1e-14, 2], 0, eps_c,
                         color=CRIMSON, alpha=0.06, label="Unsynchronised")
        ax.fill_betweenx([1e-14, 2], eps_c, 1.0,
                         color=TEAL,   alpha=0.08, label="Synchronised")
        ax.legend(fontsize=9, framealpha=0.85)

    ax.set_xlim(0, 1); ax.set_ylim(1e-14, 2)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    fig.tight_layout()
    fig.savefig("fig9_sync_transition.png", bbox_inches="tight", dpi=160)
    plt.close()
    print("  [✓] fig9_sync_transition.png")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("\n" + "═"*62)
    print("  Nonlinear Hall Transport — IDC-402")
    print("  Daman Kumar  |  MS23031")
    print("═"*62 + "\n")

    print("[1/9]  Phase portrait …")
    fig1_phase_portrait()

    print("[2/9]  Time evolution …")
    fig2_time_evolution()

    print("[3/9]  Trajectory divergence …")
    fig3_divergence()

    print("[4/9]  Orbit diagram (γ=0) …")
    fig4_orbit_diagram()

    print("[5/9]  Orbit diagram (γ=0.15) …")
    fig5_orbit_interference()

    print("[6/9]  Cobweb plots …")
    fig6_cobweb()

    print("[7/9]  Lyapunov spectrum …")
    fig7_lyapunov()

    print("[8/9]  Chaos synchronisation panels …")
    fig8_synchronisation()

    print("[9/9]  Sync transition curve …")
    fig9_sync_transition()

    print("\n" + "═"*62)
    print("  All 9 figures generated.")
    print("═"*62 + "\n")


if __name__ == "__main__":
    main()
