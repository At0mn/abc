#include <stdio.h>
#include <stdlib.h>

struct box
{
    char s[0x20];
    unsigned long seed;
};


unsigned long init()
{
    unsigned long seed;
    int fd;

    fd = open("/dev/urandom", 0);
    if (fd < 0 || read(fd, &seed, sizeof(seed)) < 0)
    {
        exit(1);
    }
    if (fd > 0)
    {
        close(fd);
    }
    
    return seed;
}

int get_shell()
{
    printf("You are a prophet!\nHere is your flag!");
    system("cat flag");
    return 0;
}

int main()
{
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);

    struct box Box;
    int guess_num = 0;
    int random_num = 0;

    Box.seed = init();
    printf("-------------------------------\n");
    printf("Welcome to a guess number game!\n");
    printf("-------------------------------\n");
    printf("Please let me know your name!\n");
    printf("Your name:");
    
    gets(&Box.s);
    srand(Box.seed);

    
    for(int i = 0; i < 10; i++)
    {
        random_num = rand()%6 + 1;
        printf("-------------Turn:%d-------------\n",i+1);
        printf("Please input your guess number:");
        scanf("%d",&guess_num);
        printf("---------------------------------\n");

        if(guess_num == random_num)
        {
            printf("Success!\n");
        }
        else
        {
            printf("GG!\n");
            exit(1);
        }
    }
    
    get_shell();
    return 0;
}