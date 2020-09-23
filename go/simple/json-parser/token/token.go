package token

import "fmt"

const (
	EOF = iota
	COMMA
	COLON
	LBRACE
	RBRACE
	LBRACKET
	RBRACKET
	STRING
	INTEGER
	BOOLEAN
	NULL
	INVALID
)

type (
	TokenType int
	Literal   []rune
)

type Token struct {
	TokenType
	Literal
}

func NewToken(tType TokenType, literal string) *Token {
	return &Token{
		TokenType: tType,
		Literal:   []rune(literal),
	}
}

func (t *Token) String() string {
	return fmt.Sprintf("{Token.%s: %s}", string(t.TokenType), string(t.Literal))
}
