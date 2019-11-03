#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void what_is_this()
{
    system("cat flag");
}

void check_passwd(char * passwd)
{
    char passwd_buf[11];
    unsigned char passwd_len = strlen(passwd);
    
    if(passwd_len>= 4 && passwd_len <= 8)
    {
        printf("Success\n");
        fflush(stdout);
        strcpy(passwd_buf,passwd);
    } 
    else 
    {
        printf("Invalid Password\n");
        fflush(stdout);
    }   
}

void login()
{
    char name[0x20];
    char passwd[0x200];
    memset(name,0,0x20);
    memset(passwd,0,0x200);

    puts("Please input your username:");
    read(0,name,0x19);
    printf("Hello %s\n", name);
    puts("Please input your passwd:");
    read(0,passwd,0x199);
    check_passwd(passwd);
}

int main()
{
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);

    int choice;
    printf("---------------------\n");
    printf("~~ Welcome to CTF! ~~\n");
    printf("       1.Login       \n");
    printf("       2.Exit        \n");
    printf("---------------------\n");
    printf("Your choice:");
    scanf("%d",&choice);
    switch(choice)
    {
        case 1:
            login();
            break;
        case 2:
            puts("Bye~");
            exit(0);
            break;
        default:
            puts("Invalid Choice!");
    }

    return 0;
}