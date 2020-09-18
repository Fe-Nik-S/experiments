#include <stdio.h>

int main()
{
    double firstNumber, secondNumber, result;
    printf("Enter two number:\n");
    scanf("%lf %lf", &firstNumber, &secondNumber);
    result = firstNumber * secondNumber;
    printf("Result = %.2lf\n", result);
    return 0;
}

/*
Output:

Enter two number:
16
3
Result = 48.00

*/
