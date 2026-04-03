# portman

![Demo](assets/demo.gif)

Local port and process manager for developers. A fast, keyboard-driven TUI that shows what is running, where it is listening, and lets you act on it.

## Install

```bash
brew install ritiksuman007/tap/portman
```

```bash
go install github.com/ritiksuman007/portman@latest
```

## Run

```bash
portman
```

```bash
portman run --refresh 2
```

## Keybindings

- `j` / `k` or arrow keys: move
- `g` / `G`: jump to top/bottom
- `/`: filter by name or port
- `x`: kill process (confirm)
- `r`: restart process (confirm)
- `d`: toggle detail panel
- `tab`: switch Processes/Profiles
- `n`: new profile (Profiles tab)
- `enter`: launch profile (Profiles tab)
- `?`: help
- `q`: quit

## Profiles

Profiles live at `~/.config/portman/profiles.json`.

Example:

```json
[
  {
    "name": "backend-stack",
    "description": "Full local dev stack",
    "commands": [
      {
        "label": "API Server",
        "cmd": "go run ./cmd/api",
        "port": 8080,
        "dir": "~/projects/myapp"
      },
      {
        "label": "PostgreSQL",
        "cmd": "docker start my-postgres",
        "port": 5432
      }
    ]
  }
]
```

## Architecture

- Scanner (gopsutil) collects process + port data on a timer.
- Bubbletea drives the UI event loop.
- Profiles are stored locally as JSON.

## License

MIT
