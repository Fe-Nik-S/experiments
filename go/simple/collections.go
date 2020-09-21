package main

import (
    "fmt"
    "github.com/golang-collections/collections/stack"
    "github.com/golang-collections/collections/queue"
    "github.com/golang-collections/collections/set"
)


func main(){
    stackObj := stack.New()
    stackObj.Push(2)
    stackObj.Push(3)
    stackObj.Push(4)
    fmt.Printf("%#v\n", stackObj)
    for stackObj.Len() != 0 {
        val := stackObj.Pop()
        fmt.Println(val, "removed from stack")
    }

    queueObj := queue.New()
    queueObj.Enqueue(2)
    queueObj.Enqueue(3)
    queueObj.Enqueue(4)
    fmt.Printf("\n%#v\n", queueObj)
    for queueObj.Len() != 0 {
        val := queueObj.Dequeue()
        fmt.Println(val, "removed from queue")
    }

    setObj := set.New()
    setObj.Insert(2)
    setObj.Insert(3)
    setObj.Insert(4)
    fmt.Printf("\n%#v\n", setObj)
    searchValues := []int{9, 2, 5}
    for _, value := range searchValues {
        if setObj.Has(value) {
            setObj.Remove(value)
            fmt.Println(value, "removed from set")
        } else {
            fmt.Printf("%v not found in set\n", value)
        }
    }
}

/*
Output:

&stack.Stack{top:(*stack.node)(0xc82000e560), length:3}
4 removed from stack
3 removed from stack
2 removed from stack

&queue.Queue{start:(*queue.node)(0xc82000e5c0), end:(*queue.node)(0xc82000e600), length:3}
2 removed from queue
3 removed from queue
4 removed from queue

&set.Set{hash:map[interface {}]set.nothing{2:set.nothing{}, 3:set.nothing{}, 4:set.nothing{}}}
9 not found in set
2 removed from set
5 not found in set
*/
