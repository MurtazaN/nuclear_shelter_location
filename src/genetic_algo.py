import numpy as np
import random

class GeneticAlgorithm:
    def __init__(self, n_genes, fitness_func, pop_size=50, generations=100, 
                 mutation_rate=0.05, crossover_rate=0.8):
        self.n_genes = n_genes
        self.fitness_func = fitness_func
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = np.random.randint(0, 2, (pop_size, n_genes))
        self.best_solution = None
        self.best_fitness = -np.inf
        self.history = []

    def select(self, scores):
        """Tournament Selection"""
        selected = []
        for _ in range(self.pop_size):
            i, j = random.sample(range(self.pop_size), 2)
            if scores[i] > scores[j]:
                selected.append(self.population[i])
            else:
                selected.append(self.population[j])
        return np.array(selected)

    def crossover(self, parent1, parent2):
        """Uniform Crossover"""
        if random.random() > self.crossover_rate:
            return parent1, parent2
        
        mask = np.random.randint(0, 2, self.n_genes).astype(bool)
        child1 = np.where(mask, parent1, parent2)
        child2 = np.where(mask, parent2, parent1)
        return child1, child2

    def mutate(self, individual):
        """Bit Flip Mutation"""
        for i in range(self.n_genes):
            if random.random() < self.mutation_rate:
                individual[i] = 1 - individual[i]
        return individual

    def evolve(self):
        for gen in range(self.generations):
            scores = np.array([self.fitness_func(ind) for ind in self.population])
            
            # Track Best
            max_score_idx = np.argmax(scores)
            if scores[max_score_idx] > self.best_fitness:
                self.best_fitness = scores[max_score_idx]
                self.best_solution = self.population[max_score_idx].copy()
            
            self.history.append(self.best_fitness)
            
            # Selection
            new_pop = self.select(scores)
            
            # Crossover & Mutation
            for i in range(0, self.pop_size, 2):
                p1, p2 = new_pop[i], new_pop[i+1]
                c1, c2 = self.crossover(p1, p2)
                new_pop[i] = self.mutate(c1)
                if i+1 < self.pop_size:
                    new_pop[i+1] = self.mutate(c2)
            
            self.population = new_pop
            print(f"Generation {gen}: Best Fitness = {self.best_fitness}")
            
        return self.best_solution, self.best_fitness