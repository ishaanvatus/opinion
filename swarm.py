import numpy as np
from config import N, D, SEED, REVERSAL_ITER, NEIGHBOR_RADIUS, FLIP_FRACTION, INITIAL_SUPPORT, POS_MIN, POS_MAX
from fitness import F1, F2
from particle import CellParticle

class CellParticleSwarm:

    def __init__(self):
        np.random.seed(SEED)
        positions = np.random.uniform(POS_MIN, POS_MAX, (N, D))
        n_support = int(N * INITIAL_SUPPORT)
        states    = [1 if i < n_support else 0 for i in range(N)]
        np.random.shuffle(states)
        self.pos_target = np.array([POS_MAX * 0.75, POS_MAX * 0.75])
        self.neg_target = np.array([POS_MIN + 0.25, POS_MIN + 0.25])
        self.particles   = [CellParticle(positions[i], states[i]) for i in range(N)]
        self.global_best = None
        self.iteration   = 0
        self.reversed    = False
        self._init_global_best()
        self.global_best = self.pos_target.copy()

    def _fitness_fn(self):
        return F1 if not self.reversed else F2

    def _init_global_best(self):
        fitness_fn = self._fitness_fn()
        for p in self.particles:
            p.personal_best_fitness = fitness_fn(p.position)
        best = min(self.particles, key=lambda p: p.personal_best_fitness)
        self.global_best = best.personal_best.copy()


    def _update_global_best(self, fitness_fn):
        if self.reversed:
            self.global_best = self.neg_target.copy()
            return
        for p in self.particles:
            if fitness_fn(p.personal_best) < fitness_fn(self.global_best):
                self.global_best = p.personal_best.copy()

    def _apply_reversal_flip(self):
        self.reversed  = True
        self.global_best = self.neg_target.copy()
        for p in self.particles:
            p.personal_best         = self.neg_target.copy()
            p.personal_best_fitness = F2(self.neg_target)
    
        supporters = [p for p in self.particles if p.state == 1]
        flip_n     = max(1, int(len(supporters) * FLIP_FRACTION))
        for p in np.random.choice(supporters, size=flip_n, replace=False):
            p.state = -1


    def _compute_neighbor_sums(self):
        positions = np.array([p.position for p in self.particles])
        states    = np.array([p.state    for p in self.particles])
        sums      = np.zeros(N)
        for i in range(N):
            dists   = np.linalg.norm(positions - positions[i], axis=1)
            mask    = (dists > 0) & (dists <= NEIGHBOR_RADIUS)
            sums[i] = np.sum(states[mask])
        return sums

    def step(self):
        fitness_fn = self._fitness_fn()

        neighbor_sums = self._compute_neighbor_sums()
        for i, p in enumerate(self.particles):
            p.update_state(neighbor_sums[i])

        if self.iteration == REVERSAL_ITER:
            self._apply_reversal_flip()

        for p in self.particles:
            p.update_personal_best(fitness_fn)
            p.update_velocity(self.global_best)
            p.update_position()

        self._update_global_best(fitness_fn)

        self.iteration += 1

    def state_counts(self):
        states = [p.state for p in self.particles]
        return {
            "neutral": states.count(0),
            "support": states.count(1),
            "suspect": states.count(-1),
        }

    def positions(self):
        return np.array([p.position for p in self.particles])

    def states(self):
        return np.array([p.state for p in self.particles])
