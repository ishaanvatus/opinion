#ifndef PARTICLE_H
#define PARTICLE_H 
#define BETA 0.7 //Persistence Force i.e Neighbor Influence
#define ALPHA 0.5 //Influence i.e Influence on Other Cells

struct Vector {
    double x;
    double y;
};

struct Cell {
    enum opinion {negative=-1, neutral=0, positive=1};
    struct Vector position;
    struct Vector velocity;
};

struct Swarm {
    /* Grid Size*/
    int width;
    int height;

    struct Cell *current_state;
    struct Cell *next_state;
};

int swarm_to_raster(Struct Swarm swarm, uint8_t *raster);
#endif
