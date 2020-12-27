#include <stdbool.h>
#include <string.h>

char *clean_number(char *str) {
    int i, j = 0;
    for (i = 0; str[i]; ++i) {
        if ((str[i] >= '0' && str[i] <= '9') || (str[i] == '.')) {
            str[j] = str[i];
            ++j;
        }
    }
    str[j] = '\0';
    return str;
}

bool has_substr(char *str, char *substr) {
    if (strstr(str, substr) != NULL) {
        return true;
    }
    return false;
}
