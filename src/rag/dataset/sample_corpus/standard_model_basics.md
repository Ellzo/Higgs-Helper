---
title: Standard Model Basics - Particles and Forces
tags: ["standard-model", "quarks", "leptons", "gauge-bosons", "theory"]
doc_type: theory
author: Higgs-Helper Corpus
---

# Standard Model Basics: Particles and Forces

## Overview

The Standard Model of particle physics describes the fundamental constituents of matter and three of the four known fundamental forces (electromagnetic, weak, and strong interactions). It is a quantum field theory that has been extraordinarily successful in predicting experimental results.

## Fundamental Particles

### Fermions (Matter Particles)

Fermions are spin-1/2 particles that obey Fermi-Dirac statistics and the Pauli exclusion principle. They are divided into two categories:

#### Quarks

Quarks come in six "flavors" organized into three generations:

| Generation | Up-Type | Mass | Down-Type | Mass | Charge |
|------------|---------|------|-----------|------|--------|
| 1st | up (u) | ~2.2 MeV | down (d) | ~4.7 MeV | +2/3, -1/3 |
| 2nd | charm (c) | ~1.3 GeV | strange (s) | ~95 MeV | +2/3, -1/3 |
| 3rd | top (t) | ~173 GeV | bottom (b) | ~4.2 GeV | +2/3, -1/3 |

Quarks also carry color charge (red, green, blue) and are never observed in isolation due to color confinement. They combine to form hadrons:

- **Baryons**: Three quarks (e.g., proton = uud, neutron = udd)
- **Mesons**: Quark-antiquark pairs (e.g., pion π⁺ = u$\bar{d}$, kaon K⁺ = u$\bar{s}$)

#### Leptons

Leptons also come in three generations:

| Generation | Charged Lepton | Mass | Neutrino | Mass |
|------------|----------------|------|----------|------|
| 1st | electron (e⁻) | 0.511 MeV | $\nu_e$ | < 1 eV |
| 2nd | muon (μ⁻) | 105.7 MeV | $\nu_\mu$ | < 1 eV |
| 3rd | tau (τ⁻) | 1.777 GeV | $\nu_\tau$ | < 1 eV |

Leptons do not carry color charge and can exist as free particles.

### Bosons (Force Carriers)

Bosons are integer-spin particles that mediate forces between fermions:

#### Gauge Bosons

- **Photon (γ)**: Massless, mediates electromagnetic force, spin-1
- **W bosons (W⁺, W⁻)**: Mass = 80.4 GeV, mediate weak force (charged current), spin-1
- **Z boson (Z⁰)**: Mass = 91.2 GeV, mediates weak force (neutral current), spin-1
- **Gluons (g)**: Massless, mediate strong force, spin-1, eight types (different color combinations)

#### Scalar Boson

- **Higgs boson (H⁰)**: Mass = 125.1 GeV, responsible for electroweak symmetry breaking, spin-0

## Fundamental Forces and Interactions

### Quantum Electrodynamics (QED)

QED describes electromagnetic interactions via photon exchange. The coupling strength is given by the fine structure constant:

$$
\alpha = \frac{e^2}{4\pi\epsilon_0\hbar c} \approx \frac{1}{137}
$$

The QED vertex factor for electron-photon interaction is:

$$
\mathcal{M} \propto -ie\gamma^\mu
$$

### Quantum Chromodynamics (QCD)

QCD describes strong interactions between quarks and gluons via color charge. The strong coupling constant $\alpha_s$ depends on the energy scale $Q$:

$$
\alpha_s(Q^2) = \frac{12\pi}{(33 - 2n_f)\ln(Q^2/\Lambda^2_{QCD})}
$$

where $n_f$ is the number of active quark flavors and $\Lambda_{QCD} \approx 200$ MeV is the QCD scale parameter. At $Q = M_Z$:

$$
\alpha_s(M_Z) \approx 0.118
$$

Key features of QCD:

- **Asymptotic freedom**: $\alpha_s$ decreases at high energies (short distances)
- **Confinement**: Quarks cannot be isolated; they are always bound in color-neutral hadrons
- **Running coupling**: The strength depends on the energy scale

### Electroweak Theory

The electroweak theory unifies electromagnetic and weak interactions through $SU(2)_L \times U(1)_Y$ gauge symmetry. After spontaneous symmetry breaking via the Higgs mechanism, we obtain:

$$
\sin^2\theta_W = 1 - \frac{M_W^2}{M_Z^2} \approx 0.223
$$

where $\theta_W$ is the weak mixing angle (Weinberg angle).

The weak charged current interaction (W exchange) has the form:

