# AI-Optimized Nuclear Shelter Siting (UFLP)

## Overview
This project applies Genetic Algorithm (GA) optimization to identify optimal geographic locations for nuclear shelters across the United States. The problem is framed as an Uncapacitated Facility Location Problem (UFLP). The objective is to maximize population coverage while ensuring shelters are positioned outside high-risk blast zones (15-mile exclusion radius) and near necessary infrastructure.

## Team Members
- [Your Name] - [Student ID]
- [Partner Name 2] - [Student ID] (If applicable)
- [Partner Name 3] - [Student ID] (If applicable)

## Project Structure
- `src/`: Core Python modules.
  - `data_loader.py`: Handles Census, Power Grid, and OSM data ingestion.
  - `fitness.py`: Calculates coverage, safety constraints, and accessibility scores.
  - `genetic_algo.py`: Implements the GA (Selection, Crossover, Mutation).
  - `baseline.py`: Implements the Greedy Heuristic for comparison.
  - `main.py`: Entry point for execution.
- `data/`: Storage for raw and processed datasets.
- `notebooks/`: Exploratory data analysis and visualization.
- `report/`: Drafts and final version of the project paper.

## Brief Explanation of Code
The system encodes candidate solutions as binary vectors where each bit represents a US Zip Code (1 = Shelter, 0 = No Shelter). 
1. **Initialization**: Generates random populations, masking out unsafe zones (within 15 miles of urban targets).
2. **Fitness Function**: Evaluates solutions based on total population covered within a service radius, penalizes unsafe placements, and rewards proximity to power/road infrastructure.
3. **Evolution**: Uses tournament selection, uniform crossover, and bit-flip mutation to evolve solutions over generations.
4. **Evaluation**: Compares final GA results against a Greedy Baseline heuristic.

## Tools and Dependencies
This project is built in **Python 3.9+**. Key libraries include:
- `numpy`, `pandas`: Data manipulation.
- `geopandas`, `shapely`: Spatial data handling.
- `osmnx`: Road network data.
- `matplotlib`: Visualization.

See `requirements.txt` for a full list of dependencies.

## Setup and Run

### 1. Environment Setup
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt