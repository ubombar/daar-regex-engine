package egrep

import (
	"fmt"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "",
	Short: "This is a proof of concept work for egrep",
	Long:  "This program tries to imitate the GOAT egrep. It will compile a dfa from the given regex and run on the input.",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("TODO: Buold the regexp here.")
	},
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		panic(err)
	}
}
