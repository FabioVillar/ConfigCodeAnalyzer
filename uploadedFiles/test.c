#include <stdio.h>

#define NUMERO 10  
#define A 5
#define B 10
#define C 13
int main() {
    #ifdef NUMERO
        printf("A macro NUMERO está definida e seu valor é: %d\n", NUMERO);
        open();
    #else
        printf("A macro NUMERO não está definida.\n");
        close();
    #endif

    #ifndef OUTRA_MACRO
        printf("A macro OUTRA_MACRO não está definida.\n");
    #endif

    #ifdef NUMERO
        int x = 20;
        close();
    #endif

    #ifdef A
        printf("A");
        #ifdef C
            printf("A, C");
        #endif
    #elif B || NUMERO
        printf("B");
    #else
        printf("Else")
    #endif

    return 0;
}