package currency

import "testing"

func TestPrittyfy(t *testing.T) {
	testValue := -12345.6789
	expectedValue := "-12,345.6789"

	resultValue := prettify(testValue)

	if expectedValue != resultValue {
		t.Fatalf("Expected %s, but %s ", expectedValue, resultValue)
	}

	testValueSecond := 123456789.98765
	expectedValueSecond := "123,456,789.98765"

	resultValueSecond := prettify(testValueSecond)
	if expectedValueSecond != resultValueSecond {
		t.Fatalf("Expected %s, but %s", expectedValueSecond, resultValueSecond)
	}
}

func TestFormat(t *testing.T) {

	testValue := -123456789.87654
	expectedValue := "$-123,456,789.87654"

	resultValue := Format(USD, float64(testValue))
	if expectedValue != resultValue {
		t.Fatalf("Expected %s, but %s", expectedValue, resultValue)
	}
}
