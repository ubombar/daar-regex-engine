package regexengine

// The idea is to create the interface compile it and use the match function to test.
// In the background the implementation will create the following entities: first a
// prefix representation of the regex, then a syntax tree using prefix then an NDFA,
// and finally the DFA using the subset method. We might optimize the alphanumerical
// searches with Knuth-Morris-Pratt (KMP) algorithm.
type Engine interface {
	// Compile the regular expression given when creating the engine
	// retuns false if the regex cannot be compiled.
	Compile() bool

	// Gets the regular expression as string.
	GetRegex() string

	// Returns true if regex matches the string.
	Match(input string) bool
}

func New(regex string) Engine {
	return &engine{
		regex: regex,
	}
}
