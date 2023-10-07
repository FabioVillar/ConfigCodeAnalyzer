#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define ENABLE_FEATURE 1 

int main() {
    srand(time(NULL));

    #if ENABLE_FEATURE
        int randomNumber = rand() % 100;
        printf("Recurso habilitado. Número aleatório: %d\n", randomNumber);
    #else
        printf("Recurso desabilitado.\n");
    #endif

    if (1){
      printf("Hello world");
    }
    #if !ENABLE_FEATURE
        int x = 0;
    #endif
    return 0;
}