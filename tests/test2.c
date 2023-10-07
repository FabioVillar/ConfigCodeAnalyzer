#include <stdio.h>

#define VERSION 2

int main() {
    #if VERSION == 1
        printf("This is version 1 of the program.\n");
    #elif VERSION == 2
        printf("This is version 2 of the program.\n");
    #else
        printf("This is an unknown version of the program.\n");
    #endif

    return 0;
}