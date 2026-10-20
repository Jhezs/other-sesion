<p align="center"><img src="logo.png" width="128" alt="other-sesion"></p>

# other-sesion

**English** · [Español](README.es.md)

**Claude Code skill** (`claude-code-skill`).

A Claude Code skill to close a long session without losing the thread, while spending few tokens: it saves the key points in the project's memory and sets up the start of the next session.

## Commands

| Command | What it does |
|---|---|
| `/other-sesion` | Saves the handoff and the project map; explains how to continue |
| `/other-sesion clear` | Same, and gets `/clear` ready |
| `/other-sesion retomar` / `resume` | In a new session: loads the handoff and map, summarizes and proposes the first pending task |
| `/other-sesion mapa` / `map` | Creates or updates the project map |
| `/other-sesion compactar` / `compact` | Gives you the text to paste into `/compact` |
| `/other-sesion ahorro` / `savings` | Token statistics per session and between marks |
| `/other-sesion ayuda` / `help` | Lists the commands |

Every command works in Spanish or English: `retomar` = `resume`, `mapa` = `map`, `compactar` = `compact`, `ahorro` = `savings`, `ayuda` = `help`.

## Installation

Clone the repository into Claude Code's skills folder.

macOS / Linux:

```bash
git clone https://github.com/Jhezs/other-sesion.git ~/.claude/skills/other-sesion
```

Windows (PowerShell):

```powershell
git clone https://github.com/Jhezs/other-sesion.git "$env:USERPROFILE\.claude\skills\other-sesion"
```

Restart Claude Code and type `/other-sesion ayuda` to check that it loaded.

To update: `git -C ~/.claude/skills/other-sesion pull`.

`ahorro.py` needs Python 3 and has no external dependencies.

## Note

The skill writes to the project's memory (`~/.claude/projects/<project>/memory/`). Review `SKILL.md` before using it and adapt it to your workflow. If the project has `graphify-out/` (optional graphify tool), the `mapa` mode uses it.

The instructions in `SKILL.md` and the skill's replies are in Spanish.

## License

MIT. See `LICENSE`.

## Contributors

- **Claude** (Anthropic): wrote the code and the documentation.
- **Jhezs**: project owner; reviewed and approved the code.
