import random

# Objective Function (Sphere Function)
def fitness_function(position):
    return sum(x**2 for x in position)   # minimize sum of squares

# Generate a random vector within bounds
def random_vector(dim, lb, ub):
    return [random.uniform(lb, ub) for _ in range(dim)]

# Clip position within search space boundaries
def clip(position, lb, ub):
    return [max(lb, min(ub, x)) for x in position]

# Select Alpha, Beta, Delta wolves (best 3 solutions)
def select_top_three(wolves, fitness):
    sorted_indices = sorted(range(len(fitness)), key=lambda i: fitness[i])
    alpha = wolves[sorted_indices[0]]
    beta  = wolves[sorted_indices[1]]
    delta = wolves[sorted_indices[2]]
    return alpha, beta, delta

# Grey Wolf Optimizer
def GWO(num_wolves=20, max_iter=30, dim=5, lb=-10, ub=10):
    # Step 1: Initialize population
    wolves = [random_vector(dim, lb, ub) for _ in range(num_wolves)]
    fitness = [fitness_function(w) for w in wolves]

    # Step 2: Identify Alpha, Beta, Delta
    alpha, beta, delta = select_top_three(wolves, fitness)

    # Step 3: Main loop
    for t in range(max_iter):
        a = 2 - (2 * t / max_iter)  # decreases linearly from 2 → 0

        for i in range(num_wolves):
            new_position = []
            for d in range(dim):
                r1, r2 = random.random(), random.random()
                A = 2 * a * r1 - a
                C = 2 * r2

                # Distances
                D_alpha = abs(C * alpha[d] - wolves[i][d])
                D_beta  = abs(C * beta[d]  - wolves[i][d])
                D_delta = abs(C * delta[d] - wolves[i][d])

                # Candidate positions
                X1 = alpha[d] - A * D_alpha
                X2 = beta[d]  - A * D_beta
                X3 = delta[d] - A * D_delta

                # New position = average influence
                new_position.append((X1 + X2 + X3) / 3)

            wolves[i] = clip(new_position, lb, ub)

        # Update fitness and leaders
        fitness = [fitness_function(w) for w in wolves]
        alpha, beta, delta = select_top_three(wolves, fitness)

        # Print progress
        print(f"Iteration {t+1}/{max_iter}, Best Fitness = {fitness_function(alpha):.6f}")

    return alpha, fitness_function(alpha)

# Run GWO
best_position, best_value = GWO()
print("\nBest Solution Found:")
print("Position:", best_position)
print("Fitness:", best_value)




'''output:
Iteration 1/30, Best Fitness = 106.272694
Iteration 2/30, Best Fitness = 57.739107
Iteration 3/30, Best Fitness = 6.798151
Iteration 4/30, Best Fitness = 30.884569
Iteration 5/30, Best Fitness = 11.160607
Iteration 6/30, Best Fitness = 12.614032
Iteration 7/30, Best Fitness = 3.640948
Iteration 8/30, Best Fitness = 5.108484
Iteration 9/30, Best Fitness = 9.945948
Iteration 10/30, Best Fitness = 8.301751
Iteration 11/30, Best Fitness = 2.470748
Iteration 12/30, Best Fitness = 1.831470
Iteration 13/30, Best Fitness = 1.273637
Iteration 14/30, Best Fitness = 1.348260
Iteration 15/30, Best Fitness = 1.033956
Iteration 16/30, Best Fitness = 0.426006
Iteration 17/30, Best Fitness = 0.314813
Iteration 18/30, Best Fitness = 0.069714
Iteration 19/30, Best Fitness = 0.013935
Iteration 20/30, Best Fitness = 0.004399
Iteration 21/30, Best Fitness = 0.001815
Iteration 22/30, Best Fitness = 0.001073
Iteration 23/30, Best Fitness = 0.000784
Iteration 24/30, Best Fitness = 0.000682
Iteration 25/30, Best Fitness = 0.000413
Iteration 26/30, Best Fitness = 0.000323
Iteration 27/30, Best Fitness = 0.000307
Iteration 28/30, Best Fitness = 0.000285
Iteration 29/30, Best Fitness = 0.000269
Iteration 30/30, Best Fitness = 0.000259

Best Solution Found:
Position: [0.003441191269912458, 0.008519359170539741, -0.011018253720306856, -0.007281297516036882, -0.0007071621993456097]
Fitness: 0.00025934056497106537
''' 
