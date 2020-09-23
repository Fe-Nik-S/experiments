package main

import (
	"testing"

	"./utils"
	"./pool"
)

var (
	TEST_JOB_COUNT = 100
	TEST_DATA_SIZE = 5
)

func DoConcurrent1(workersCount int) {
	queue := pool.NewDispatcher(workersCount)
	for i:=0; i< TEST_JOB_COUNT; i++ {
		t := pool.NewTask(i, utils.GenerateRandomStr(TEST_DATA_SIZE))
		queue.Put(t)
	}
	queue.Stop()
	queue.Wait()
}

func DoConcurrent2(workersCount int) {
	queue := pool.NewDispatcher(workersCount)

	go func() {
		defer func() {
			queue.Stop()
			queue.Wait()
		}()

		for i:=0; i< TEST_JOB_COUNT; i++ {
			t := pool.NewTask(i, utils.GenerateRandomStr(TEST_DATA_SIZE))
			queue.Put(t)
		}
	}()
}

func BenchmarkNonConcurrent(b *testing.B) {
	for n := 0; n < b.N; n++ {
		for i:= 0; i < TEST_JOB_COUNT; i++ {
			utils.GenerateRandomStr(TEST_DATA_SIZE)
		}
	}
}

func Benchmark1Concurrent1(b *testing.B) {
	for n := 0; n < b.N; n++ {
		DoConcurrent1(1)
	}
}

func Benchmark10Concurrent1(b *testing.B) {
	for n := 0; n < b.N; n++ {
		DoConcurrent1(10)
	}
}

func Benchmark25Concurrent1(b *testing.B) {
	for n := 0; n < b.N; n++ {
		DoConcurrent1(25)
	}
}

func Benchmark1Concurrent2(b *testing.B) {
	for n := 0; n < b.N; n++ {
		DoConcurrent2(1)
	}
}

func Benchmark10Concurrent2(b *testing.B) {
	for n := 0; n < b.N; n++ {
		DoConcurrent2(10)
	}
}

func Benchmark25Concurrent2(b *testing.B) {
	for n := 0; n < b.N; n++ {
		DoConcurrent2(25)
	}
}
