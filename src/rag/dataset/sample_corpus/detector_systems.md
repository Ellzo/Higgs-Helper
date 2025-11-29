---
title: Particle Detector Systems - ATLAS and CMS
tags: ["detectors", "ATLAS", "CMS", "calorimetry", "tracking", "muon-system"]
doc_type: reference
author: Higgs-Helper Corpus
---

# Particle Detector Systems: ATLAS and CMS

## Introduction

Modern particle physics detectors at the Large Hadron Collider (LHC) are complex, multi-layered instruments designed to measure the properties of particles produced in high-energy collisions. The two general-purpose detectors, ATLAS (A Toroidal LHC ApparatuS) and CMS (Compact Muon Solenoid), use different technologies but share similar design philosophies.

## General Detector Architecture

Both ATLAS and CMS consist of concentric layers arranged in a cylindrical geometry around the collision point:

1. **Inner Tracking System**: Measures particle trajectories and momenta
2. **Electromagnetic Calorimeter (ECAL)**: Measures energy of electrons and photons
3. **Hadronic Calorimeter (HCAL)**: Measures energy of hadrons (jets)
4. **Muon System**: Identifies and measures muons
5. **Magnet System**: Bends charged particle trajectories for momentum measurement

## Coordinate System

Standard coordinate system for both detectors:

- **Origin**: Nominal collision point
- **z-axis**: Along beam direction
- **x-axis**: Points toward center of LHC ring
- **y-axis**: Points upward (perpendicular to ground)

**Cylindrical coordinates**:
- **r**: Radial distance from beam axis
- **φ**: Azimuthal angle around beam axis (0 to 2π)
- **η**: Pseudorapidity, $\eta = -\ln\tan(\theta/2)$ where $θ$ is polar angle from beam

**Coverage**:
- Central region: $|\eta| < 1.0$
- Forward region: $1.0 < |\eta| < 2.5$
- Very forward: $|\eta| > 2.5$

## ATLAS Detector

### Overview

- **Dimensions**: 46 m long, 25 m diameter
- **Weight**: ~7,000 tons
- **Magnetic field**: 2 T solenoid + toroidal system
- **Design philosophy**: Large acceptance, precision measurements

### Inner Detector (ID)

The ATLAS Inner Detector operates within a 2 T solenoidal magnetic field and provides tracking up to $|\eta| < 2.5$.

#### Pixel Detector

- **Innermost layer**: Insertable B-Layer (IBL) at r = 33 mm
- **Technology**: Silicon pixel sensors
- **Total pixels**: ~92 million
- **Pixel size**: 50 × 250 μm² (r-φ × z)
- **Spatial resolution**: ~10 μm (r-φ), ~115 μm (z)
- **Coverage**: $|\eta| < 2.5$

**Purpose**: Precise vertex reconstruction, b-tagging

#### Semiconductor Tracker (SCT)

- **Technology**: Silicon microstrip detectors
- **Modules**: ~4,000 modules, 8 layers
- **Strip pitch**: 80 μm
- **Spatial resolution**: ~17 μm (r-φ), ~580 μm (z)
- **Total strips**: ~6.3 million

#### Transition Radiation Tracker (TRT)

- **Technology**: Straw tube drift chambers with xenon gas
- **Straws**: ~350,000 tubes, 4 mm diameter
- **Resolution**: ~130 μm per straw
- **Coverage**: $|\eta| < 2.0$
- **Special feature**: Transition radiation for electron identification

**Momentum resolution**:

$$
\frac{\sigma_{p_T}}{p_T} = 0.05\% \times p_T [\text{GeV}] \oplus 1\%
$$

where $\oplus$ denotes addition in quadrature.

### Calorimetry

#### Electromagnetic Calorimeter (ECAL)

- **Technology**: Liquid argon (LAr) sampling calorimeter with lead absorbers
- **Granularity**: $\Delta\eta \times \Delta\phi = 0.025 \times 0.025$ (barrel)
- **Depth**: > 22 radiation lengths ($X_0$)
- **Coverage**: $|\eta| < 3.2$

**Energy resolution**:

