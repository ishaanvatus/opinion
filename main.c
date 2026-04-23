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
    int width = 192;
    int height = 108;
    uint8_t *raster = malloc(width * height * 3);
    if (raster == NULL) {
        fprintf(stderr, "Failed to memory to raster\n");
        return -1;
    }
    swarm_init(&swarm, width, height);

    for (int t = 0; t < TIMESTEPS; t++) {
        swarm_update(&swarm, t);
        render_swarm_to_raster(&swarm, raster);
    
        write_pam(stdout, width, height, 3, 8, raster);
    }

    free(swarm.current_state);
    free(swarm.next_state);

    return 0;
}
