package parser

import (
	"../ast"
	"../lexer"
	"../token"
	"fmt"
)

type Parser struct {
	Lexer *lexer.Lexer
}

func NewParser(l *lexer.Lexer) *Parser {
	return &Parser{Lexer: l}
}

func (p *Parser) Parse() ast.Json {
	tok := p.Lexer.GetToken()
	switch tok.TokenType {
	case token.STRING:
		return &ast.String{string(tok.Literal)}
	case token.INTEGER:
		return &ast.Integer{string(tok.Literal)}
	case token.LBRACE:
		return parseObject(p)
	case token.LBRACKET:
		return parseArray(p)
	case token.EOF:
		return nil
	}
	return nil
}

func parseArray(p *Parser) ast.Json {
	array := []ast.Json{}
	tok := p.Lexer.PeakToken()

	if tok.TokenType == token.RBRACKET {
		return &ast.Array{array}
	} else {
		array = append(array, p.Parse())
		tok = p.Lexer.GetToken()
		if tok.TokenType == token.RBRACKET {
			return &ast.Array{array}
		}
	}

	for {
		array = append(array, p.Parse())
		tok = p.Lexer.GetToken()
		if tok.TokenType == token.RBRACKET {
			break
		}

		if tok.TokenType != token.COMMA {
			panic(fmt.Sprintf("was expecting ',' got %s in array parse", string(tok.Literal)))
		}
	}

	return &ast.Array{array}
}

func parseObject(p *Parser) ast.Json {
	object := map[string]ast.Json{}
	tok := p.Lexer.GetToken()

	if tok.TokenType == token.RBRACE {
		return &ast.Object{object}
	} else {
		key := string(tok.Literal)
		p.Lexer.GetToken()
		object[key] = p.Parse()
		tok = p.Lexer.GetToken()
		if tok.TokenType == token.RBRACE {
			return &ast.Object{object}
		}
	}

	for {
		key := string(p.Lexer.GetToken().Literal)
		tok = p.Lexer.GetToken()
		if tok.TokenType != token.COLON {
			panic(fmt.Sprintf("was expecting ':' got %s", string(tok.Literal)))
		}
		object[key] = p.Parse()
		tok = p.Lexer.GetToken()

		if tok.TokenType == token.RBRACE {
			break
		}

		if tok.TokenType != token.COMMA {
			panic(fmt.Sprintf("was expecting ',' got %s", string(tok.Literal)))
		}
	}
	return &ast.Object{object}
}
