%module seedow

%{
#include "ext.h"
#include <stdbool.h>
%}

extern bool has_substr(char *str, char *substr);
