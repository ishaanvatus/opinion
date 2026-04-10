#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <stdlib.h>
#include <math.h>
#include "pam.h"
#include "particle.h"

int main(int argc, char **argv)
{
    (void) argc;
    (void) argv;
    int width, height, planes, bit_depth;
    width = 1920;
    height = 1080;
    planes = 3;
    bit_depth = 8;
    char *filename = "sample.pam";
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
