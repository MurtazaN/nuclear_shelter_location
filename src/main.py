from src.data_loader import load_census_data, load_urban_targets, load_infrastructure_data
from src.fitness import FitnessFunction
from src.genetic_algo import GeneticAlgorithm
from src.baseline import greedy_heuristic # You need to create this file
import matplotlib.pyplot as plt

def main():
    # 1. Load Data
    zip_codes = load_census_data()
    targets = load_urban_targets()
    infra_scores = load_infrastructure_data()
    
    # Ensure infra scores match zip code length
    if len(infra_scores) != len(zip_codes):
        infra_scores = infra_scores[:len(zip_codes)] # Trim for mock data

    # 2. Initialize Fitness
    fitness_func = FitnessFunction(zip_codes, targets, infra_scores).evaluate

    # 3. Run Genetic Algorithm
    print("Starting Genetic Algorithm...")
    ga = GeneticAlgorithm(n_genes=len(zip_codes), fitness_func=fitness_func, 
                          pop_size=20, generations=50) # Small for testing
    best_sol, best_fit = ga.evolve()
    
    # 4. Run Baseline (Greedy)
    print("Running Greedy Baseline...")
    # greedy_sol, greedy_fit = greedy_heuristic(zip_codes, targets, infra_scores)
    
    # 5. Plot Convergence
    plt.plot(ga.history)
    plt.title("GA Convergence")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.savefig("convergence_plot.png")
    print("Results saved. Check convergence_plot.png")

if __name__ == "__main__":
    main()