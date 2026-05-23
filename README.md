# Modelling Public Opinion Inversion using Particle Swarm Optimization and Cellular Automaton

## Quickstart

```bash
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python main.py
```

This generates:
- `fig4.png` -- Forward aggregation scatter plots
- `fig5.png` -- Reverse aggregation scatter plots
- `fig6.png` -- State counts over time
- `opinion_evolution.gif` -- Full animation

## Project Structure

| File | Description |
|------|-------------|
| `config.py` | Central configuration of all tunable parameters |
| `fitness.py` | PSO fitness functions $F_1$, $F_2$ |
| `particle.py` | `CellParticle` class (position, velocity, state, personal best) |
| `swarm.py` | `CellParticleSwarm` class (population, global best, reversal, step) |
| `visualise.py` | Plotting and animation utilities |
| `main.py` | Entry point: run simulation and generate all outputs |
| `Final_Report.tex` | Final project report (LaTeX) |
| `Final_Presentation.tex` | Final viva presentation (Beamer) |
| `myref.bib` | Bibliography file |

## Parameters

Key parameters in `config.py`:
- $N = 600$ -- swarm size
- $T = 30$ -- number of timesteps
- $w = 0.729$ -- PSO inertia weight
- $C_1 = C_2 = 1.494$ -- learning factors
- $\alpha = 0.5$ -- CA influence weight
- $\beta = 0.7$ -- CA persistence weight
- Flip fraction $= 0.33$ -- fraction of supporters flipped at reversal
