package cmd

import (
    "context"
    "time"

    "github.com/ritiksuman07/portman/internal/tui"
    "github.com/spf13/cobra"
)

var refreshSeconds int

var runCmd = &cobra.Command{
    Use:   "run",
    Short: "Launch the portman TUI",
    RunE: func(cmd *cobra.Command, args []string) error {
        ctx := context.Background()
        return tui.Run(ctx, time.Duration(refreshSeconds)*time.Second)
    },
}

func init() {
    runCmd.Flags().IntVarP(&refreshSeconds, "refresh", "r", 2, "refresh interval in seconds")
    rootCmd.RunE = runCmd.RunE
}
