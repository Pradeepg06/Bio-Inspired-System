import random
import time

# Example: 3 tasks, 1 resource with capacity 30 units
NUM_TASKS = 3
BITS_PER_TASK = 5  # allows 0-31 units per task
RESOURCE_CAPACITY = 30
MAX_ALLOCATION = (2 ** BITS_PER_TASK) - 1  # 31 units max per task

# Demands for each task
TASK_DEMANDS = [10, 12, 8]  # units needed by each task

def decode_chromosome(chromosome):
    """Split chromosome into allocations per task."""
    allocations = []
    for i in range(NUM_TASKS):
        start = i * BITS_PER_TASK
        end = start + BITS_PER_TASK
        gene = chromosome[start:end]
        alloc = int(gene, 2)
        allocations.append(alloc)
    return allocations

def fitness(chromosome):
    """Calculate fitness of allocation:

    - Penalize exceeding resource capacity.
    - Reward allocations that meet or exceed demand without waste.
    """
    allocations = decode_chromosome(chromosome)

    total_alloc = sum(allocations)
    penalty = 0
    if total_alloc > RESOURCE_CAPACITY:
        # Heavy penalty if resource capacity exceeded
        penalty += (total_alloc - RESOURCE_CAPACITY) * 10

    fitness_score = 0
    # Reward meeting demands (up to demand, no extra reward beyond demand)
    for alloc, demand in zip(allocations, TASK_DEMANDS):
        if alloc <= demand:
            fitness_score += alloc  # proportional to allocation if below demand
        else:
            # Penalize waste for allocations beyond demand
            fitness_score += demand - (alloc - demand) * 2

    # Final fitness: reward minus penalties (must be positive)
    final_score = max(fitness_score - penalty, 0)
    return final_score

def print_population(population):
    print(f"{'Chromosome':<15} | {'Allocations':<20} | {'Fitness':<7}")
    print("-" * 50)
    for chrom in population:
        alloc = decode_chromosome(chrom)
        fit = fitness(chrom)
        print(f"{chrom:<15} | {str(alloc):<20} | {fit:<7}")

def selection(population):
    fitness_values = [fitness(chrom) for chrom in population]
    total_fitness = sum(fitness_values)
    max_fitness = max(fitness_values)
    avg_fitness = total_fitness / len(population)

    if total_fitness == 0:
        prob_values = [1 / len(population)] * len(population)
    else:
        prob_values = [f / total_fitness for f in fitness_values]

    expected_output = [p * len(population) for p in prob_values]
    actual_count = [round(val) for val in expected_output]

    print("\nPopulation fitness:")
    print_population(population)

    print(f"\nSum fitness: {total_fitness}, Max fitness: {max_fitness}, Avg fitness: {avg_fitness:.2f}")

    return prob_values, expected_output, actual_count, max_fitness

def crossover(population, pool_size, bit_pos):
    mating_pool = population[:pool_size]

    print(f"\nMating Pool before crossover at bit {bit_pos}:")
    for i, chrom in enumerate(mating_pool):
        print(f"{i:<2} | {chrom}")

    for i in range(0, pool_size - 1, 2):
        chrom1 = list(mating_pool[i])
        chrom2 = list(mating_pool[i + 1])

        # Swap bit at bit_pos
        chrom1[bit_pos], chrom2[bit_pos] = chrom2[bit_pos], chrom1[bit_pos]

        mating_pool[i] = "".join(chrom1)
        mating_pool[i + 1] = "".join(chrom2)

    print(f"\nMating Pool after crossover at bit {bit_pos}:")
    for i, chrom in enumerate(mating_pool):
        print(f"{i:<2} | {chrom}")

    new_population = population.copy()
    new_population[:pool_size] = mating_pool
    return new_population

def mutation(population, mutation_rate=0.05):
    new_population = []
    print(f"\nApplying mutation with rate {mutation_rate:.2f} per bit:")

    for idx, chrom in enumerate(population):
        chrom_list = list(chrom)
        for i in range(len(chrom_list)):
            if random.random() < mutation_rate:
                # Flip bit
                chrom_list[i] = "1" if chrom_list[i] == "0" else "0"
        mutated = "".join(chrom_list)
        print(f"Chromosome {idx}: {chrom} -> {mutated}")
        new_population.append(mutated)
    return new_population