$$
\frac{\sigma_E}{E} = \frac{10\%}{\sqrt{E[\text{GeV}]}} \oplus 0.7\%
$$

Excellent for electron and photon measurements.

#### Hadronic Calorimeter (HCAL)

**Tile Calorimeter** (barrel and extended barrel, $|\eta| < 1.7$):
- Technology: Steel absorber with plastic scintillating tiles
- Granularity: $\Delta\eta \times \Delta\phi = 0.1 \times 0.1$
- Depth: ~7.4 interaction lengths (λ)

**LAr Hadronic End-Cap** ($1.5 < |\eta| < 3.2$):
- Technology: Liquid argon with copper absorbers

**LAr Forward Calorimeter** ($3.1 < |\eta| < 4.9$):
- Technology: LAr with copper (EM) and tungsten (hadronic) absorbers
- Handles extreme radiation doses

**Energy resolution**:

$$
\frac{\sigma_E}{E} = \frac{50\%}{\sqrt{E[\text{GeV}]}} \oplus 3\%
$$

### Muon Spectrometer

The largest component of ATLAS, using three large superconducting toroid magnets.

**Technologies**:
- **Monitored Drift Tubes (MDT)**: Precision tracking, $|\eta| < 2.7$
- **Cathode Strip Chambers (CSC)**: High-rate capability, $2.0 < |\eta| < 2.7$
- **Resistive Plate Chambers (RPC)**: Trigger, barrel
- **Thin Gap Chambers (TGC)**: Trigger, endcaps

**Resolution**:
- Single-tube: ~80 μm
- Momentum resolution: $\frac{\sigma_{p_T}}{p_T} = 10\%$ at $p_T = 1$ TeV

### Trigger System

ATLAS uses a two-level trigger system:

1. **Level-1 (L1)**: Hardware-based, reduces rate from 40 MHz to ~100 kHz, decision time < 2.5 μs
2. **High-Level Trigger (HLT)**: Software-based, reduces to ~1 kHz for storage

## CMS Detector

### Overview

- **Dimensions**: 21 m long, 15 m diameter
- **Weight**: ~14,000 tons (denser than ATLAS)
- **Magnetic field**: 3.8 T solenoid (stronger than ATLAS)
- **Design philosophy**: Compact, strong magnetic field, excellent muon and energy resolution

### Tracking System

CMS uses an all-silicon tracker within a 3.8 T magnetic field.

#### Pixel Detector

- **Layers**: 4 barrel layers + 3 endcap disks per side
- **Technology**: Silicon pixel sensors
- **Total pixels**: ~124 million
- **Pixel size**: 100 × 150 μm²
- **Spatial resolution**: ~10 μm
- **Coverage**: $|\eta| < 2.5$

#### Silicon Strip Tracker

- **Technology**: Silicon microstrip detectors
- **Total strips**: ~9.6 million
- **Modules**: ~15,000
- **Strip pitch**: 80-180 μm
- **Spatial resolution**: 20-50 μm

**Momentum resolution**:

$$
\frac{\sigma_{p_T}}{p_T} = 0.015\% \times p_T [\text{GeV}] \oplus 0.5\%
$$

Better than ATLAS due to stronger magnetic field.

### Electromagnetic Calorimeter (ECAL)

**Technology**: Scintillating lead tungstate (PbWO₄) crystals

- **Barrel crystals**: 61,200 crystals, $|\eta| < 1.479$
- **Endcap crystals**: 14,648 crystals, $1.479 < |\eta| < 3.0$
- **Crystal size**: ~22 × 22 mm² front face
- **Length**: 23 cm (25.8 $X_0$)
- **Light decay time**: ~25 ns (fast response)

**Advantages**:
- Homogeneous calorimeter (no sampling)
- Excellent energy resolution
- Radiation hard

**Energy resolution**:

$$
\frac{\sigma_E}{E} = \frac{2.8\%}{\sqrt{E[\text{GeV}]}} \oplus \frac{12\%}{E[\text{GeV}]} \oplus 0.3\%
$$

Significantly better than ATLAS for EM particles.

