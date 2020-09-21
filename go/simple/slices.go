package main

import "fmt"

var (
    outputTemplate = "Len: %d; Cap: %d; Address: %p"
)

type MyArray []int

func (array MyArray) ToString() {
    var arrayInfo = fmt.Sprintf(outputTemplate, len(array), cap(array), &array)
    fmt.Print(arrayInfo)
    fmt.Print("; Data: ")
    for key, val := range array {
        fmt.Printf("[%d|%d] ", key, val)
    }
    fmt.Print("\n")
}

func (array *MyArray) ToStringByP() {
    var arrayInfo = fmt.Sprintf(outputTemplate, len(*array), cap(*array), array)
    fmt.Print(arrayInfo)
    fmt.Print("; Data: ")
    for key, val := range *array {
        fmt.Printf("[%d|%d] ", key, val)
    }
    fmt.Print("\n")
}

func main() {
    fmt.Println("Init a base slice:")
    data := MyArray{9, 1, 8, 2, 7, 3, 6, 4, 5}
    var arrayInfo = fmt.Sprintf(outputTemplate, len(data), cap(data), &data)
    fmt.Println(arrayInfo)
    data.ToString()
    data.ToStringByP()

    fmt.Println("\nAppend new elements to data:")
    data1 := append(data, 15, 20)
    data1.ToString()
    data.ToString()

    fmt.Println("\nMade new empty slice:")
    data2 := make(MyArray, 0, 5)
    data2.ToString()

    fmt.Println("\nAppend new elements to data2:")
    data2 = append(data2, 0)
    data2.ToString()

    fmt.Println("\nAppend new elements to data2->data3:")
    data3 := append(data2, 2, 4, 6)
    data3.ToString()

    fmt.Println("\nAppend new elements to data2->data4:")
    data4 := append(data2, []int{1, 2, 3, 4, 5}...)
    data4.ToString()

    fmt.Println("\nCopy elements to data4:")
    copy(data4, []int{100, 200, -1, 300})
    data4.ToString()

    fmt.Println("\nCopy elements to data4 in custom position:")
    copy(data4[1:], []int{0, 100, -1, 200, -2, 300, -3})
    data4.ToString()
}



/*
Output:

Init a base slice:
Len: 9; Cap: 9; Address: 0xc00000a080
Len: 9; Cap: 9; Address: 0xc00000a0a0; Data: [0|9] [1|1] [2|8] [3|2] [4|7] [5|3] [6|6] [7|4] [8|5]
Len: 9; Cap: 9; Address: 0xc00000a080; Data: [0|9] [1|1] [2|8] [3|2] [4|7] [5|3] [6|6] [7|4] [8|5]

Append new elements to data:
Len: 11; Cap: 18; Address: 0xc00000a0c0; Data: [0|9] [1|1] [2|8] [3|2] [4|7] [5|3] [6|6] [7|4] [8|5] [9|15] [10|20]
Len: 9; Cap: 9; Address: 0xc00000a0e0; Data: [0|9] [1|1] [2|8] [3|2] [4|7] [5|3] [6|6] [7|4] [8|5]

Made new empty slice:
Len: 0; Cap: 5; Address: 0xc00000a100; Data:

Append new elements to data2:
Len: 1; Cap: 5; Address: 0xc00000a120; Data: [0|0]

Append new elements to data2->data3:
Len: 4; Cap: 5; Address: 0xc00000a140; Data: [0|0] [1|2] [2|4] [3|6]

Append new elements to data2->data4:
Len: 6; Cap: 10; Address: 0xc00000a160; Data: [0|0] [1|1] [2|2] [3|3] [4|4] [5|5]

Copy elements to data4:
Len: 6; Cap: 10; Address: 0xc00000a180; Data: [0|100] [1|200] [2|-1] [3|300] [4|4] [5|5]

Copy elements to data4 in custom position:
Len: 6; Cap: 10; Address: 0xc00000a1a0; Data: [0|100] [1|0] [2|100] [3|-1] [4|200] [5|-2]

*/