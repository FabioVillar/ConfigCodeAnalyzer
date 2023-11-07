
#include <stdio.h>

#define NUMERO 10  
#define A 5
#define B 10
#define C 13
int main() {
    #ifdef NUMERO
        printf("A macro NUMERO está definida e seu valor é: %d\n", NUMERO);
        open();
    #elif B
        printf("NUMERO nao esta definida e B sim")
    #else
        printf("A macro NUMERO não está definida e B tambem nao.\n");
        close();
    #endif

    #ifndef OUTRA_MACRO
        printf("A macro OUTRA_MACRO não está definida.\n");
    #endif

    #ifdef NUMERO
        int x = 20;
        close();
        #ifdef B
            print("NUMERO esta definida e B tambem");
            #ifdef C
                printf("NUMERO, B e C estao definidos");
            #endif
        #endif
    #endif

    #ifdef A
        printf("A");
        #ifdef C
		    #ifdef C > B
                printf("A, C");
            #endif
        #endif
    #elif B || NUMERO
        printf("B");
    #else
        printf("Else");
    #endif

    return 0;
}