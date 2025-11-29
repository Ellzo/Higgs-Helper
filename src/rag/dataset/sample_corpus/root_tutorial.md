---
title: ROOT Tutorial - Getting Started with Data Analysis
tags: ["ROOT", "tutorial", "C++", "data-analysis", "histograms"]
doc_type: tutorial
author: Higgs-Helper Corpus
---

# ROOT Tutorial: Getting Started with Data Analysis

## Introduction to ROOT

ROOT is a data analysis framework developed at CERN, written in C++. It provides tools for data storage, processing, analysis, and visualization. ROOT is widely used in high-energy physics for analyzing experimental data from particle detectors.

## Installation and Setup

ROOT can be installed from pre-compiled binaries or built from source. On most systems:

```bash
# Download from https://root.cern/install/
# Or use package managers:
conda install -c conda-forge root
# or
brew install root  # macOS
```

To set up ROOT environment:

```bash
source /path/to/root/bin/thisroot.sh
```

## Basic ROOT Session

Start an interactive ROOT session:

```bash
root
```

You'll see the ROOT prompt:

```
root [0]
```

## TH1F: One-Dimensional Histograms

### Creating a Histogram

```cpp
// Create a 1D histogram with 100 bins from 0 to 100
TH1F *h1 = new TH1F("h1", "My First Histogram;X axis;Entries", 100, 0, 100);

// Fill with random data
for (int i = 0; i < 10000; i++) {
    h1->Fill(gRandom->Gaus(50, 10));
}

// Draw the histogram
h1->Draw();
```

### Histogram Operations

```cpp
// Get histogram statistics
double mean = h1->GetMean();
double rms = h1->GetRMS();
int entries = h1->GetEntries();

// Fit with a Gaussian
h1->Fit("gaus");

// Get integral
double integral = h1->Integral();

// Rebin histogram (merge bins)
h1->Rebin(2);  // Merge 2 bins into 1

// Get bin content
double content = h1->GetBinContent(50);
```

## TTree: Data Storage and Analysis

TTree is ROOT's optimized data structure for storing large datasets.

### Creating a TTree

```cpp
// Create a ROOT file
TFile *file = new TFile("data.root", "RECREATE");

// Create a TTree
TTree *tree = new TTree("events", "Event Data");

// Define branch variables
Float_t px, py, pz, E;
Int_t event_number;

// Create branches
tree->Branch("px", &px, "px/F");
tree->Branch("py", &py, "py/F");
tree->Branch("pz", &pz, "pz/F");
tree->Branch("E", &E, "E/F");
tree->Branch("event", &event_number, "event/I");

// Fill the tree
for (int i = 0; i < 1000; i++) {
    event_number = i;
    px = gRandom->Gaus(0, 10);
    py = gRandom->Gaus(0, 10);
    pz = gRandom->Gaus(0, 20);
    E = TMath::Sqrt(px*px + py*py + pz*pz + 0.938*0.938);  // Proton mass
    
    tree->Fill();
}

// Write to file
tree->Write();
file->Close();
```

### Reading a TTree

```cpp
// Open the file
TFile *file = new TFile("data.root", "READ");
TTree *tree = (TTree*)file->Get("events");

// Set branch addresses
Float_t px, py, pz, E;
tree->SetBranchAddress("px", &px);
tree->SetBranchAddress("py", &py);
tree->SetBranchAddress("pz", &pz);
tree->SetBranchAddress("E", &E);

// Create histogram
TH1F *h_pt = new TH1F("h_pt", "Transverse Momentum;p_{T} (GeV);Events", 50, 0, 50);

// Loop over entries
Long64_t nentries = tree->GetEntries();
for (Long64_t i = 0; i < nentries; i++) {
    tree->GetEntry(i);
    
    // Calculate transverse momentum
    double pt = TMath::Sqrt(px*px + py*py);
    h_pt->Fill(pt);
}

h_pt->Draw();
```

### TTree::Draw() Method

