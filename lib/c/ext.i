%module seedow

%{
#include "ext.h"
#include <stdbool.h>
%}

%feature("autodoc", "Clean a string, keeping only numbers and the '.' character.") clean_number;
extern char *clean_number(char *str);

extern bool has_substr(char *str, char *substr);
