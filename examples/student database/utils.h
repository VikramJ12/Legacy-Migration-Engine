#ifndef UTILS_H
#define UTILS_H

#include <stddef.h>

// A utility function to safely copy strings.
void safe_strncpy(char *dest, const char *src, size_t size);

#endif // UTILS_H