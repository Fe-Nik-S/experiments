package converter

import "fmt"


const (
	errorConverterUnexpectedType = "Convert: unexpected type: `%T`, expected `%T`"
)


func ErrorUnexpectedType(currentType, expectedType interface{}) error {
	return fmt.Errorf(errorConverterUnexpectedType, currentType, expectedType)
}


func ToString(value interface{}) (res string, err error) {
	switch t := value.(type) {
	case string:
		res = t
	case []byte:
		res = string(t)
	default:
		err = ErrorUnexpectedType(value, res)
	}
	return
}


func ToFloat64(value interface{}) (res float64, err error) {
	switch t := value.(type) {
	case int:
		res = float64(t)
	case int8:
		res = float64(t)
	case int16:
		res = float64(t)
	case int32:
		res = float64(t)
	case int64:
		res = float64(t)
	case uint:
		res = float64(t)
	case uint8:
		res = float64(t)
	case uint16:
		res = float64(t)
	case uint32:
		res = float64(t)
	case uint64:
		res = float64(t)
	case float32:
		res = float64(t)
	case float64:
		res = t
	default:
		err = ErrorUnexpectedType(value, res)
	}
	return
}


func ToBool(value interface{}) (res bool, err error) {
	switch t := value.(type) {
	case bool:
		return t, nil
	default:
		err = ErrorUnexpectedType(value, res)
	}
	return
}


func ToBytes(value interface{}) (res []byte, err error) {
	switch t := value.(type) {
	case []byte:
		res = t
	case string:
		res = []byte(t)
	default:
		err = ErrorUnexpectedType(value, res)
	}
	return
}
