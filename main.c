#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <stdlib.h>
#include <math.h>
#include "pam.h"

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
    int bytes_per_pixel = bit_depth / 8;
    size_t raster_byte_count =  (size_t) bytes_per_pixel*width*height*planes;
    uint8_t *raster;
    raster = malloc((size_t) raster_byte_count);
    if (raster == NULL) {
        fprintf(stderr, "couldn't allocate memory to raster\n");
        return 1;
    }
    for (int row = 0; row < height; row++) {
        for (int col = 0; col < width; col++) {
            for (int plane = 0; plane < planes; plane++) {
                int index = row*width*planes + col*planes + plane;
                raster[index] = 0x4A5387 >> (planes - plane - 1)*bit_depth;
            }
        }
    }
    write_pam(fp, width, height, planes, bit_depth, raster);
    fclose(fp);
    return 0;
}
