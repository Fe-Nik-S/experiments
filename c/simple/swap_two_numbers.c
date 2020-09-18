#include <stdio.h>

int main()
{
    double firstNumber, secondNumber, temp;
    printf("Enter two number:\n");
    scanf("%lf %lf", &firstNumber, &secondNumber);

    temp = firstNumber;
    firstNumber = secondNumber;
    secondNumber = temp;

    printf("After the swapping, A = %.2lf\n", firstNumber);
    printf("After the swapping, B = %.2lf\n", secondNumber);

    firstNumber = firstNumber - secondNumber;
    secondNumber = firstNumber + secondNumber;
    firstNumber = secondNumber - firstNumber;

    printf("After the swapping, A = %.2lf\n", firstNumber);
    printf("After the swapping, B = %.2lf\n", secondNumber);

    return 0;
}

/*
Output:

Enter two number:
17 -199
After the swapping, A = -199.00
After the swapping, B = 17.00
After the swapping, A = 17.00
After the swapping, B = -199.00

*/
