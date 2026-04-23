#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <math.h>
#include "pam.h"
#include "particle.h"

void swarm_init(struct Swarm *s, int width, int height) {
    s->width = width;
    s->height = height;
    s->current_state = malloc(sizeof(struct Cell) * SWARM_SIZE);
    s->next_state = malloc(sizeof(struct Cell) * SWARM_SIZE);

    s->pos_target = (struct Vector){width * 0.75, height * 0.75};
    s->neg_target = (struct Vector){width * 0.25, height * 0.25};
    s->global_best = s->pos_target;

    int n_supporters = SWARM_SIZE / 10;
    for (int i = 0; i < SWARM_SIZE; i++) {
        s->current_state[i].position = (struct Vector){rand() % width, rand() % height};
        s->current_state[i].velocity = (struct Vector){0, 0};
        s->current_state[i].state = (i < n_supporters) ? positive : neutral;
        s->current_state[i].personal_best = s->current_state[i].position;
    }
}

static double F1(double x, double y) {
    return (x*x*x - 1.5*x) + (y*y*y - 1.5*y);
}

static double F2(double x, double y) {
    return x + y;
}

void swarm_update(struct Swarm *s, int curr_timestep) {
    double (*fitness)(double, double) = (curr_timestep < REVERSAL_TIMESTEP) ? F1 : F2;

    if (curr_timestep == REVERSAL_TIMESTEP) {
        for (int i = 0; i < SWARM_SIZE; i++) {
            if (s->current_state[i].state == positive) {
                if ((double)rand() / RAND_MAX < 0.33) {
                    s->current_state[i].state = negative;
                }
            }
        }
    }

    for (int i = 0; i < SWARM_SIZE; i++) {
        struct Cell *c = &s->current_state[i];

        double current_fit = fitness(c->position.x, c->position.y);
        double best_fit    = fitness(c->personal_best.x, c->personal_best.y);
        if (current_fit < best_fit) {
            c->personal_best = c->position;
        }

        double r1x = (double)rand() / RAND_MAX;
        double r1y = (double)rand() / RAND_MAX;
        double r2x = (double)rand() / RAND_MAX;
        double r2y = (double)rand() / RAND_MAX;

        c->velocity.x = (W_INERTIA * c->velocity.x) +
                        (C1_COGNITIVE * r1x * (c->personal_best.x - c->position.x)) +
                        (C2_SOCIAL * r2x * (s->global_best.x - c->position.x));

        c->velocity.y = (W_INERTIA * c->velocity.y) +
                        (C1_COGNITIVE * r1y * (c->personal_best.y - c->position.y)) +
                        (C2_SOCIAL * r2y * (s->global_best.y - c->position.y));

        double max_v = 5.0;
        if (c->velocity.x >  max_v) c->velocity.x =  max_v;
        if (c->velocity.x < -max_v) c->velocity.x = -max_v;
        if (c->velocity.y >  max_v) c->velocity.y =  max_v;
        if (c->velocity.y < -max_v) c->velocity.y = -max_v;

        c->position.x += c->velocity.x;
        c->position.y += c->velocity.y;

        if (c->position.x < 0)          c->position.x = 0;
        if (c->position.x >= s->width)  c->position.x = s->width - 1;
        if (c->position.y < 0)          c->position.y = 0;
        if (c->position.y >= s->height) c->position.y = s->height - 1;

        s->next_state[i].position      = c->position;
        s->next_state[i].velocity      = c->velocity;
        s->next_state[i].personal_best = c->personal_best;
        s->next_state[i].state         = c->state;
    }

    for (int i = 0; i < SWARM_SIZE; i++) {
        int neighbor_sum = 0;
        for (int j = 0; j < SWARM_SIZE; j++) {
            if (i == j) continue;
            double dist = sqrt(pow(s->current_state[i].position.x - s->current_state[j].position.x, 2) +
                               pow(s->current_state[i].position.y - s->current_state[j].position.y, 2));
            if (dist < 10.0) neighbor_sum += (int)s->current_state[j].state;
        }
        double phi = (BETA * (int)s->current_state[i].state) +
                     ((1.0 - BETA) * ALPHA * neighbor_sum);
        s->next_state[i].state = (phi > 0) ? positive : (phi < 0 ? negative : neutral);
    }

    double best_global = fitness(s->global_best.x, s->global_best.y);
    for (int i = 0; i < SWARM_SIZE; i++) {
        double f = fitness(s->current_state[i].personal_best.x,
                           s->current_state[i].personal_best.y);
        if (f < best_global) {
            best_global    = f;
            s->global_best = s->current_state[i].personal_best;
        }
    }

    struct Cell *temp = s->current_state;
    s->current_state  = s->next_state;
    s->next_state     = temp;
}

void render_swarm_to_raster(struct Swarm *s, uint8_t *raster)
{
    int width  = s->width;
    int height = s->height;

    memset(raster, 255, width * height * 3);

    for (int i = 0; i < SWARM_SIZE; i++) {
        struct Cell *c = &s->current_state[i];

        int x = (int)c->position.x;
        int y = (int)c->position.y;

        if (x >= 0 && x < width && y >= 0 && y < height) {
            int idx = (y * width + x) * 3;

            if (c->state == positive) {
                raster[idx] = 255; raster[idx+1] = 0; raster[idx+2] = 0;
            } else if (c->state == negative) {
                raster[idx] = 0; raster[idx+1] = 255; raster[idx+2] = 0;
            } else {
                raster[idx] = 0; raster[idx+1] = 0; raster[idx+2] = 255;
            }
        }
    }
}
