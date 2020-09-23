package main

import (
	"fmt"
	"log"

	"./utils"
	"./pool"
)

const (
	WORKER_COUNT = 5
	JOB_COUNT = 100
	DATA_SIZE = 7
)


func main() {

	log.Println("starting application...")

	for i:=0; i< JOB_COUNT; i++ {
		job := utils.GenerateRandomStr(DATA_SIZE)
		fmt.Println(i, job)
	}


	queue := pool.NewDispatcher(WORKER_COUNT)
	for i:=0; i< JOB_COUNT; i++ {
		t := pool.NewTask(i, utils.GenerateRandomStr(DATA_SIZE))
		queue.Put(t)
	}
	queue.Stop()
	queue.Wait()
}
