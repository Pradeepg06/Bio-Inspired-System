import numpy as np
import random
import matplotlib.pyplot as plt

class AntColony:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=2):
        """
        distances: 2D numpy array (distance matrix between cities)
        n_ants: number of ants per iteration
        n_best: number of best ants that deposit pheromone
        n_iterations: number of iterations
        decay: pheromone evaporation rate (rho)
        alpha: importance of pheromone
        beta: importance of heuristic (1/distance)
        """
        self.distances = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        all_time_shortest_path = (None, np.inf)
        
        for i in range(self.n_iterations):
            all_paths = self.construct_colony_paths()
            self.spread_pheromone(all_paths, self.n_best)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            # Evaporation
            self.pheromone *= (1 - self.decay)
        
        return all_time_shortest_path

    def construct_colony_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.construct_solution(0)  # start from city 0
            all_paths.append((path, self.path_distance(path)))
        return all_paths

    def construct_solution(self, start):
        path = []
        visited = set([start])
        prev = start
        for _ in range(len(self.distances) - 1):
            move = self.pick_next_city(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))  # return to start
        return path

    def pick_next_city(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        # Heuristic = 1 / distance (avoid div by zero)
        with np.errstate(divide='ignore'):
            heuristic = 1.0 / dist
        heuristic[dist == 0] = 0

        row = (pheromone ** self.alpha) * (heuristic ** self.beta)

        if row.sum() == 0:
            # fallback: choose randomly among unvisited
            choices = list(set(self.all_inds) - visited)
            return random.choice(choices)

        norm_row = row / row.sum()
        return np.random.choice(self.all_inds, 1, p=norm_row)[0]

    def spread_pheromone(self, all_paths, n_best):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / dist

    def path_distance(self, path):
        return sum(self.distances[edge] for edge in path)


# ---- Example Usage ----
if __name__ == "__main__":
    # Define cities (coordinates)
    cities = np.array([
        [0, 0], [1, 5], [5, 2], [7, 8], [8, 3]
    ])

    # Distance matrix
    n_cities = len(cities)
    distances = np.zeros((n_cities, n_cities))
    for i in range(n_cities):
        for j in range(n_cities):
            if i == j:
                distances[i][j] = np.inf
            else:
                distances[i][j] = np.linalg.norm(cities[i] - cities[j])

    # Run ACO
    ant_colony = AntColony(distances, n_ants=10, n_best=5, n_iterations=100, decay=0.5, alpha=1, beta=2)
    best_path, best_distance = ant_colony.run()

    print("Best Path:", best_path)
    print("Best Distance:", best_distance)

    # ---- Visualization ----
    plt.figure(figsize=(6,6))
    for (i, j) in best_path:
        plt.plot([cities[i][0], cities[j][0]], [cities[i][1], cities[j][1]], 'b-')
    plt.scatter(cities[:,0], cities[:,1], c='red', s=100)
    for idx, (x,y) in enumerate(cities):
        plt.text(x+0.1, y+0.1, str(idx), fontsize=12)
    plt.title(f"Best TSP Path (Distance = {best_distance:.2f})")
    plt.show()


#output
Best Path: [(0, 1), (1, 3), (3, 4), (4, 2), (2, 0)]
Best Distance: 25.45368542698782
