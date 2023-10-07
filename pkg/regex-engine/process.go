package regexengine

import "fmt"

var SPECIAL_CHARACTERS = map[string]bool{
	"(": true,
	")": true,
	"*": true,
	".": true,
	"|": true,
	"+": true,
}

func Tokenize(regex string) []string {
	concat_list := make([]string, 0)
	continue_concatination := false

	for i := 0; i < len(regex); i++ {
		char := fmt.Sprintf("%c", regex[i])
		if _, ok := SPECIAL_CHARACTERS[char]; ok {
			concat_list = append(concat_list, char)
			continue_concatination = false
		} else {
			if continue_concatination {
				concat_list[len(concat_list)-1] = fmt.Sprint(concat_list[len(concat_list)-1], char)
			} else {
				concat_list = append(concat_list, char)
				continue_concatination = true
			}
		}
	}

	return concat_list
}
