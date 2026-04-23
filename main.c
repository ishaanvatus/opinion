#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include "pam.h"
#include "particle.h"

int main(int argc, char **argv)
{
    (void) argc;
    (void) argv;

    srand(time(NULL));

    struct Swarm swarm;
    int width = 800;
    int height = 600;

    swarm_init(&swarm, width, height);

    printf("Starting Swarm Opinion Reversal Simulation...\n");

    for (int t = 0; t < TIMESTEPS; t++) {
        printf("Processing Timestep: %d/%d\n", t + 1, TIMESTEPS);

        swarm_update(&swarm, t);
        printf("TODO: pipe frames to ffmpeg\n");

    }

    free(swarm.current_state);
    free(swarm.next_state);

    printf("Simulation complete.\n");

    return 0;
}
