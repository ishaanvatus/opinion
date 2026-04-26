import numpy as np
from config import D, W, C1, C2, ALPHA, BETA, VEL_MIN, VEL_MAX, POS_MIN, POS_MAX

class CellParticle:
    def __init__(self, position, state):
        self.position              = position.copy()
        self.velocity              = np.random.uniform(VEL_MIN, VEL_MAX, D)
        self.state                 = state
        self.personal_best         = position.copy()
        self.personal_best_fitness = None

    def update_personal_best(self, fitness_fn):
        current_fitness = fitness_fn(self.position)
        if self.personal_best_fitness is None or current_fitness < self.personal_best_fitness:
            self.personal_best         = self.position.copy()
            self.personal_best_fitness = current_fitness

    def update_velocity(self, global_best):
        r1 = np.random.uniform(0, 1, D)
        r2 = np.random.uniform(0, 1, D)
        self.velocity = (W  * self.velocity
                       + C1 * r1 * (self.personal_best - self.position)
                       + C2 * r2 * (global_best        - self.position))
        self.velocity = np.clip(self.velocity, VEL_MIN, VEL_MAX)

    def update_position(self):
        self.position = np.clip(self.position + self.velocity, POS_MIN, POS_MAX)

    def update_state(self, neighbor_sum):
        phi = BETA * self.state + (1 - BETA) * ALPHA * neighbor_sum
        self.state = 1 if phi > 0 else (-1 if phi < 0 else 0)
