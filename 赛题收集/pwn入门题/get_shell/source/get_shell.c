#include <stdio.h>

int main()
{
    printf("OK,this time we will get a shell.\n");
    system("/bin/sh");
}