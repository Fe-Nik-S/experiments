package main

import "fmt"

const (
	M_SIZE = 5

	TOP = iota
	LEFT
	DOWN
	RIGHT
)

func main() {

	printMatrix(fillMatrix(M_SIZE))
}

func fillMatrix(size int) (matrix [][]int) {
	matrix = make([][] int, size, size)
	for i := range matrix {
		matrix[i] = make([]int, size, size)
	}

	var i, j = size / 2, size / 2
	var iMin, iMax = i, i
	var jMin, jMax = j, j

	var d = TOP
	for step := 1; step < size*size+1; step++ {
		matrix[i][j] = step

		switch d {
		case TOP:
			i = i - 1
			if i < iMin {
				d = LEFT
				iMin = i
			}
		case LEFT:
			j = j - 1
			if j < jMin {
				d = DOWN
				jMin = j
			}
		case DOWN:
			i = i + 1
			if i > iMax {
				d = RIGHT
				iMax = i
			}
		case RIGHT:
			j = j + 1
			if j > jMax {
				d = TOP
				jMax = j
			}
		}
	}
	return
}

func printMatrix(matrix [][]int) {
	mLen := len(matrix)
	fmt.Printf("Matrix: %dx%d\n", mLen, len(matrix))
	fmt.Print("===========\n")
	for i := range matrix {
		for j := range matrix[i] {
			fmt.Printf("%d\t", matrix[i][j])
		}
		fmt.Print("\n")
	}
}

// OUTPUT
// Matrix: 5x5
// ===========
// 13	12	11	10	25
// 14	3	2	9	24
// 15	4	1	8	23
// 16	5	6	7	22
// 17	18	19	20	21
