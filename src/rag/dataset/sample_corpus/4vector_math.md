---
title: Four-Vector Mathematics in Particle Physics
tags: ["four-vectors", "lorentz", "kinematics", "mathematics", "special-relativity"]
doc_type: theory
author: Higgs-Helper Corpus
---

# Four-Vector Mathematics in Particle Physics

## Introduction

Four-vectors are essential mathematical objects in special relativity and particle physics. They encode both spatial and temporal (or energy) information in a way that transforms properly under Lorentz transformations. Understanding four-vector mathematics is crucial for analyzing particle collisions and decays.

## Definition and Notation

A four-vector (or four-momentum) is typically written as:

$$
p^\mu = (E, \vec{p}) = (E, p_x, p_y, p_z)
$$

where:
- $E$ is the energy (time-like component)
- $\vec{p} = (p_x, p_y, p_z)$ is the three-momentum (space-like components)
- $\mu = 0, 1, 2, 3$ is the Lorentz index

### Metric and Index Notation

We use the metric tensor $g^{\mu\nu}$ with signature $(+, -, -, -)$:

$$
g^{\mu\nu} = \begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & -1 & 0 & 0 \\
0 & 0 & -1 & 0 \\
0 & 0 & 0 & -1
\end{pmatrix}
$$

Contravariant and covariant four-vectors are related by:

$$
p_\mu = g_{\mu\nu} p^\nu = (E, -p_x, -p_y, -p_z)
$$

## Invariant Mass

The most important property of a four-vector is its invariant mass, which is the same in all reference frames:

$$
m^2 = p^\mu p_\mu = E^2 - |\vec{p}|^2 = E^2 - (p_x^2 + p_y^2 + p_z^2)
$$

In natural units where $c = 1$. For a particle at rest, $\vec{p} = 0$ and $E = m$.

### Energy-Momentum Relation

From the invariant mass, we get the energy-momentum relation:

$$
E = \sqrt{|\vec{p}|^2 + m^2}
$$

For massless particles (photons, gluons): $E = |\vec{p}|$

For ultra-relativistic particles ($E \gg m$): $E \approx |\vec{p}|$

## Four-Vector Addition

Four-vectors add component-wise. For a system of $n$ particles:

$$
P^\mu_{total} = \sum_{i=1}^{n} p_i^\mu = \left(\sum_{i} E_i, \sum_{i} \vec{p}_i\right)
$$

### Invariant Mass of a System

The invariant mass of a multi-particle system is:

$$
M_{inv}^2 = \left(\sum_{i} E_i\right)^2 - \left|\sum_{i} \vec{p}_i\right|^2
$$

Expanding this for two particles:

$$
M_{12}^2 = (E_1 + E_2)^2 - |\vec{p}_1 + \vec{p}_2|^2
$$

$$
= E_1^2 + E_2^2 + 2E_1E_2 - p_1^2 - p_2^2 - 2\vec{p}_1 \cdot \vec{p}_2
$$

Using $E_i^2 - p_i^2 = m_i^2$:

$$
M_{12}^2 = m_1^2 + m_2^2 + 2(E_1E_2 - \vec{p}_1 \cdot \vec{p}_2)
$$

$$
= m_1^2 + m_2^2 + 2(E_1E_2 - p_1 p_2 \cos\theta)
$$

where $\theta$ is the angle between $\vec{p}_1$ and $\vec{p}_2$.

### Special Cases

**Two massless particles** (e.g., two photons):

$$
M_{\gamma\gamma}^2 = 2E_1E_2(1 - \cos\theta) = 4E_1E_2\sin^2(\theta/2)
$$

**Particle at rest + moving particle**:

If particle 2 is at rest ($\vec{p}_2 = 0$, $E_2 = m_2$):

$$
M_{12}^2 = m_1^2 + m_2^2 + 2E_1m_2
$$

## Coordinate Systems in Collider Physics

### Cartesian Coordinates

Standard coordinates $(x, y, z)$ where:
- $z$-axis: beam direction
- $x$-axis: pointing toward the center of accelerator ring
- $y$-axis: pointing upward (perpendicular to the beam and ground)

Four-momentum: $p^\mu = (E, p_x, p_y, p_z)$

### Cylindrical Coordinates

More natural for collider experiments:

$$
p_T = \sqrt{p_x^2 + p_y^2} \quad \text{(transverse momentum)}
$$

$$
\phi = \arctan(p_y / p_x) \quad \text{(azimuthal angle)}
$$

$$
p_z \quad \text{(longitudinal momentum)}
$$

