package main

import (
    "fmt"
)


func main(){
    data := []int{9, 1, 8, 2, 7, 3, 6, 4, 5}
    fmt.Println("Initial array: ", data)

    BubbleSort(data, more)
    fmt.Println("Booble_sort, asc: ", data)

    BubbleSort(data, less)
    fmt.Println("Booble_sort, des: ", data)

    InsertionSort(data, more)
    fmt.Println("Insertion_sort, asc: ", data)

    InsertionSort(data, less)
    fmt.Println("Insertion_sort, des: ", data)

}

func less(value1 int, value2 int) bool {
    return value1 < value2
}

func more(value1 int, value2 int) bool {
    return value1 > value2
}

func BubbleSort(arr []int, comp func(int, int) bool) {
    size := len(arr)
    for i := 0; i < (size - 1); i++ {
        for j := 0; j < size-i-1; j++ {
            if comp(arr[j], arr[j+1]) {
                /* Swapping */
                arr[j+1], arr[j] = arr[j], arr[j+1]
            }
        }
    }
}

func InsertionSort(arr []int, comp func(int, int) bool) {
    size := len(arr)
    var temp, i, j int
    for i = 1; i < size; i++ {
        temp = arr[i]
        for j = i; j > 0 && comp(arr[j-1], temp); j-- {
            arr[j] = arr[j-1]
        }
    arr[j] = temp
    }
}

/*
Output:

Initial array:  [9 1 8 2 7 3 6 4 5]
Booble_sort, asc:  [1 2 3 4 5 6 7 8 9]
Booble_sort, des:  [9 8 7 6 5 4 3 2 1]
Insertion_sort, asc:  [1 2 3 4 5 6 7 8 9]
Insertion_sort, des:  [9 8 7 6 5 4 3 2 1]

*/
