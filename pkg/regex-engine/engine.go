package regexengine

type engine struct {
	Engine
	regex string
}

// Compile the regular expression given when creating the engine
// retuns false if the regex cannot be compiled.
func (e *engine) Compile() bool {
	panic("not implemented yet")
}

// Gets the regular expression as string.
func (e *engine) GetRegex() string {
	return e.regex
}

// Returns true if regex matches the string.
func (e *engine) Match(input string) bool {
	panic("not implemented yet")
}
