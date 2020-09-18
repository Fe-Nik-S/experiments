#include <stdio.h>

int main()
{
    int firstNumber, secondNumber, result;
    printf("Enter two number:\n");
    scanf("%d %d", &firstNumber, &secondNumber);
    result = firstNumber + secondNumber;
    printf("%d + %d = %d\n", firstNumber, secondNumber, result);
    return 0;
}

/*
Output:

Enter two number:
15
-100
15 + -100 = -85

*/
