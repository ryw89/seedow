#include <stdbool.h>
#include <string.h>

bool has_substr(char *str, char *substr) {
    if (strstr(str, substr) != NULL) {
        return true;
    }
    return false;
}
