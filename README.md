Nonlinear Hall Transport — IDC-402 Term Project
Dynamics and Applications of Nonlinear Hall Transport: Stability, Bifurcation, and Chaos in Mesoscopic Semiconductors
	
Course	Nonlinear Dynamics (IDC-402)
Author	Daman Kumar · MS23031
Session	Jan–April 2025
---
Overview
This repository contains the complete simulation code and generated figures for the IDC-402 term project. The project models Hall transport in mesoscopic semiconductor systems as a nonlinear discrete map:
```
x_{n+1} = r · x_n · (1 − x_n) + γ · sin(ω · x_n)
```
where:
`x_n ∈ [0,1]` — normalised Hall voltage at step n
`r` — dimensionless nonlinearity / magnetic drive (controls dynamics)
`γ` — quantum interference amplitude (Aharonov–Bohm correction)
`ω` — interference oscillation wavenumber
When `γ = 0` this reduces to the canonical logistic map, providing a well-understood benchmark.
---
Repository Structure
```
nonlinear-hall-transport-IDC402/
├── hall_transport.py          # Main simulation script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├──└── figures/
    ├── fig1_xn1_vs_xn.png           # x_{n+1} vs x_n (4 r-values)
    ├── fig2_time_series.png          # Time-series x_n vs n
    ├── fig3_sensitive_dependence.png # SDIC: trajectory divergence
    ├── fig4_orbit_diagram_logistic.png   # Orbit diagram (γ=0)
    ├── fig4_orbit_diagram_gamma10.png    # Orbit diagram (γ=0.1)
    ├── fig6_cobweb_plots.png         # Cobweb diagrams (4 r-values)
    ├── fig7_lyapunov_spectrum.png    # Lyapunov exponent vs r
    ├── fig8_encryption.png           # Chaos-based encryption demo
    └── fig_period3.png               # Period-3 window
```
---
Quickstart
1. Clone the repository
```bash
git clone ```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Run the simulation
```bash
python hall_transport.py
```
All 9 figures are saved as high-resolution PNG files in the working directory.
---
Dependencies
```
numpy>=1.23
matplotlib>=3.6
```
---
Figures Generated
Figure	Description
`fig1_xn1_vs_xn.png`	x_{n+1} vs x_n for r = 0.76, 2.5, 3.11, 3.9
`fig2_time_series.png`	Time evolution for r = 0.86, 1.6, 3.1, 3.94
`fig3_sensitive_dependence.png`	Trajectory divergence at r = 3.9
`fig4_orbit_diagram_logistic.png`	Full orbit diagram, γ = 0
`fig4_orbit_diagram_gamma10.png`	Orbit diagram with interference, γ = 0.1
`fig6_cobweb_plots.png`	Cobweb plots for r = 0.724, 2.862, 3.472, 3.889
`fig7_lyapunov_spectrum.png`	Lyapunov exponent spectrum λ_L(r)
`fig8_encryption.png`	Chaos-based XOR encryption of "IDC402"
`fig_period3.png`	Period-3 window at r = 1 + 2√2 ≈ 3.8284
---
Key Physics Summary
r range	Hall transport regime	Attractor
0 < r < 1	Ohmic decay; voltage collapses	x* = 0
1 < r < 3	Stable nonlinear Hall plateau	x* = 1 − 1/r
3 < r ≲ 3.57	Period-doubling oscillations	Period-2ⁿ cycles
r ≳ 3.57	Chaotic voltage fluctuations	Strange attractor
r ≈ 3.83	Period-3 window (order in chaos)	Period-3 orbit
r = 4	Fully chaotic transport	Dense orbit in (0,1)
---
References
E. H. Hall, On a new action of the magnet on electric currents, Am. J. Math. 2, 287–292 (1879).
R. M. May, Simple mathematical models with very complicated dynamics, Nature 261, 459–467 (1976).
S. H. Strogatz, Nonlinear Dynamics and Chaos, 2nd ed., Westview Press (2015).
M. J. Feigenbaum, Quantitative universality for a class of nonlinear transformations, J. Stat. Phys. 19, 25–52 (1978).
L. M. Pecora and T. L. Carroll, Synchronization in chaotic systems, PRL 64, 821 (1990).
---
IDC-402 Nonlinear Dynamics · Jan–April 2025