$$
\mathcal{L}_{CC} = -\frac{g}{2\sqrt{2}} [J^\mu_W W^+_\mu + J^\mu_W W^-_\mu]
$$

where the current is:

$$
J^\mu_W = \bar{\psi}_L \gamma^\mu \psi_L
$$

Only left-handed fermions (and right-handed antifermions) participate in weak charged current interactions.

## Conservation Laws

### Exact Conservation Laws

1. **Electric charge (Q)**: Total charge is conserved in all interactions
2. **Color charge**: Total color is conserved (always color-neutral states)
3. **Baryon number (B)**: Number of quarks/3 minus antiquarks/3
4. **Lepton number (L)**: Separate conservation for $L_e$, $L_\mu$, $L_\tau$ (approximately)

### Approximate Conservation Laws

1. **Parity (P)**: Conserved in strong and electromagnetic, violated in weak interactions
2. **Charge conjugation (C)**: Conserved in strong and electromagnetic, violated in weak
3. **CP**: Violated in weak interactions (observed in K and B meson systems)
4. **Flavor**: Conserved in strong and electromagnetic, violated in weak (CKM mixing)

## Quark Mixing (CKM Matrix)

Weak interactions can change quark flavor via the Cabibbo-Kobayashi-Maskawa (CKM) matrix:

$$
\begin{pmatrix} d' \\ s' \\ b' \end{pmatrix} = \begin{pmatrix} 
V_{ud} & V_{us} & V_{ub} \\
V_{cd} & V_{cs} & V_{cb} \\
V_{td} & V_{ts} & V_{tb}
\end{pmatrix} \begin{pmatrix} d \\ s \\ b \end{pmatrix}
$$

Approximate values:

$$
|V_{CKM}| \approx \begin{pmatrix}
0.974 & 0.225 & 0.004 \\
0.225 & 0.973 & 0.041 \\
0.009 & 0.040 & 0.999
\end{pmatrix}
$$

The matrix is unitary: $V^\dagger V = I$. CP violation arises from the complex phase in this matrix.

## Feynman Diagrams and Calculations

Particle interactions are visualized using Feynman diagrams. Each element corresponds to a mathematical term:

- **External lines**: Incoming/outgoing particles (wave functions)
- **Internal lines (propagators)**: Virtual particles with propagator factor $\frac{i}{p^2 - m^2 + i\epsilon}$
- **Vertices**: Interaction points with coupling factors

Example: Electron-muon scattering via photon exchange ($e^-\mu^- \rightarrow e^-\mu^-$)

$$
\mathcal{M} = \frac{-ie^2}{q^2}[\bar{u}_e\gamma^\mu u_e][\bar{u}_\mu\gamma_\mu u_\mu]
$$

where $q$ is the four-momentum transfer.

## Cross Sections and Decay Rates

The cross section for a $2 \rightarrow n$ process is:

$$
\sigma = \frac{1}{2E_1 2E_2 |v_1 - v_2|} \int d\Pi_n |\mathcal{M}|^2
$$

where $d\Pi_n$ is the $n$-body phase space element.

For a particle decay $A \rightarrow B + C$:

$$
\Gamma = \frac{1}{2M_A} \int \frac{d^3p_B}{(2\pi)^3 2E_B} \frac{d^3p_C}{(2\pi)^3 2E_C} (2\pi)^4 \delta^4(p_A - p_B - p_C) |\mathcal{M}|^2
$$

The lifetime is $\tau = \hbar/\Gamma$.

## Units and Natural Units

In particle physics, we often use natural units where $\hbar = c = 1$. This means:

- Energy, mass, and momentum all have units of GeV
- Time and length have units of GeV⁻¹
- Cross sections have units of GeV⁻² (or equivalently, barns: 1 barn = 10⁻²⁴ cm² ≈ 2.568 GeV⁻²)

Conversions:
$$
\hbar c \approx 197.3 \text{ MeV·fm}
$$

$$
1 \text{ GeV}^{-1} \approx 6.58 \times 10^{-25} \text{ s} \approx 0.197 \text{ fm}
$$

## Beyond the Standard Model

While the Standard Model is remarkably successful, it has known limitations:

1. **Neutrino masses**: Observed neutrino oscillations require mass, but the SM assumes massless neutrinos
2. **Dark matter**: The SM does not contain a viable dark matter candidate
3. **Dark energy**: Not addressed by the SM
4. **Gravity**: Not included in the SM framework
5. **Hierarchy problem**: Why is $M_H \ll M_{Planck}$?
6. **Strong CP problem**: Why is the θ-parameter so small?
7. **Matter-antimatter asymmetry**: Insufficient CP violation in the SM

These open questions motivate searches for new physics beyond the Standard Model.
