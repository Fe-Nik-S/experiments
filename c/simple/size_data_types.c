#include <stdio.h>

int main()
{
    int intType;
    float floatType;
    double doubleType;
    char charType;

    long longType;
    long long longTwiceType;
    long double longDoubleType;

    printf("Size of int = %ld bytes\n", sizeof(intType));
    printf("Size of float = %ld bytes\n", sizeof(floatType));
    printf("Size of double = %ld bytes\n", sizeof(doubleType));
    printf("Size of char = %ld bytes\n", sizeof(charType));

    printf("Size of long = %ld bytes\n", sizeof(longType));
    printf("Size of long long = %ld bytes\n", sizeof(longTwiceType));
    printf("Size of long double = %ld bytes\n", sizeof(longDoubleType));
    return 0;
}

/*
Output:

Size of int = 4 bytes
Size of float = 4 bytes
Size of double = 8 bytes
Size of char = 1 bytes
Size of long = 8 bytes
Size of long long = 8 bytes
Size of long double = 16 bytes

*/