Four-momentum: $p^\mu = (E, p_T\cos\phi, p_T\sin\phi, p_z)$

### Pseudorapidity and Rapidity

**Rapidity** $y$ is defined as:

$$
y = \frac{1}{2}\ln\left(\frac{E + p_z}{E - p_z}\right) = \tanh^{-1}\left(\frac{p_z}{E}\right)
$$

Rapidity is additive under Lorentz boosts along the $z$-axis.

**Pseudorapidity** $\eta$ is defined in terms of the polar angle $\theta$:

$$
\eta = -\ln\tan(\theta/2) = \tanh^{-1}\left(\frac{p_z}{|\vec{p}|}\right)
$$

For massless particles or ultra-relativistic particles, $\eta \approx y$.

Useful values:
- $\eta = 0$: perpendicular to beam ($\theta = 90°$)
- $\eta = \pm 1$: $\theta \approx 40°$ or $140°$
- $\eta = \pm 2$: $\theta \approx 15°$ or $165°$

## Angular Separations

### ΔR Distance

The most common measure of angular separation in collider physics:

$$
\Delta R = \sqrt{(\Delta\eta)^2 + (\Delta\phi)^2}
$$

where:

$$
\Delta\eta = \eta_1 - \eta_2
$$

$$
\Delta\phi = \phi_1 - \phi_2 \quad \text{(with } \Delta\phi \in [-\pi, \pi])
$$

$\Delta R$ is approximately Lorentz invariant under boosts along the beam direction.

**Usage**: 
- Jet clustering: particles within $\Delta R < 0.4$ or $0.8$ are grouped
- Isolation criteria: no other particles within $\Delta R < 0.3$ or $0.4$
- Lepton-jet separation: require $\Delta R > 0.4$ between leptons and jets

### Angular Distance in 3D Space

The opening angle between two particles:

$$
\cos\theta_{12} = \frac{\vec{p}_1 \cdot \vec{p}_2}{|\vec{p}_1||\vec{p}_2|}
$$

$$
= \frac{p_{1x}p_{2x} + p_{1y}p_{2y} + p_{1z}p_{2z}}{\sqrt{p_1^2}\sqrt{p_2^2}}
$$

## Lorentz Transformations

### Boost Along z-Axis

A boost with velocity $\beta = v/c$ (or rapidity $\zeta$) transforms:

$$
\begin{pmatrix} E' \\ p_x' \\ p_y' \\ p_z' \end{pmatrix} = 
\begin{pmatrix}
\gamma & 0 & 0 & -\beta\gamma \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
-\beta\gamma & 0 & 0 & \gamma
\end{pmatrix}
\begin{pmatrix} E \\ p_x \\ p_y \\ p_z \end{pmatrix}
$$

where $\gamma = 1/\sqrt{1-\beta^2}$.

Equivalently:

$$
E' = \gamma(E - \beta p_z)
$$

$$
p_z' = \gamma(p_z - \beta E)
$$

$$
p_T' = p_T \quad \text{(unchanged)}
$$

### Boost to Center-of-Mass Frame

For two particles with total four-momentum $P^\mu = p_1^\mu + p_2^\mu$, the boost velocity to the CM frame is:

$$
\vec{\beta}_{CM} = \frac{\vec{P}}{E_{total}} = \frac{\vec{p}_1 + \vec{p}_2}{E_1 + E_2}
$$

In the CM frame, $\vec{P}_{CM} = 0$ (total momentum is zero).

## Mandelstam Variables

For a scattering process $1 + 2 \rightarrow 3 + 4$, the Mandelstam variables are:

$$
s = (p_1 + p_2)^2 \quad \text{(center-of-mass energy squared)}
$$

$$
t = (p_1 - p_3)^2 \quad \text{(four-momentum transfer squared)}
$$

$$
u = (p_1 - p_4)^2
$$

They satisfy:

$$
s + t + u = \sum_{i=1}^{4} m_i^2
$$

**Physical interpretation**:
- $s$: square of total energy in CM frame, $\sqrt{s}$ is the collision energy
- $t$: squared four-momentum transfer between initial and final state
- $u$: alternative momentum transfer

For elastic scattering where $m_1 = m_3$ and $m_2 = m_4$:

$$
s + t + u = 2(m_1^2 + m_2^2)
$$

## Common Calculations

### Transverse Mass

Used when one particle is missing (neutrinos):

$$
m_T = \sqrt{2p_{T,1}p_{T,2}(1 - \cos\Delta\phi)}
$$

where $\Delta\phi$ is the azimuthal angle between the two objects.