ROOT provides a powerful shortcut for simple analyses:

```cpp
// Draw histogram directly from tree
tree->Draw("sqrt(px*px + py*py) >> h_pt(50, 0, 50)");

// With selection cuts
tree->Draw("E", "E > 50");

// Two-dimensional plot
tree->Draw("py:px", "E > 100", "colz");

// With mathematical operations
tree->Draw("TMath::Sqrt(px*px + py*py + pz*pz)");
```

## TLorentzVector: Four-Vector Calculations

TLorentzVector is essential for relativistic particle physics calculations:

```cpp
#include "TLorentzVector.h"

// Create four-vectors for two particles
TLorentzVector p1, p2;

// Set using (px, py, pz, E)
p1.SetPxPyPzE(10.0, 5.0, 20.0, 25.0);
p2.SetPxPyPzE(-8.0, 3.0, -15.0, 20.0);

// Alternative: Set using (pt, eta, phi, mass)
p1.SetPtEtaPhiM(10.0, 2.0, 1.57, 0.105);  // Muon

// Access components
double px = p1.Px();
double py = p1.Py();
double pz = p1.Pz();
double E = p1.E();

// Kinematic variables
double pt = p1.Pt();           // Transverse momentum
double eta = p1.Eta();         // Pseudorapidity
double phi = p1.Phi();         // Azimuthal angle
double mass = p1.M();          // Invariant mass

// Four-vector operations
TLorentzVector p_sum = p1 + p2;  // Add four-vectors
double inv_mass = p_sum.M();     // Invariant mass of system

// Lorentz transformations
TVector3 boost_vector = p1.BoostVector();
p2.Boost(-boost_vector);  // Boost p2 to rest frame of p1

// Angular separations
double deltaR = p1.DeltaR(p2);  // ΔR = sqrt(Δη² + Δφ²)
double deltaPhi = p1.DeltaPhi(p2);
```

## Invariant Mass Example

Calculate invariant mass of two muons (common in Z boson → μ⁺μ⁻ analyses):

```cpp
// Define muon mass
const double MUON_MASS = 0.105658;  // GeV

// Read from tree or set manually
TLorentzVector muon1, muon2;

// Set muon 1 (positive charge)
muon1.SetPtEtaPhiM(45.0, 0.5, 1.2, MUON_MASS);

// Set muon 2 (negative charge)
muon2.SetPtEtaPhiM(38.0, -0.8, -2.1, MUON_MASS);

// Calculate invariant mass
TLorentzVector dimuon = muon1 + muon2;
double inv_mass = dimuon.M();

cout << "Invariant mass: " << inv_mass << " GeV" << endl;

// If inv_mass ≈ 91.2 GeV, this could be a Z boson decay!
```

## File I/O and Object Storage

### Writing Objects to File

```cpp
TFile *outfile = new TFile("output.root", "RECREATE");

// Write histogram
TH1F *hist = new TH1F("h", "Histogram", 100, 0, 100);
hist->Write();

// Write tree
TTree *tree = new TTree("data", "Data Tree");
// ... fill tree ...
tree->Write();

// Write any object
TGraph *graph = new TGraph(10);
graph->Write("my_graph");

outfile->Close();
```

### Reading Objects from File

```cpp
TFile *infile = new TFile("output.root", "READ");

// Method 1: Get by name
TH1F *hist = (TH1F*)infile->Get("h");

// Method 2: Direct pointer
TTree *tree;
infile->GetObject("data", tree);

// List contents
infile->ls();

// Close file
infile->Close();
```

## Canvas and Drawing Options

### Creating a Canvas

```cpp
// Create a canvas
TCanvas *c1 = new TCanvas("c1", "My Canvas", 800, 600);

// Divide canvas into pads
c1->Divide(2, 2);  // 2x2 grid

// Draw in different pads
c1->cd(1);  // Top-left
h1->Draw();

c1->cd(2);  // Top-right
h2->Draw();

// Save canvas
c1->SaveAs("plot.png");
c1->SaveAs("plot.pdf");
c1->SaveAs("plot.root");  // Can be reopened in ROOT
```

