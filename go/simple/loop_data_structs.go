package main

import (
    "fmt"
)

func main(){
    numbers := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    sum := 0
    for index, val := range numbers {
        sum += val
        fmt.Print("[", index, ",", val, "] ")
    }
    fmt.Println("\nSum is :: ", sum)

    keyValues := map[int]string{1: "A", 2: "B", 3: "C", 4: "D"}
        for k, v := range keyValues {
        fmt.Println(k, " -> ", v)
    }

    str := "Some text!"
    for index, c := range str {
        fmt.Print("[", index, ",", string(c), "] ")
    }
}

/*
Output:

[0,1] [1,2] [2,3] [3,4] [4,5] [5,6] [6,7] [7,8] [8,9] [9,10]
Sum is ::  55
4  ->  D
1  ->  A
2  ->  B
3  ->  C
[0,S] [1,o] [2,m] [3,e] [4, ] [5,t] [6,e] [7,x] [8,t] [9,!]

*/