### Missing Transverse Energy

In a collider, the total transverse momentum should be zero:

$$
\vec{p}_{T,miss} = -\sum_{\text{visible}} \vec{p}_T
$$

$$
E_{T,miss} = |\vec{p}_{T,miss}|
$$

Used to infer the presence of neutrinos or other invisible particles.

### Thrust

A measure of how "jet-like" an event is:

$$
T = \max_{\hat{n}} \frac{\sum_i |\vec{p}_i \cdot \hat{n}|}{\sum_i |\vec{p}_i|}
$$

where $\hat{n}$ is a unit vector. $T = 1$ for perfectly collimated events, $T = 0.5$ for isotropic events.

## Practical Examples

### Example 1: Dimuon Invariant Mass

Two muons (mass $m_\mu = 0.106$ GeV):

- Muon 1: $p_T = 50$ GeV, $\eta = 0.5$, $\phi = 1.0$
- Muon 2: $p_T = 45$ GeV, $\eta = -0.8$, $\phi = -2.0$

Calculate $p_x, p_y, p_z$ for each:

$$
p_x = p_T \cos\phi, \quad p_y = p_T \sin\phi, \quad p_z = p_T \sinh\eta
$$

$$
E = \sqrt{p_x^2 + p_y^2 + p_z^2 + m_\mu^2}
$$

Then:

$$
M_{\mu\mu} = \sqrt{(E_1 + E_2)^2 - (\vec{p}_1 + \vec{p}_2)^2}
$$

If $M_{\mu\mu} \approx 91$ GeV, this is likely a $Z \rightarrow \mu^+\mu^-$ decay.

### Example 2: Higgs to Two Photons

Two photons (massless):

- Photon 1: $E_1 = 65$ GeV, $\theta_1 = 30°$, $\phi_1 = 0°$
- Photon 2: $E_2 = 60$ GeV, $\theta_2 = 150°$, $\phi_2 = 180°$

$$
M_{\gamma\gamma} = \sqrt{2E_1E_2(1 - \cos\Theta)}
$$

where $\Theta$ is the 3D opening angle:

$$
\cos\Theta = \sin\theta_1\sin\theta_2\cos(\phi_1 - \phi_2) + \cos\theta_1\cos\theta_2
$$

If $M_{\gamma\gamma} \approx 125$ GeV, this could be $H \rightarrow \gamma\gamma$.

### Example 3: Top Quark Reconstruction

Top quark decays: $t \rightarrow W + b \rightarrow \ell + \nu + b$

Given:
- Lepton: $(E_\ell, \vec{p}_\ell)$
- b-jet: $(E_b, \vec{p}_b)$
- Missing $E_T$: $\vec{p}_{T,\nu}$

The neutrino $p_z$ can be found from the W mass constraint:

$$
M_W^2 = (E_\ell + E_\nu)^2 - |\vec{p}_\ell + \vec{p}_\nu|^2
$$

This gives a quadratic equation for $p_{z,\nu}$ (often has two solutions).

Then reconstruct top mass:

$$
M_t = \sqrt{(E_\ell + E_\nu + E_b)^2 - |\vec{p}_\ell + \vec{p}_\nu + \vec{p}_b|^2}
$$

Should peak around $M_t \approx 173$ GeV.

## Code Implementation

### In ROOT (C++)

```cpp
TLorentzVector p1, p2;
p1.SetPtEtaPhiM(50, 0.5, 1.0, 0.106);   // muon 1
p2.SetPtEtaPhiM(45, -0.8, -2.0, 0.106); // muon 2

TLorentzVector p_sum = p1 + p2;
double inv_mass = p_sum.M();
double deltaR = p1.DeltaR(p2);
```

### In Python (with vector library)

```python
import vector

p1 = vector.obj(pt=50, eta=0.5, phi=1.0, mass=0.106)
p2 = vector.obj(pt=45, eta=-0.8, phi=-2.0, mass=0.106)

p_sum = p1 + p2
inv_mass = p_sum.mass
deltaR = p1.deltaR(p2)
```

## Summary

Four-vector mathematics is the foundation of kinematic analysis in particle physics:

1. **Invariant mass** is conserved across reference frames
2. **Four-vector addition** allows reconstruction of parent particles
3. **$(p_T, \eta, \phi, m)$** coordinates are natural for collider physics
4. **$\Delta R$** measures angular separation in a Lorentz-invariant way
5. **Lorentz boosts** allow frame transformations (especially to CM frame)

Mastering these concepts is essential for understanding and performing particle physics analyses.
