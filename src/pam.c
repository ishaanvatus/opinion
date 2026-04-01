#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <stdlib.h>
#include <math.h>

#include "pam.h"

/*
P7
WIDTH 227
HEIGHT 149
DEPTH 3
MAXVAL 255
TUPLTYPE RGB
ENDHDR
*/
int write_pam(FILE *fp, int width, int height, int channels, int depth, uint8_t *raster)
{
    int maxval = ((int) pow(2, depth)) - 1;

    fprintf(fp, "P7\n");
    fprintf(fp, "WIDTH %d\n", width);
    fprintf(fp, "HEIGHT %d\n", height);
    fprintf(fp, "DEPTH %d\n", channels);
    fprintf(fp, "MAXVAL %d\n", maxval);
    switch (channels) {
        case 0:
            fprintf(stderr, "Can't have 0 channels\n");
            return 1;
            break;
        case 1:
            fprintf(fp, "TUPLTYPE GRAYSCALE\n");
            break;
        case 2:
            fprintf(fp, "TUPLTYPE GRAYSCALE_ALPHA\n");
            break;
        case 3:
            fprintf(fp, "TUPLTYPE RGB\n");
            break;
        case 4:
            fprintf(fp, "TUPLTYPE RGB_ALPHA\n");
            break;
        default:
            fprintf(stderr, "%d channels is too many channels\n", channels);
            return 1;

    }
    fprintf(fp, "ENDHDR\n");
    fwrite(raster, sizeof(raster[0]), width*height*channels, fp);
    return 0;
}
