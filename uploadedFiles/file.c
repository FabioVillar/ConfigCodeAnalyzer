#include <stdio.h>

int main() {
    int value = 42;

    #if RANDOM_CONDITION_1
        printf("Condition 1 is true\n");
    #else
        printf("Condition 1 is false\n");
    #endif

    #if RANDOM_CONDITION_2
        printf("Condition 2 is true\n");
    #else
        printf("Condition 2 is false\n");
    #endif

    #if RANDOM_CONDITION_3
        printf("Condition 3 is true\n");
    #else
        printf("Condition 3 is false\n");
    #endif

    return 0;
}
