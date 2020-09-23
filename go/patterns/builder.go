package main

import (
	"fmt"
)

type Builder interface {
	makeHeader(text string)
	makeContent(text string)
	makeFooter(text string)
}

type Item struct {
	Header  string
	Content string
	Footer  string
}

func (this *Item) ToString() string {
	var result string
	result = this.Header
	result += this.Content
	result += this.Footer
	return result
}

type ConcreteBuilder struct {
	item *Item
}

func (this *ConcreteBuilder) makeHeader(text string) {
	this.item.Header = "<header>" + text + "</header>\n"
}

func (this *ConcreteBuilder) makeContent(text string) {
	this.item.Content = "<article>" + text + "</article>\n"
}

func (this *ConcreteBuilder) makeFooter(text string) {
	this.item.Footer = "<footer>" + text + "</footer>\n"
}

type Director struct {
	builder Builder
}

func (this *Director) Construct() {
	this.builder.makeHeader("Header")
	this.builder.makeContent("Content")
	this.builder.makeFooter("Footer")
}

func main() {

	item := &Item{}

	director := Director{&ConcreteBuilder{item}}
	director.Construct()

	fmt.Println(item.ToString())

}

// OUTPUT
// <header>Header</header>
// <article>Content</article>
// <footer>Footer</footer>
