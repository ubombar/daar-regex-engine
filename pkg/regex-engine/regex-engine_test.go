package regexengine_test

import (
	"fmt"
	"testing"

	regexengine "github.com/ubombar/daar-regex-engine/pkg/regex-engine"
)

func TestRegexes(t *testing.T) {
	tests := []struct {
		regex   string
		input   string
		compile bool
		matched bool
	}{
		{regex: "a", input: "a", compile: true, matched: true},
		{regex: "a", input: "b", compile: true, matched: false},
		{regex: "a|b", input: "b", compile: true, matched: true},
		{regex: "abab", input: "b", compile: true, matched: false},
		{regex: "a|bc+", input: "b", compile: true, matched: false},
		{regex: "a|bc+", input: "bccc", compile: true, matched: true},
	}

	for i, testCell := range tests {
		t.Run(fmt.Sprintf("regex-test-%d", i), func(tt *testing.T) {
			re := regexengine.New(testCell.regex)
			compiles := re.Compile()

			if compiles != testCell.compile {
				tt.Errorf("regex comilation result is different than expected. Compiled: %v", compiles)
			}

			// If it should have compiled we test for input match.
			if testCell.compile {
				if matched := re.Match(testCell.input); matched != testCell.matched {
					tt.Errorf("regex matched is different than expected. Matched: %v", matched)
				}
			}

		})
	}
}
