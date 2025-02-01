#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <png.h>
#include <string.h>

// Maze colors
#define SIDE 0
#define START 1
#define PATH 2
#define END 3

// Function declerations
int isPossible(int *field, int x, int y, int val, int W, int H);
void createMaze(int *field, int W, int H, int verbose);
void fill(int *field, int ox, int oy, int nx, int ny, int W);
void createImage(const char *file, int *field, int W, int H, int Scale, int verbose);

int main(int argc, char *argv[]) {
    if (argc < 3 || argc > 4) {
        printf("Usage: %s <size> <output_file> \n", argv[0]);
        return 1;
    }

    int verbose = (argc == 4 && strcmp(argv[3], "-v") == 0);

    if (verbose) {
        printf("Maze request received\n");
        fflush(stdout);
    }

    int W = atoi(argv[1]);
    int H = W;
    int Scale = (W < 100) ? 10 : (W < 200) ? 5 : 1;

    if (verbose) {
        printf("Scale: %d Size: %d\n", Scale, W);
        fflush(stdout);
    }

    int *field = (int *)malloc(W * H * sizeof(int));
    if (!field) {
        printf("Not enough memory: what crap PC are you on??\n");
        fflush(stdout);
        return 1;
    }

    clock_t start = clock();
    createMaze(field, W, H, verbose);
    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;

    if (verbose) {
        printf("Pathing maze complete\n");
        fflush(stdout);
    }

    createImage(argv[2], field, W, H, Scale, verbose);

    if (verbose) {
        printf("Saved image to %s\n", argv[2]);
        printf("Time to generate and path maze: %.2f seconds\n", time_spent);
        fflush(stdout);
    }

    free(field);
    return 0;
}

int isPossible(int *field, int x, int y, int val, int W, int H) {
    if (x < 0 || y < 0 || x >= W || y >= H) {
        return 0;
    }
    return (val == 1) ? (field[y * W + x] != 1) : (field[y * W + x] == 1);
}

void createMaze(int *field, int W, int H, int verbose) {
    srand(time(NULL));

    int (*history)[2] = malloc(W * H * sizeof(int[2]));
    if (!history) {
        printf("Failed to allocate memory for history\n");
        fflush(stdout);
        return;
    }

    int historySize = 0;
    int pos[2] = {0, 0};

    while (1) {
        int possible[4][2];
        int possibleCount = 0;

        int up[2] = {pos[0], pos[1] - 2};
        int down[2] = {pos[0], pos[1] + 2};
        int left[2] = {pos[0] - 2, pos[1]};
        int right[2] = {pos[0] + 2, pos[1]};

        if (isPossible(field, up[0], up[1], 1, W, H)) {
            possible[possibleCount][0] = up[0];
            possible[possibleCount][1] = up[1];
            possibleCount++;
        }
        if (isPossible(field, down[0], down[1], 1, W, H)) {
            possible[possibleCount][0] = down[0];
            possible[possibleCount][1] = down[1];
            possibleCount++;
        }
        if (isPossible(field, left[0], left[1], 1, W, H)) {
            possible[possibleCount][0] = left[0];
            possible[possibleCount][1] = left[1];
            possibleCount++;
        }
        if (isPossible(field, right[0], right[1], 1, W, H)) {
            possible[possibleCount][0] = right[0];
            possible[possibleCount][1] = right[1];
            possibleCount++;
        }

        if (possibleCount == 0) {
            if (historySize == 0) {
                if (verbose) {
                    printf("Finished generating maze\n");
                    fflush(stdout);
                }
                free(history);
                return;
            }
            pos[0] = history[historySize - 1][0];
            pos[1] = history[historySize - 1][1];
            historySize--;
            continue;
        }

        history[historySize][0] = pos[0];
        history[historySize][1] = pos[1];
        historySize++;

        int choice = rand() % possibleCount;
        pos[0] = possible[choice][0];
        pos[1] = possible[choice][1];
        field[pos[1] * W + pos[0]] = 1;
        fill(field, history[historySize - 1][0], history[historySize - 1][1], pos[0], pos[1], W);
    }

    free(history);
}

void fill(int *field, int ox, int oy, int nx, int ny, int W) {
    if (ox != nx) {
        field[oy * W + ((nx - ox) / 2) + ox] = 1;
    } else {
        field[((ny - oy) / 2 + oy) * W + ox] = 1;
    }
}

void createImage(const char *file, int *field, int W, int H, int Scale, int verbose) {
    if (verbose) {
        printf("Generating image...\n");
        fflush(stdout);
    }

    FILE *fp = fopen(file, "wb");
    if (!fp) {
        printf("Unable to open file (server side error)\n");
        fflush(stdout);
        return;
    }

    png_structp png = png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
    if (!png) {
        printf("Unable to make png (unknown reason)\n");
        fflush(stdout);
        fclose(fp);
        return;
    }

    png_infop info = png_create_info_struct(png);
    if (!info) {
        printf("Unable to make png (unknown reason)\n");
        fflush(stdout);
        png_destroy_write_struct(&png, NULL);
        fclose(fp);
        return;
    }

    if (setjmp(png_jmpbuf(png))) {
        printf("Error during PNG creation\n");
        fflush(stdout);
        png_destroy_write_struct(&png, &info);
        fclose(fp);
        return;
    }

    png_init_io(png, fp);

    // Set image dimensions (scaled)
    int scaledWidth = (W + 2) * Scale;
    int scaledHeight = (H + 2) * Scale;

    png_set_IHDR(
        png,
        info,
        scaledWidth,
        scaledHeight,
        8,
        PNG_COLOR_TYPE_RGB,
        PNG_INTERLACE_NONE,
        PNG_COMPRESSION_TYPE_DEFAULT,
        PNG_FILTER_TYPE_DEFAULT
    );

    png_write_info(png, info);

    png_bytep row = (png_bytep)malloc(3 * scaledWidth * sizeof(png_byte));
    if (!row) {
        printf("Failed to allocate memory for PNG\n");
        fflush(stdout);
        png_destroy_write_struct(&png, &info);
        fclose(fp);
        return;
    }

    // Write image data
    for (int y = 0; y < H + 2; y++) {
        for (int i = 0; i < Scale; i++) { // Repeat each row `Scale` times
            for (int x = 0; x < W + 2; x++) {
                unsigned char color[3];
                if (x == 0 || y == 0 || x == W + 1 || y == H + 1) {
                    color[0] = 0; color[1] = 0; color[2] = 0; // SIDE (black)
                } else if (x == 1 && y == 1) {
                    color[0] = 255; color[1] = 0; color[2] = 0; // START (red)
                } else if (x == W && y == H) {
                    color[0] = 0; color[1] = 0; color[2] = 255; // END (blue)
                } else {
                    int val = field[(x - 1) + (y - 1) * W];
                    color[0] = val == 0 ? 0 : 255;
                    color[1] = val == 0 ? 0 : 255;
                    color[2] = val == 0 ? 0 : 255;
                }

                // Repeat each pixel Scale times
                for (int j = 0; j < Scale; j++) {
                    row[(x * Scale + j) * 3 + 0] = color[0]; // Red
                    row[(x * Scale + j) * 3 + 1] = color[1]; // Green
                    row[(x * Scale + j) * 3 + 2] = color[2]; // Blue
                }
            }
            png_write_row(png, row);
        }
    }

    png_write_end(png, NULL);
    free(row);
    png_destroy_write_struct(&png, &info);
    fclose(fp);

    if (verbose) {
        printf("Exporting image...\n");
        fflush(stdout);
    }
}
