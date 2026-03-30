# Fitness Function Factors — Nuclear Shelter Siting (UFLP)

This document outlines potential factors that can be incorporated into the fitness function for the GA-based nuclear shelter siting problem. Each factor is described with its motivation, formulation, data requirements, and expected impact on the optimization.

---

## Currently Implemented

### 1. Population Coverage
**What it measures:** The fraction of the total U.S. population that falls within the service radius (50 miles) of at least one selected shelter.

**Why it matters:** The primary objective of shelter siting is to maximize the number of people who can reach a shelter in an emergency. This is the most important factor in the fitness function.

**Formula:**
```
coverage_score = covered_population / total_population
```

**Weight:** 0.7 (highest)

**Data required:** ZIP-level population (Census), coverage adjacency matrix.

**Impact:** High — directly drives shelter placement toward densely populated areas.

---

### 2. Infrastructure Accessibility
**What it measures:** Proximity of each selected shelter to urban areas, used as a proxy for road access, utilities, and supply chains.

**Why it matters:** A shelter in a remote location with no road access or utilities is impractical regardless of population coverage. Shelters near urban infrastructure are easier to supply and reach.

**Formula:**
```
infra_score = mean over selected shelters of exp(-dist_to_nearest_urban / decay)
```

**Weight:** 0.2

**Data required:** Urban area centroids (already loaded).

**Impact:** Medium — acts as a tiebreaker between candidate sites with similar coverage scores.

---

### 3. Cost Penalty (Shelter Count)
**What it measures:** Penalizes solutions that use more shelters, encouraging efficiency.

**Why it matters:** In real facility location problems, each shelter has a construction and maintenance cost. Fewer shelters achieving the same coverage is a better solution.

**Formula:**
```
cost_penalty = num_shelters / total_candidates
```

**Weight:** -0.1 (negative — penalizes)

**Data required:** None (derived from chromosome).

**Impact:** Low — prevents the GA from trivially placing shelters everywhere.

---

## Proposed Additions

### 4. Shelter Spacing / Anti-Clustering Penalty
**What it measures:** Penalizes solutions where selected shelters are placed too close to each other (within a minimum spacing threshold, e.g. 20 miles).

**Why it matters:** Clustered shelters are redundant — they cover the same population. Real emergency planning requires geographic spread to ensure coverage across all regions, not just dense urban cores. This is a hard real-world constraint that the current fitness function does not enforce.

**Formula:**
```
pairwise_dist = haversine_distance_matrix(selected_shelters, selected_shelters)
too_close_pairs = count of pairs where dist < min_spacing_threshold
clustering_penalty = too_close_pairs / (n_shelters * (n_shelters - 1))
```

**Weight:** -0.1 to -0.2 (negative — penalizes)

**Data required:** None — uses existing `haversine_distance_matrix` from `utils.py`.

**Impact:** High — would significantly change the spatial distribution of shelters, forcing the GA to spread placements more evenly across the country and likely closing the gap with the greedy baseline.

---

### 5. Equity / Average Distance to Nearest Shelter
**What it measures:** The population-weighted average distance from every ZIP code to its nearest selected shelter. Lower is better — it means people on average don't have to travel far.

**Why it matters:** Pure coverage maximization can result in solutions that serve 99% of the population but leave rural or remote communities with no nearby shelter at all. An equity term penalizes this — it rewards solutions where shelter access is distributed fairly across all populations, not just concentrated in dense areas.

**Formula:**
```
dist_to_nearest = haversine_distance_matrix(all_zips, selected_zips).min(axis=1)
equity_score = 1 - (population_weighted_mean(dist_to_nearest) / max_possible_dist)
```

**Weight:** 0.1 to 0.2 (positive — rewards equity)

**Data required:** None — uses existing ZIP coordinates and distance functions.

**Impact:** High academic value — shifts the problem from pure efficiency maximization to fairness-aware optimization. Changes GA behavior by discouraging solutions that ignore low-density regions entirely. Adds a meaningful dimension to the comparison with the greedy baseline.

---

### 6. Blast Zone Buffer Margin
**What it measures:** Instead of a hard binary exclusion (safe/unsafe), rewards shelters that are farther from blast zones — i.e. a soft safety margin on top of the hard constraint.

**Why it matters:** A shelter placed just 16 miles from a target (just outside the 15-mile exclusion) is technically safe but highly vulnerable to secondary effects (fallout, EMP, infrastructure damage). Rewarding larger margins improves real-world safety.

**Formula:**
```
margin_score = mean over selected shelters of min_dist_to_any_target / normalization_constant
```

**Weight:** 0.05 to 0.1 (positive — rewards distance)

**Data required:** Nuclear target coordinates (already loaded).

**Impact:** Medium — would push shelters farther from urban centers (which tend to be near targets), creating an interesting tension with the coverage and infrastructure terms.

---

### 7. State-Level Coverage Balance
**What it measures:** Penalizes solutions where some states have very high coverage and others have very low coverage — encourages balanced national distribution.

**Why it matters:** A federal emergency shelter network should provide equitable coverage across all states, not just maximize aggregate national statistics. A solution that achieves 99% coverage in California but 10% in Wyoming is not a good national policy.

**Formula:**
```
per_state_coverage = covered_pop_per_state / total_pop_per_state
balance_score = 1 - std_deviation(per_state_coverage)
```

**Weight:** 0.05 to 0.1

**Data required:** State labels per ZIP code (available in Census data).

**Impact:** Medium — adds a distributional fairness constraint. Most impactful for sparsely populated states that would otherwise be ignored by coverage maximization.

---

## Summary Table

| Factor | Type | Weight | Data Needed | Implementation Effort |
|---|---|---|---|---|
| Population Coverage | Maximize | 0.7 | Census, coverage matrix | ✅ Done |
| Infrastructure Accessibility | Maximize | 0.2 | Urban areas | ✅ Done |
| Cost Penalty | Minimize | -0.1 | None | ✅ Done |
| Shelter Spacing | Minimize | -0.1 to -0.2 | None (utils.py) | Low |
| Equity / Avg Distance | Maximize | 0.1 to 0.2 | None (utils.py) | Low |
| Blast Zone Buffer Margin | Maximize | 0.05 to 0.1 | Targets (loaded) | Low |
| State-Level Balance | Maximize | 0.05 to 0.1 | Census state column | Medium |

---

## Recommendation

For the final submission, adding **Shelter Spacing** and **Equity** together would be the strongest choice:
- Both require zero new data
- They address real and distinct weaknesses in the current fitness function
- They pull the GA in a meaningfully different direction than the greedy baseline, making the comparison more interesting
- They give the paper a strong "fairness-aware optimization" narrative