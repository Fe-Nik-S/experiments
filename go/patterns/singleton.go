package main

import (
	"fmt"
	"sync"
	"time"
)

type Singleton struct {
	CreatedAt time.Time
}

var (
	instance *Singleton
	once sync.Once
)

func GetInstance() *Singleton {
	once.Do(func() {
		instance = &Singleton{time.Now()}
	})
	return instance
}

func main() {

	singletonObject := GetInstance()
	fmt.Println(singletonObject, singletonObject.CreatedAt)

	singletonObject = GetInstance()
	fmt.Println(singletonObject, singletonObject.CreatedAt)
}

// OUTPUT
// &{{63680230300 370255466 0x585800}} 2018-08-12 12:33:40.370255466 +0500 +05
// &{{63680230300 370255466 0x585800}} 2018-08-12 12:33:40.370255466 +0500 +05
