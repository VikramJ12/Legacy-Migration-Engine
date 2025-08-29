#include "utils.h"
#include <string.h>

void safe_strncpy(char *dest, const char *src, size_t size) {
    // Ensure null termination even if src is too long.
    strncpy(dest, src, size - 1);
    dest[size - 1] = '\0';
}