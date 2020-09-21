package main

import (
        "fmt"
        "reflect"
)

func printValueByType(v reflect.Value) {
        switch v.Kind() {
        case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
                fmt.Printf("int %v \n", v.Int())

        case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64, reflect.Uintptr:
                fmt.Printf("uint %v \n", v.Uint())

        case reflect.Float32, reflect.Float64:
                fmt.Printf("float %v \n", v.Float())

        case reflect.String:
                fmt.Printf("string %v \n", v.String())

        case reflect.Bool:
                fmt.Printf("bool %v \n", v.Bool())

        case reflect.Map:
                fmt.Print("map{\n")
                for i, key := range v.MapKeys() {
                        if i > 0 {
                                fmt.Print(", \n")
                        }
                        printValue(key)
                        fmt.Print(" : ")
                        printValue(v.MapIndex(key))
                }
                fmt.Print("}\n")

        case reflect.Interface, reflect.Ptr:
                fmt.Print("pointer ")
                printValue(v.Elem())

        default:
                fmt.Print("Not implemented type:", v.Kind(), v.Interface())
        }
}

func printValue(arg interface{}) {
        printValueByType(reflect.ValueOf(arg))
}

func main() {
      
        var i int = -105
        printValue(i)

        var u uint = 1048
        printValue(u)

        var f float32 = 1256.943
        printValue(f)

        printValue("Some text")

        printValue(false)
        
        printValue(map[int]string{
                0: "text_1",
                15: "text_2",
        })

        printValue(&i)
}

/*
Output:


*/