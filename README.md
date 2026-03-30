# AI-Optimized Nuclear Shelter Siting (UFLP)

## Overview

This project applies a Genetic Algorithm (GA) to identify optimal geographic locations for nuclear shelters across the United States. The problem is framed as an Uncapacitated Facility Location Problem (UFLP). The objective is to maximize population coverage while ensuring shelters are positioned outside yield-scaled blast zones derived from the Hopkinson-Cranz cube-root scaling law.

Results are compared against a greedy heuristic baseline. Hyperparameters are tuned using Optuna.

## Team Members

- Murtaza Nipplewala
- Aartika Parmar
- Samyak Shah

---

## Project Structure

```
nuclear_shelter_location/
│
├── data/
│   └── raw/                        # ← Place downloaded data files here
│       ├── population_by_zip_2000.csv
│       ├── population_by_zip_2010.csv
│       ├── us_nuclear_targets.xlsx
│       └── Urban_Areas.csv
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py              # Loads and preprocesses all datasets
│   ├── preprocessing.py            # Safety mask, coverage matrix, infra scores
│   ├── blast_radius.py             # Hopkinson-Cranz blast radius calculations
│   ├── fitness.py                  # Fitness function (coverage + safety + infra)
│   ├── genetic_algo.py             # GA (selection, crossover, mutation, elitism)
│   ├── baseline.py                 # Greedy heuristic baseline
│   ├── utils.py                    # Haversine distance helpers
│   ├── main.py                     # Entry point — run this
│   └── optuna_tuning.py            # Optional: hyperparameter tuning
│
├── results/                        # Auto-generated outputs (plots, JSON)
├── requirements.txt
└── pyproject.toml
```

---

## Setup and Run

### Step 1 — Clone the repository

```bash
git clone https://github.com/MurtazaN/nuclear_shelter_location.git
cd nuclear_shelter_location
```

### Step 2 — Download the data

Download all four data files from Google Drive:

📁 **[Download Data Files](https://drive.google.com/drive/folders/1WEe_0riT-9PBuILeSj9PrpZ-Qqmdha4D?usp=sharing)**

Place them in the `data/raw/` directory. Create the folder if it doesn't exist:

```
data/raw/population_by_zip_2000.csv
data/raw/population_by_zip_2010.csv
data/raw/us_nuclear_targets.xlsx
data/raw/Urban_Areas.csv
```

### Step 3 — Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Step 4 — Install dependencies

```bash
pip install -e .
```

### Step 5 — Run the optimizer

```bash
python src/main.py
```

Results (plots, convergence data, comparison JSON) will be saved to the `results/` directory.

---

## Optional: Hyperparameter Tuning with Optuna

To run Optuna tuning before the main run:

```bash
python src/optuna_tuning.py --n-trials 30
```

This saves the best parameters to `results/optuna_best_params.json`, which `main.py` automatically loads on the next run. If no tuning has been run, `main.py` falls back to default parameters.

---

## Methodology

Candidate solutions are encoded as binary vectors over ~30,000 U.S. ZIP codes (1 = shelter placed, 0 = no shelter). Unsafe ZIP codes within the yield-scaled blast radius of any nuclear target are masked out before the GA begins.

**Fitness Function:**
```
Fitness = 0.7 × (covered_population / total_population)
        + 0.2 × mean_infrastructure_score
        - 0.1 × (num_shelters / total_candidates)
```

**GA operators:** tournament selection, uniform crossover, bit-flip mutation, elitism, adaptive mutation rate with stagnation detection.

---

## Data Sources

| Dataset | Source |
|---|---|
| U.S. ZIP-level population (2000, 2010) | U.S. Census Bureau |
| U.S. Nuclear Targets (1,087 targets) | Nuclear War Map (Christopher Minson LLC) |
| U.S. Urban Areas (3,601 areas) | The Devastator (Kaggle) |

---

## Dependencies

See `requirements.txt`. Key libraries: `numpy`, `pandas`, `scipy`, `geopandas`, `pgeocode`, `matplotlib`, `optuna`, `tqdm`, `openpyxl`.