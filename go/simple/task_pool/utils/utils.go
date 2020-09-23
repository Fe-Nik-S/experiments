package utils

import "math/rand"

var letterRunes = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

func GenerateRandomStr(size int) string {
    runesCount := len(letterRunes)
    result := make([]rune, size)
    for i := range result {
        result[i] = letterRunes[rand.Intn(runesCount)]
    }
    return string(result)
}
