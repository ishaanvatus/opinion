## constants taken from 10.1109/CISP-BMEI60920.2023.10373262
SEED = 42 # random value for numpy's prng
N = 600 # swarm size, aka number of cell particles/opinion agents
D = 2 # dimensions, the dimension of the space occupied by the cell particles
T = 30 # number of timesteps
REVERSAL_ITER = 8 # inflection point

W = 0.729 # inertia factor
C1 = 1.494 # cognitive learning factor 
C2 = 1.494 # social learning factor 

ALPHA =  0.5 # influence weight, effect on neighbors by cell
BETA =  0.7 # persistence force weight, effect of neighbors on cell
NEIGHBOR_RADIUS = 0.05

FLIP_FRACTION = 0.33 # the percentage of opinion individuals that change their opinion during the reversal event
INITIAL_SUPPORT = 0.10 # the percentge of initial supporters

# PSO bounds
POS_MIN         = 0.0
POS_MAX         = 1.0
VEL_MIN         = -0.1
VEL_MAX         = 0.1

# animation
GIF_FPS         = 3
GIF_PATH        = "opinion_evolution.gif"
