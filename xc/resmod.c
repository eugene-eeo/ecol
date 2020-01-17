/*
 * resmod.c
 * ========
 * Split file into chunks.
 *
 */

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

static char* USAGE = "usage: resmod <r> <m>\n";

int main(int argc, char* argv[]) {
    if (argc != 3) {
        printf("%s", USAGE);
        exit(1);
    }

    int res = atoi(argv[1]);
    int mod = atoi(argv[2]);
    int n = 0;

    // IO
    char* line = NULL;
    size_t size = 0;
    ssize_t nbytes = 0;

    while ((nbytes = getline(&line, &size, stdin)) > 0) {
        if (n == res)
            write(1, line, nbytes);
        n++;
        if (n == mod)
            n = 0;
    }
}
