#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char **argv)
{
    if (argc < 4) {
        fprintf(stderr, "Program Usage: ./main <w> <h> <planes> <depth> <filename>\n");
        return 1;
    }
    char *filename = argv[5]; 
    int width, height, planes, bit_depth;
    int maxval = ((int) pow(2, bit_depth)) - 1;
    width = atoi(argv[1]);
    height = atoi(argv[2]);
    planes = atoi(argv[3]);
    bit_depth = atoi(argv[4]);
    FILE *fp = fopen(filename, "w");
    if (fp == NULL) {
        fprintf(stderr, "Error opening file \"%s\": \n", filename);
        return 1;
    }
    /*
    P7
    WIDTH 227
    HEIGHT 149
    DEPTH 3
    MAXVAL 255
    TUPLTYPE RGB
    ENDHDR
    */
    fprintf(fp, "P7\n");
    fprintf(fp, "WIDTH %d\n", width);
    fprintf(fp, "HEIGHT %d\n", height);
    fprintf(fp, "DEPTH %d\n", planes);
    fprintf(fp, "MAXVAL %d\n", maxval);
    switch (planes) {
        case 0:
            fprintf(stderr, "Can't have 0 planes\n");
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
            fprintf(stderr, "%d planes is too many planes\n", planes);
            return 1;

    }
    fprintf(fp, "ENDHDR\n");
    for (int row = 0; row < height; row++) {
        for (int col = 0; col < width; col++) {
            for (int plane = 0; plane < planes; plane++) {
                uint8_t gray = rand()%256;
                fwrite(&gray, sizeof(gray), 1, fp);
            }
        }
    }
    return 0;
}
