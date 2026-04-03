# Profiles

Profiles are stored at:

```
~/.config/portman/profiles.json
```

## Example

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
