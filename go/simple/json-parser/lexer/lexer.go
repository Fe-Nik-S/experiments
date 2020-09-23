package lexer

import (
	"../token"
	"unicode"
)

type Lexer struct {
	start  int
	end    int
	symbol rune
	input  []rune
}

func NewLexer(input []byte) *Lexer {
	l := &Lexer{
		input: []rune(string(input)),
	}
	l.nextChar()
	return l
}

func (l *Lexer) nextChar() {
	if l.end >= len(l.input) {
		l.symbol = 0
	} else {
		l.symbol = l.input[l.end]
	}
	l.start = l.end
	l.end++
}

func (l *Lexer) isInteger() bool {
	if !unicode.IsDigit(l.symbol) {
		return false
	}

	for unicode.IsDigit(l.symbol) {
		l.end++
		l.symbol = l.input[l.end]
	}
	return true
}

func (l *Lexer) isString() bool {
	if l.symbol != '"' {
		return false
	}

	iLen := len(l.input)
	for l.end < iLen {
		l.end++
		l.symbol = l.input[l.end]

		if l.symbol == '"' {
			l.end++
			l.symbol = l.input[l.end]
			return true
		}

	}
	return false
}

func (l *Lexer) skipWhiteSpace() {
	for {
		switch l.symbol {
		case ' ', '\n', '\t', '\r':
			l.nextChar()
		default:
			return
		}
	}
}

func (l *Lexer) GetToken() (tok *token.Token) {
	l.skipWhiteSpace()
	defer l.nextChar()

	switch l.symbol {
	case ':':
		tok = token.NewToken(token.COLON, string(l.symbol))
	case ',':
		tok = token.NewToken(token.COMMA, string(l.symbol))
	case '{':
		tok = token.NewToken(token.LBRACE, string(l.symbol))
	case '}':
		tok = token.NewToken(token.RBRACE, string(l.symbol))
	case '[':
		tok = token.NewToken(token.LBRACKET, string(l.symbol))
	case ']':
		tok = token.NewToken(token.RBRACKET, string(l.symbol))
	default:
		if l.isString() {
			tok = token.NewToken(token.STRING, string(l.input[l.start:l.end]))
		} else if l.isInteger() {
			tok = token.NewToken(token.INTEGER, string(l.input[l.start:l.end]))
		} else if l.symbol == rune(0) {
			tok = token.NewToken(token.EOF, "")
		} else {
			tok = token.NewToken(token.INVALID, string(l.symbol))
		}
	}

	return
}

func (l *Lexer) PeakToken() (tok *token.Token) {
	start := l.start
	end := l.end
	tok = l.GetToken()

	l.start = start
	l.end = end
	l.symbol = l.input[l.end-1]
	return
}
