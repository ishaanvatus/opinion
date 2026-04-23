#ifndef PARTICLE_H
#define PARTICLE_H 

#define SWARM_SIZE 600
/*
//  Parameters taken from IEEE 10373262, todo: use scraped data and use crossing point 
//  (sentiment analysis, opinion turns from +ve to -ve) for reversal timestep 
//  and total timeline of the event for total timesteps
*/
#define BETA 0.7 //Persistence Force i.e Neighbor Influence
#define ALPHA 0.5 //Influence i.e Influence on Other Cells
#define REVERSAL_TIMESTEP 8
#define TIMESTEPS 30

#define W_INERTIA 0.8
#define C1_COGNITIVE 2.0
#define C2_SOCIAL 2.0

enum Opinion {negative=-1, neutral=0, positive=1};
struct Vector {
    double x;
    double y;
};

struct Cell {
    enum Opinion state;
    struct Vector position;
    struct Vector velocity;
    struct Vector personal_best;
};

struct Swarm {
    /* Grid Size*/
    int width;
    int height;
    struct Vector global_best;
    struct Vector pos_target; //global hotspot for +1 
    struct Vector neg_target; //global hotspot for -1 
    struct Cell *current_state;
    struct Cell *next_state;
};
void swarm_init(struct Swarm *s, int width, int height);
void swarm_update(struct Swarm *s, int curr_timestep);
#endif
