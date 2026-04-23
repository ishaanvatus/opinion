#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
#include <math.h>
#include "pam.h"
#include "particle.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "particle.h"

void swarm_init(struct Swarm *s, int width, int height) {
    s->width = width;
    s->height = height;
    s->current_state = malloc(sizeof(struct Cell) * SWARM_SIZE);
    s->next_state = malloc(sizeof(struct Cell) * SWARM_SIZE);

    s->pos_target = (struct Vector){width * 0.75, height * 0.75};
    s->neg_target = (struct Vector){width * 0.25, height * 0.25};
    s->global_best = s->pos_target; 

    for (int i = 0; i < SWARM_SIZE; i++) {
        s->current_state[i].position = (struct Vector){rand() % width, rand() % height};
        s->current_state[i].velocity = (struct Vector){0, 0};
        s->current_state[i].state = (i < 10) ? positive : neutral;
        s->current_state[i].personal_best = s->current_state[i].position;
    }
}

void swarm_update(struct Swarm *s, int curr_timestep) {
    struct Vector target = (curr_timestep < REVERSAL_TIMESTEP) ? s->pos_target : s->neg_target;
    s->global_best = target;

    for (int i = 0; i < SWARM_SIZE; i++) {
        struct Cell *c = &s->current_state[i];

        double r1 = (double)rand() / RAND_MAX;
        double r2 = (double)rand() / RAND_MAX;

        c->velocity.x = (W_INERTIA * c->velocity.x) + 
                        (C1_COGNITIVE * r1 * (c->personal_best.x - c->position.x)) + 
                        (C2_SOCIAL * r2 * (s->global_best.x - c->position.x));
        
        c->velocity.y = (W_INERTIA * c->velocity.y) + 
                        (C1_COGNITIVE * r1 * (c->personal_best.y - c->position.y)) + 
                        (C2_SOCIAL * r2 * (s->global_best.y - c->position.y));

        c->position.x += c->velocity.x;
        c->position.y += c->velocity.y;

        int neighbor_sum = 0; 
        for (int j = 0; j < SWARM_SIZE; j++) {
            if (i == j) continue; 
            double dist = sqrt(pow(c->position.x - s->current_state[j].position.x, 2) + 
                               pow(c->position.y - s->current_state[j].position.y, 2));
            if (dist < 10.0) {
                neighbor_sum += (int)s->current_state[j].state;
            }
        }

        double phi = (BETA * (int)c->state) + ((1.0 - BETA) * ALPHA * neighbor_sum);
        s->next_state[i].state = (phi > 0) ? positive : (phi < 0 ? negative : neutral);
        s->next_state[i].position = c->position;
        s->next_state[i].velocity = c->velocity;
    }

    struct Cell *temp = s->current_state;
    s->current_state = s->next_state;
    s->next_state = temp;
}
