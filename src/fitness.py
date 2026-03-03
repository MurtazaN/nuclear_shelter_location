import numpy as np
from src.utils import haversine_distance

class FitnessFunction:
    def __init__(self, zip_codes, targets, infrastructure_scores, service_radius=50):
        self.zip_codes = zip_codes
        self.targets = targets
        self.infra_scores = infrastructure_scores
        self.service_radius = service_radius
        self.populations = zip_codes['population'].values
        self.lats = zip_codes['lat'].values
        self.lons = zip_codes['lon'].values
        
        # Pre-calculate safety mask (Hard Constraint)
        # 1 = Safe, 0 = Unsafe
        self.safety_mask = self._compute_safety_mask()

    def _compute_safety_mask(self):
        """Identify zip codes within 15-mile blast zone."""
        mask = np.ones(len(self.zip_codes), dtype=bool)
        for i in range(len(self.zip_codes)):
            for target in self.targets:
                dist = haversine_distance(self.lats[i], self.lons[i], target['lat'], target['lon'])
                if dist < 15: # 15-mile exclusion
                    mask[i] = False
                    break
        return mask

    def evaluate(self, chromosome):
        """
        Chromosome: Binary array (1 = shelter built, 0 = no shelter)
        Returns: Fitness score (Higher is better)
        """
        # 1. Hard Constraint Check: Penalty if shelter built in unsafe zone
        unsafe_placement = np.sum(chromosome * (~self.safety_mask))
        if unsafe_placement > 0:
            return -1000 * unsafe_placement # Heavy penalty

        # 2. Population Coverage
        # For each zip code, find if there is a shelter within service_radius
        total_covered_pop = 0
        selected_indices = np.where(chromosome == 1)[0]
        
        if len(selected_indices) == 0:
            return 0

        # Simplified coverage calculation (O(N*M) - optimize for final)
        for i in range(len(self.zip_codes)):
            covered = False
            for s_idx in selected_indices:
                dist = haversine_distance(self.lats[i], self.lons[i], 
                                          self.lats[s_idx], self.lons[s_idx])
                if dist <= self.service_radius:
                    covered = True
                    break
            if covered:
                total_covered_pop += self.populations[i]
        
        # 3. Infrastructure Accessibility (Average score of selected shelters)
        if len(selected_indices) > 0:
            avg_infra = np.mean(self.infra_scores[selected_indices])
        else:
            avg_infra = 0
            
        # Weighted Fitness
        # Weights can be tuned. Coverage is primary, Infra is secondary.
        fitness = (total_covered_pop / 1000) + (avg_infra * 100)
        
        return fitness