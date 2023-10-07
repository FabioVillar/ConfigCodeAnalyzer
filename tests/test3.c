#include <stdio.h>

#define DEBUG 1

#ifdef DEBUG
    #define LOG(message) printf("Debug: %s\n", message)
#else
    #define LOG(message)
#endif

#define PLATFORM_LINUX 1
#define PLATFORM_WINDOWS 2
#define PLATFORM_MAC 3

#ifndef PLATFORM
    #error "Please define PLATFORM macro to specify the target platform."
#endif

int main() {
    #if PLATFORM == PLATFORM_LINUX
        LOG("Running on Linux.");
    #elif PLATFORM == PLATFORM_WINDOWS
        LOG("Running on Windows.");
    #elif PLATFORM == PLATFORM_MAC
        LOG("Running on macOS.");
    #else
        LOG("Unknown platform.");
    #endif

    return 0;
}