def initialize_population(num_chromosomes):
    population = []
    chromosome_length = NUM_TASKS * BITS_PER_TASK
    for _ in range(num_chromosomes):
        chrom = ''.join(random.choice('01') for _ in range(chromosome_length))
        population.append(chrom)
    return population

def main():
    print("=== Real-Time Resource Allocation GA ===")

    num_chromosomes = 6
    max_iterations = 50
    mutation_rate = 0.05
    chromosome_length = NUM_TASKS * BITS_PER_TASK

    population = initialize_population(num_chromosomes)
    print(f"Initial population (length {chromosome_length} bits):")
    print_population(population)

    max_fitness_old = -1

    for iteration in range(1, max_iterations + 1):
        print(f"\n--- Iteration {iteration} ---")

        prob_values, expected_output, actual_count, max_fitness = selection(population)

        if max_fitness == max_fitness_old or abs(max_fitness - max_fitness_old) < 1e-5:
            print("\nFitness stabilized, stopping evolution.")
            break

        max_fitness_old = max_fitness

        pool_size = random.choice([x for x in range(2, num_chromosomes + 1, 2)])
        bit_pos = random.randint(0, chromosome_length - 1)

        print(f"Selected mating pool size: {pool_size}")
        print(f"Selected bit position for crossover: {bit_pos}")

        population = crossover(population, pool_size, bit_pos)
        population = mutation(population, mutation_rate)

        time.sleep(0.3)  # simulate real-time delay

    print("\n=== Final Population ===")
    print_population(population)

if __name__ == "__main__":
    main()









'''outpt:
=== Real-Time Resource Allocation GA ===
Initial population (length 15 bits):
Chromosome      | Allocations          | Fitness
--------------------------------------------------
010011110100001 | [9, 29, 1]           | 0      
101100111110010 | [22, 15, 18]         | 0      
100100011010101 | [18, 6, 21]          | 0      
111110100111001 | [31, 9, 25]          | 0      
100101110111000 | [18, 29, 24]         | 0      
001010010000111 | [5, 4, 7]            | 16     

--- Iteration 1 ---

Population fitness:
Chromosome      | Allocations          | Fitness
--------------------------------------------------
010011110100001 | [9, 29, 1]           | 0      
101100111110010 | [22, 15, 18]         | 0      
100100011010101 | [18, 6, 21]          | 0      
111110100111001 | [31, 9, 25]          | 0      
100101110111000 | [18, 29, 24]         | 0      
001010010000111 | [5, 4, 7]            | 16     

Sum fitness: 16, Max fitness: 16, Avg fitness: 2.67
Selected mating pool size: 6
Selected bit position for crossover: 8

Mating Pool before crossover at bit 8:
0  | 010011110100001
1  | 101100111110010
2  | 100100011010101
3  | 111110100111001
4  | 100101110111000
5  | 001010010000111

Mating Pool after crossover at bit 8:
0  | 010011111100001
1  | 101100110110010
2  | 100100010010101
3  | 111110101111001
4  | 100101110111000
5  | 001010010000111

Applying mutation with rate 0.05 per bit:
Chromosome 0: 010011111100001 -> 010011101100001
Chromosome 1: 101100110110010 -> 101100100110010
Chromosome 2: 100100010010101 -> 100100010010101
Chromosome 3: 111110101111001 -> 111110101111001
Chromosome 4: 100101110111000 -> 100101110111000
Chromosome 5: 001010010000111 -> 001010011000101

--- Iteration 2 ---

Population fitness:
Chromosome      | Allocations          | Fitness
--------------------------------------------------
010011101100001 | [9, 27, 1]           | 0      
101100100110010 | [22, 9, 18]          | 0      
100100010010101 | [18, 4, 21]          | 0      
111110101111001 | [31, 11, 25]         | 0      
100101110111000 | [18, 29, 24]         | 0      
001010011000101 | [5, 6, 5]            | 16     

Sum fitness: 16, Max fitness: 16, Avg fitness: 2.67

Fitness stabilized, stopping evolution.

=== Final Population ===
Chromosome      | Allocations          | Fitness
--------------------------------------------------
010011101100001 | [9, 27, 1]           | 0      
101100100110010 | [22, 9, 18]          | 0      
100100010010101 | [18, 4, 21]          | 0      
111110101111001 | [31, 11, 25]         | 0      
100101110111000 | [18, 29, 24]         | 0      
001010011000101 | [5, 6, 5]            | 16    
'''
