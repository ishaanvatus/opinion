from config import T
from swarm import CellParticleSwarm
from visualise import plot_fig4, plot_fig5, plot_fig6, animate

swarm    = CellParticleSwarm()
frames_X = []
frames_S = []
history  = {"neutral": [], "support": [], "suspect": []}

for t in range(T):
    swarm.step()
    frames_X.append(swarm.positions())
    frames_S.append(swarm.states())
    counts = swarm.state_counts()
    history["neutral"].append(counts["neutral"])
    history["support"].append(counts["support"])
    history["suspect"].append(counts["suspect"])

plot_fig4(frames_X, frames_S)
plot_fig5(frames_X, frames_S)
plot_fig6(history)
animate(frames_X, frames_S, history)