**Preshower Detector**:
- Silicon strip detectors in front of endcap ECAL
- Improves π⁰/γ separation

### Hadronic Calorimeter (HCAL)

**Barrel HCAL** ($|\eta| < 1.3$):
- Technology: Brass absorber with plastic scintillator
- Granularity: $\Delta\eta \times \Delta\phi = 0.087 \times 0.087$
- Depth: 5.82 interaction lengths

**Endcap HCAL** ($1.3 < |\eta| < 3.0$):
- Similar technology to barrel
- 10 interaction lengths deep

**Forward HCAL** ($3.0 < |\eta| < 5.2$):
- Technology: Steel absorber with quartz fibers (Cherenkov light)
- Radiation hard for very forward region

**Outer HCAL**:
- Additional layer outside solenoid for "tail-catching"
- Improves energy measurement for energetic hadrons

**Energy resolution**:

$$
\frac{\sigma_E}{E} = \frac{100\%}{\sqrt{E[\text{GeV}]}} \oplus 5\%
$$

### Muon System

CMS muon system is embedded in the steel return yoke of the magnet.

**Barrel** ($|\eta| < 1.2$):
- **Drift Tubes (DT)**: 4 stations, precision tracking
- Spatial resolution: ~100 μm

**Endcaps** ($0.9 < |\eta| < 2.4$):
- **Cathode Strip Chambers (CSC)**: 4 stations
- Better rate capability than DTs

**Trigger System**:
- **Resistive Plate Chambers (RPC)**: Fast response in both barrel and endcaps

**Resolution**:

$$
\frac{\sigma_{p_T}}{p_T} = 1-2\% \text{ (for } p_T < 100 \text{ GeV)}
$$

$$
\frac{\sigma_{p_T}}{p_T} = 5-10\% \text{ (for } p_T \sim 1 \text{ TeV)}
$$

### Trigger System

CMS also uses a two-level system:

1. **Level-1 (L1)**: Custom hardware, reduces 40 MHz to ~100 kHz
2. **High-Level Trigger (HLT)**: Software farm, reduces to ~1 kHz

## Particle Identification

### Electrons

**Signatures**:
- Narrow electromagnetic shower in ECAL
- Matched track in inner detector
- High $E/p$ ratio (energy/momentum ≈ 1)
- TRT hits (ATLAS) showing transition radiation

**Efficiency**: > 95% for $E_T > 25$ GeV, $|\eta| < 2.5$

### Photons

**Signatures**:
- Electromagnetic shower in ECAL
- No associated track
- Isolation: little energy in surrounding region

**Conversions**: Some photons convert to $e^+e^-$ pairs in tracker material

### Muons

**Signatures**:
- Track in inner detector
- Track segments in muon system
- Minimal energy deposit in calorimeters (minimum ionizing particle, or MIP)

**Types**:
- **Standalone muons**: Reconstructed only in muon system
- **Combined muons**: Matched tracks in inner detector and muon system (highest quality)
- **Tagged muons**: Inner detector track with matching calorimeter signature

**Efficiency**: > 99% for $p_T > 10$ GeV

### Jets

**Jet clustering algorithms**:
- **Anti-kt algorithm**: Most common, $R = 0.4$ or $0.8$
- **kt algorithm**: Alternative for some studies

**Jet identification**:
- Hadronic shower in HCAL (and sometimes ECAL)
- Multiple tracks pointing to calorimeter cluster

**Jet energy corrections**:
1. Pile-up correction (subtract extra pp interactions)
2. Relative η-dependent correction
3. Absolute energy scale correction

**b-tagging**: Identifying jets from b-quarks
- Secondary vertex reconstruction (b-hadrons travel ~few mm before decaying)
- High-impact parameter tracks
- **Algorithms**: MV2 (ATLAS), DeepCSV (CMS)
- **Efficiency**: ~70-80% for b-jets, ~1% mistagging rate for light jets

### Missing Transverse Energy ($E_T^{miss}$)

Indicates presence of neutrinos or other invisible particles:

$$
\vec{E}_T^{miss} = -\sum_{\text{all objects}} \vec{p}_T
$$

