import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D
from config import T, N, REVERSAL_ITER, POS_MIN, POS_MAX, GIF_FPS, GIF_PATH

COLOR_MAP = {0: "blue", 1: "red", -1: "green"}

def scatter_at(ax, frames_X, frames_S, frame, title):
    ax.set_xlim(POS_MIN, POS_MAX)
    ax.set_ylim(POS_MIN, POS_MAX)
    ax.set_title(title, fontsize=9)
    ax.set_xlabel("X(pos)", fontsize=7)
    ax.set_ylabel("Y(pos)", fontsize=7)
    ax.scatter(frames_X[frame][:, 0], frames_X[frame][:, 1],
               c=[COLOR_MAP[s] for s in frames_S[frame]], s=4, alpha=0.7)

def plot_fig4(frames_X, frames_S):
    fig, axes = plt.subplots(2, 2, figsize=(8, 8))
    for ax, (frame, label) in zip(axes.flat,
            [(0, "Iteration 1"), (2, "Iteration 3"),
             (4, "Iteration 5"), (6, "Iteration 7")]):
        scatter_at(ax, frames_X, frames_S, frame, label)
    fig.suptitle("Fig 4 — Forward view aggregation", fontsize=11)
    plt.tight_layout()
    plt.savefig("fig4.png", dpi=150)
    plt.close()
    print("Saved fig4.png")

def plot_fig5(frames_X, frames_S):
    fig, axes = plt.subplots(2, 2, figsize=(8, 8))
    for ax, (frame, label) in zip(axes.flat,
            [(10, "Iteration 11"), (14, "Iteration 15"),
             (19, "Iteration 20"), (29, "Iteration 30")]):
        scatter_at(ax, frames_X, frames_S, frame, label)
    fig.suptitle("Fig 5 — Reverse view aggregation", fontsize=11)
    plt.tight_layout()
    plt.savefig("fig5.png", dpi=150)
    plt.close()
    print("Saved fig5.png")

def plot_fig6(history):
    iters = list(range(T))
    plt.figure(figsize=(8, 5))
    plt.plot(iters, history["neutral"], color="gray",  label="Neutralist", lw=2)
    plt.plot(iters, history["support"], color="red",   label="Supporter",  lw=2)
    plt.plot(iters, history["suspect"], color="green", label="Skeptic",    lw=2)
    plt.axvline(x=REVERSAL_ITER, color="orange", linestyle=":", lw=1.5, label="Reversal")
    plt.xlabel("Iteration")
    plt.ylabel("Number of particles")
    plt.title("Fig 6 — State counts over time")
    plt.legend()
    plt.tight_layout()
    plt.savefig("fig6.png", dpi=150)
    plt.close()
    print("Saved fig6.png")

def animate(frames_X, frames_S, history):
    iters = list(range(T))

    fig, (ax_scatter, ax_line) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Cell Particle Swarm — Opinion Evolution", fontsize=13)

    ax_scatter.set_xlim(POS_MIN, POS_MAX)
    ax_scatter.set_ylim(POS_MIN, POS_MAX)
    ax_scatter.set_xlabel("X(pos)")
    ax_scatter.set_ylabel("Y(pos)")
    ax_scatter.legend(handles=[
        Line2D([0],[0], marker="o", color="w", markerfacecolor="blue",  markersize=8, label="Neutral"),
        Line2D([0],[0], marker="o", color="w", markerfacecolor="red",   markersize=8, label="Supporter"),
        Line2D([0],[0], marker="o", color="w", markerfacecolor="green", markersize=8, label="Skeptic"),
    ], loc="lower right", fontsize=8)

    scat       = ax_scatter.scatter([], [], s=8, alpha=0.7)
    iter_text  = ax_scatter.text(0.02, 0.96, "", transform=ax_scatter.transAxes, fontsize=10, va="top")
    phase_text = ax_scatter.text(0.02, 0.90, "", transform=ax_scatter.transAxes, fontsize=9,  va="top", color="purple")

    line_n, = ax_line.plot([], [], color="gray",  label="Neutral",   lw=2)
    line_s, = ax_line.plot([], [], color="red",   label="Supporter", lw=2)
    line_k, = ax_line.plot([], [], color="green", label="Skeptic",   lw=2)
    vline    = ax_line.axvline(x=0, color="purple", linestyle="--", lw=1, alpha=0.6)

    ax_line.set_xlim(0, T - 1)
    ax_line.set_ylim(0, N + 20)
    ax_line.set_xlabel("Iteration")
    ax_line.set_ylabel("Number of particles")
    ax_line.set_title("State counts over time")
    ax_line.legend(fontsize=8)
    ax_line.axvline(x=REVERSAL_ITER, color="orange", linestyle=":", lw=1.5, alpha=0.8)

    def update(frame):
        scat.set_offsets(frames_X[frame])
        scat.set_color([COLOR_MAP[s] for s in frames_S[frame]])
        iter_text.set_text(f"Iteration: {frame + 1}")
        phase_text.set_text("Forward aggregation" if frame < REVERSAL_ITER else "Reverse aggregation")
        line_n.set_data(iters[:frame + 1], history["neutral"][:frame + 1])
        line_s.set_data(iters[:frame + 1], history["support"][:frame + 1])
        line_k.set_data(iters[:frame + 1], history["suspect"][:frame + 1])
        vline.set_xdata([frame, frame])
        return scat, iter_text, phase_text, line_n, line_s, line_k, vline

    ani = animation.FuncAnimation(fig, update, frames=T, interval=400, blit=True)
    plt.tight_layout()
    ani.save(GIF_PATH, writer="pillow", fps=GIF_FPS, dpi=120)
    print(f"Saved {GIF_PATH}")
    plt.show()
