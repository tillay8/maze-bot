#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <png.h>
#include <string.h>

#define SIDE 0
#define START 1
#define PATH 2
#define END 3

int isPossible(int *field, int x, int y, int val, int W, int H);
void createMaze(int *field, int W, int H);
void fill(int *field, int ox, int oy, int nx, int ny, int W);
void createImage(const char *file, int *field, int W, int H, int Scale);

int main(int argc, char *argv[]) {
    if (argc < 3 || argc > 4) {
        fprintf(stderr, "Usage: %s <size> <output_file>\n", argv[0]);
        return 1;
    }
    int W = atoi(argv[1]);
    if (W % 2 == 0) {
        W++;
    }

    int H = W;
    int Scale = (W < 100) ? 10 : (W < 200) ? 8 : (W < 300) ? 6 : (W < 400) ? 4 : 1;

    FILE *logFile = fopen("mazebot.log", "a");
    if (logFile) {
        fprintf(logFile, "\nScale: %d Size: %d\n", Scale, W - 1);
        fclose(logFile);
    }

    int *field = (int *)malloc(W * H * sizeof(int));
    if (!field) {
        return 1;
    }

    clock_t start = clock();
    createMaze(field, W, H);
    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;

    logFile = fopen("mazebot.log", "a");
    if (logFile) {
        fprintf(logFile, "Time to path maze: %.2f seconds\n", time_spent);
        fclose(logFile);
    }

    createImage(argv[2], field, W, H, Scale);

    logFile = fopen("mazebot.log", "a");
    if (logFile) {
        fprintf(logFile, "Saved image to %s", argv[2]);
        fclose(logFile);
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

void createMaze(int *field, int W, int H) {
    srand(time(NULL));

    int (*history)[2] = malloc(W * H * sizeof(int[2]));
    if (!history) {
        return;
    }

    int historySize = 0;
    int pos[2] = {0, 0};

    for (int i = 0; i < W * H; i++) {
        field[i] = 0;
    }

    field[0] = 1;
    history[historySize][0] = 0;
    history[historySize][1] = 0;
    historySize++;

    while (historySize > 0) {
        int possible[4][2];
        int possibleCount = 0;

        int directions[4][2] = {{0, -2}, {0, 2}, {-2, 0}, {2, 0}};
        for (int i = 0; i < 4; i++) {
            int nx = pos[0] + directions[i][0];
            int ny = pos[1] + directions[i][1];
            if (isPossible(field, nx, ny, 1, W, H)) {
                possible[possibleCount][0] = nx;
                possible[possibleCount][1] = ny;
                possibleCount++;
            }
        }

        if (possibleCount == 0) {
            historySize--;
            if (historySize > 0) {
                pos[0] = history[historySize - 1][0];
                pos[1] = history[historySize - 1][1];
            }
            continue;
        }

        int choice = rand() % possibleCount;
        int nx = possible[choice][0];
        int ny = possible[choice][1];

        field[ny * W + nx] = 1;
        fill(field, pos[0], pos[1], nx, ny, W);

        pos[0] = nx;
        pos[1] = ny;

        history[historySize][0] = pos[0];
        history[historySize][1] = pos[1];
        historySize++;
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

void createImage(const char *file, int *field, int W, int H, int Scale) {
    FILE *fp = fopen(file, "wb");
    if (!fp) {
        return;
    }

    png_structp png = png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
    if (!png) {
        fclose(fp);
        return;
    }

    png_infop info = png_create_info_struct(png);
    if (!info) {
        png_destroy_write_struct(&png, NULL);
        fclose(fp);
        return;
    }

    if (setjmp(png_jmpbuf(png))) {
        png_destroy_write_struct(&png, &info);
        fclose(fp);
        return;
    }

    png_init_io(png, fp);

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
        png_destroy_write_struct(&png, &info);
        fclose(fp);
        return;
    }

    for (int y = 0; y < H + 2; y++) {
        for (int i = 0; i < Scale; i++) {
            for (int x = 0; x < W + 2; x++) {
                unsigned char color[3];
                if (x == 0 || y == 0 || x == W + 1 || y == H + 1) {
                    color[0] = 0; color[1] = 0; color[2] = 0;
                } else if (x == 1 && y == 1) {
                    color[0] = 255; color[1] = 0; color[2] = 0;
                } else if (x == W && y == H) {
                    color[0] = 0; color[1] = 0; color[2] = 255;
                } else {
                    int val = field[(x - 1) + (y - 1) * W];
                    color[0] = val == 0 ? 0 : 255;
                    color[1] = val == 0 ? 0 : 255;
                    color[2] = val == 0 ? 0 : 255;
                }

                for (int j = 0; j < Scale; j++) {
                    row[(x * Scale + j) * 3 + 0] = color[0];
                    row[(x * Scale + j) * 3 + 1] = color[1];
                    row[(x * Scale + j) * 3 + 2] = color[2];
                }
            }
            png_write_row(png, row);
        }
    }

    png_write_end(png, NULL);
    free(row);
    png_destroy_write_struct(&png, &info);
    fclose(fp);
}
