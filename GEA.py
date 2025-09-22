import random
import math

# Objective function to maximize
def fitness_function(x):
    return x * math.sin(10 * math.pi * x) + 1.0

# Gene Expression Algorithm
class GeneExpressionAlgorithm:
    def __init__(self, pop_size=30, generations=50, crossover_rate=0.8, mutation_rate=0.1):
        self.pop_size = pop_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.population = [random.uniform(-1, 2) for _ in range(pop_size)]  # genetic sequences

    def selection(self):
        # Tournament selection
        a, b = random.sample(self.population, 2)
        return a if fitness_function(a) > fitness_function(b) else b

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            alpha = random.random()
            return alpha * parent1 + (1 - alpha) * parent2
        return parent1

    def mutate(self, gene):
        if random.random() < self.mutation_rate:
            return gene + random.uniform(-0.1, 0.1)  # small random change
        return gene

    def run(self):
        best_solution = None
        best_fitness = float('-inf')

        for gen in range(self.generations):
            new_population = []
            for _ in range(self.pop_size):
                # Selection
                parent1 = self.selection()
                parent2 = self.selection()

                # Crossover
                offspring = self.crossover(parent1, parent2)

                # Mutation
                offspring = self.mutate(offspring)

                new_population.append(offspring)

                # Track best solution
                fit = fitness_function(offspring)
                if fit > best_fitness:
                    best_fitness = fit
                    best_solution = offspring

            self.population = new_population
            print(f"Generation {gen+1}: Best Fitness = {best_fitness:.5f}, Best Solution = {best_solution:.5f}")

        return best_solution, best_fitness


# Run GEA
gea = GeneExpressionAlgorithm(pop_size=30, generations=30)
best_sol, best_fit = gea.run()

print("\nFinal Best Solution:", best_sol)
print("Final Best Fitness:", best_fit)



#output
Generation 1: Best Fitness = 2.23378, Best Solution = 1.24561
Generation 2: Best Fitness = 2.23378, Best Solution = 1.24561
Generation 3: Best Fitness = 2.24368, Best Solution = 1.24751
Generation 4: Best Fitness = 2.24368, Best Solution = 1.24751
Generation 5: Best Fitness = 2.25032, Best Solution = 1.25119
Generation 6: Best Fitness = 2.25032, Best Solution = 1.25119
Generation 7: Best Fitness = 2.25032, Best Solution = 1.25119
Generation 8: Best Fitness = 2.25032, Best Solution = 1.25119
Generation 9: Best Fitness = 2.25032, Best Solution = 1.25119
Generation 10: Best Fitness = 2.25032, Best Solution = 1.25119
Generation 11: Best Fitness = 2.25032, Best Solution = 1.25119
Generation 12: Best Fitness = 2.25032, Best Solution = 1.25119
Generation 13: Best Fitness = 2.25038, Best Solution = 1.25102
Generation 14: Best Fitness = 2.25038, Best Solution = 1.25102
Generation 15: Best Fitness = 2.25038, Best Solution = 1.25102
Generation 16: Best Fitness = 2.25038, Best Solution = 1.25102
Generation 17: Best Fitness = 2.25040, Best Solution = 1.25084
Generation 18: Best Fitness = 2.25040, Best Solution = 1.25084
Generation 19: Best Fitness = 2.25040, Best Solution = 1.25084
Generation 20: Best Fitness = 2.25040, Best Solution = 1.25083
Generation 21: Best Fitness = 2.25040, Best Solution = 1.25083
Generation 22: Best Fitness = 2.25041, Best Solution = 1.25081
Generation 23: Best Fitness = 2.25041, Best Solution = 1.25081
Generation 24: Best Fitness = 2.25041, Best Solution = 1.25081
Generation 25: Best Fitness = 2.25041, Best Solution = 1.25081
Generation 26: Best Fitness = 2.25041, Best Solution = 1.25081
Generation 27: Best Fitness = 2.25041, Best Solution = 1.25081
Generation 28: Best Fitness = 2.25041, Best Solution = 1.25081
Generation 29: Best Fitness = 2.25041, Best Solution = 1.25081
Generation 30: Best Fitness = 2.25041, Best Solution = 1.25081

