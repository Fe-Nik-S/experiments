#include <stdio.h>

int main()
{
    int divident, divisor, quotient, remainder;
    printf("Enter divident and divisor:\n");
    scanf("%d %d", &divident, &divisor);

    quotient = divident/divisor;
    remainder = divident % divisor;

    printf("Quotient = %d\n", quotient);
    printf("Remainder = %d\n", remainder);
    return 0;
}

/*
Output:

Enter divident and divisor:
24
7
Quotient = 3
Remainder = 3

*/