**Quality**: Depends on calorimeter coverage and resolution

**Typical cuts**: $E_T^{miss} > 30-50$ GeV to reject backgrounds

## Performance Comparison

| Feature | ATLAS | CMS |
|---------|-------|-----|
| **Size** | Larger (46 m long) | Compact (21 m long) |
| **Weight** | ~7,000 tons | ~14,000 tons |
| **B-field** | 2 T (solenoid) | 3.8 T (solenoid) |
| **Tracking resolution** | Good | Excellent |
| **EM energy resolution** | Good | Excellent (crystals) |
| **Muon resolution** | Excellent (toroids) | Good |
| **Design philosophy** | Large acceptance | High precision |

## Event Reconstruction Pipeline

1. **Raw data**: Detector signals (voltages, currents)
2. **Hit reconstruction**: Convert signals to space points
3. **Track reconstruction**: Find particle trajectories from hits
4. **Calorimeter clustering**: Group cells into showers
5. **Particle flow**: Combine tracking + calorimetry for optimal energy measurement
6. **Physics objects**: Reconstruct electrons, muons, jets, $E_T^{miss}$
7. **Analysis-level objects**: Apply quality cuts, calibrations, identification

**Particle Flow**: Modern approach combining:
- Charged hadrons: use tracker momentum (better resolution)
- Neutral hadrons: use calorimeter energy
- Photons: use calorimeter energy
- Muons: use muon system momentum

Significantly improves jet energy resolution and $E_T^{miss}$ measurement.

## Luminosity and Pile-up

**Instantaneous luminosity**: $\mathcal{L} \sim 10^{34}$ cm⁻²s⁻¹ (design) to $2 \times 10^{34}$ cm⁻²s⁻¹ (Run 2 peak)

**Pile-up**: Multiple pp collisions per bunch crossing
- Average: ~30-50 interactions per crossing
- Challenge: Distinguish signal from pile-up
- Mitigation: Timing, tracking, jet substructure techniques

**Integrated luminosity** (Run 2, 2015-2018): ~140 fb⁻¹ per experiment

## Detector Simulation

Simulation pipeline:
1. **Event generation**: Monte Carlo generators (Pythia, Herwig, MadGraph)
2. **Detector simulation**: GEANT4 (models material interactions)
3. **Digitization**: Convert energy deposits to detector signals
4. **Reconstruction**: Same algorithms as data

**Validation**: Compare data to simulation, apply corrections

## Upgrades for High-Luminosity LHC (HL-LHC)

Starting ~2029, HL-LHC will increase luminosity to $\mathcal{L} = 5-7 \times 10^{34}$ cm⁻²s⁻¹.

**Challenges**:
- Pile-up: ~200 interactions per crossing
- Radiation damage: Much higher integrated doses

**Upgrades**:
- New inner tracking detectors (radiation-hard silicon)
- Improved trigger systems (read out at 40 MHz)
- Enhanced calorimeter electronics and readout
- Improved muon coverage

**Goal**: Collect 3000-4000 fb⁻¹ over 10 years

## Key Physics Signatures

### Higgs → γγ
- Two isolated, high-$E_T$ photons
- Excellent mass resolution (~1-2%)
- Low background

### Higgs → ZZ* → 4ℓ
- Four isolated leptons (e or μ)
- Very clean "golden channel"
- Mass resolution ~1-2 GeV

### Higgs → bb
- Two b-tagged jets
- Large background from QCD
- Requires associated production (VH, ttH)

### SUSY searches
- Jets + $E_T^{miss}$
- Multiple leptons
- High $H_T = \sum p_T$ (jets)

### Top quark pair production
- Two b-jets + leptons/jets from W decays
- Cross section measurement, top mass

## References

- ATLAS Collaboration, "The ATLAS Experiment at the CERN Large Hadron Collider", JINST 3 (2008) S08003
- CMS Collaboration, "The CMS Experiment at the CERN LHC", JINST 3 (2008) S08004
- Technical Design Reports: https://twiki.cern.ch/twiki/bin/view/AtlasPublic/ and https://cms.cern/
