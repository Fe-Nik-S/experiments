package main

import (
	"fmt"
)


func BinarySearchRecursive(data []int, low int, high int, value int) int {
	mid := low + (high - low)/2;
	if data[mid] == value {
		return mid
	} else if data[mid] < value {
		return BinarySearchRecursive(data, mid+1, high, value)
	} else {
		return BinarySearchRecursive(data, low, mid-1, value)
	}
	return -1
}


func main(){
	numbers := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	searchValues := []int{9, 2, 5}

	fmt.Println(numbers)
	for _, value := range searchValues {
		findedIndex := BinarySearchRecursive(numbers, 1, 10, value)
		//outStr := fmt.Sprintf("Search value:: %v. Result index:: %v", value, findedIndex)
		fmt.Printf("Search value:: %v. Result index:: %v\n", value, findedIndex)
	}
}

/*
Output:

[1 2 3 4 5 6 7 8 9 10]
Search value:: 9. Result index:: 8
Search value:: 2. Result index:: 1
Search value:: 5. Result index:: 4

*/