### Drawing Options

```cpp
hist->Draw();           // Default (bars)
hist->Draw("hist");     // Histogram (no error bars)
hist->Draw("E");        // With error bars
hist->Draw("same");     // Overlay on existing plot

// 2D histogram options
hist2d->Draw("colz");   // Color plot with palette
hist2d->Draw("lego");   // Lego plot
hist2d->Draw("surf");   // Surface plot
```

## Fitting Data

### Built-in Functions

```cpp
// Fit with predefined function
hist->Fit("gaus");      // Gaussian
hist->Fit("expo");      // Exponential
hist->Fit("pol2");      // 2nd order polynomial

// Fit in a range
hist->Fit("gaus", "", "", 40, 60);

// Get fit parameters
TF1 *fit = hist->GetFunction("gaus");
double mean = fit->GetParameter(1);
double sigma = fit->GetParameter(2);
double chi2 = fit->GetChisquare();
int ndf = fit->GetNDF();
```

### Custom Functions

```cpp
// Define custom function
TF1 *func = new TF1("func", "[0]*exp(-0.5*((x-[1])/[2])^2) + [3]", 0, 100);
func->SetParameters(100, 50, 10, 5);  // Initial guesses
func->SetParNames("Amplitude", "Mean", "Sigma", "Background");

hist->Fit(func);
```

## Macros and Scripts

Save ROOT code in a `.C` file:

```cpp
// analysis.C
void analysis() {
    TFile *file = TFile::Open("data.root");
    TTree *tree = (TTree*)file->Get("events");
    
    TH1F *h = new TH1F("h", "Histogram", 100, 0, 100);
    tree->Draw("variable >> h");
    
    h->Draw();
}
```

Run with:

```bash
root -l analysis.C
# or
root [0] .x analysis.C
```

## Common Patterns in HEP Analysis

### Event Selection

```cpp
// Loop over events and apply cuts
for (Long64_t i = 0; i < tree->GetEntries(); i++) {
    tree->GetEntry(i);
    
    // Apply selection cuts
    if (pt < 20) continue;           // Minimum pt cut
    if (TMath::Abs(eta) > 2.5) continue;  // Detector acceptance
    if (charge == 0) continue;       // Require charged particle
    
    // Fill histograms for selected events
    h_pt->Fill(pt);
    h_eta->Fill(eta);
}
```

### Efficiency Calculation

```cpp
// Create "passed" and "total" histograms
TH1F *h_total = new TH1F("total", "Total", 50, 0, 100);
TH1F *h_passed = new TH1F("passed", "Passed", 50, 0, 100);

// Fill based on criteria
for (auto event : events) {
    h_total->Fill(event.pt);
    if (event.passes_selection) {
        h_passed->Fill(event.pt);
    }
}

// Calculate efficiency
TEfficiency *eff = new TEfficiency(*h_passed, *h_total);
eff->Draw();
```

## Transition to Python: uproot

Modern analyses often use Python with the `uproot` library to read ROOT files:

```python
import uproot
import awkward as ak
import numpy as np

# Open ROOT file
file = uproot.open("data.root")
tree = file["events"]

# Read branches as arrays
px = tree["px"].array()
py = tree["py"].array()
pz = tree["pz"].array()
E = tree["E"].array()

# Calculate pt
pt = np.sqrt(px**2 + py**2)

# Apply cuts
selection = (pt > 20) & (np.abs(pz) < 100)
pt_selected = pt[selection]
```

This is covered in more detail in the PyHEP integration documentation.

## Resources

- Official ROOT documentation: https://root.cern/doc/master/
- ROOT tutorials: https://root.cern/doc/master/group__Tutorials.html
- ROOT forum: https://root-forum.cern.ch/
- Uproot documentation: https://uproot.readthedocs.io/
