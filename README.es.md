<p align="center"><img src="logo.png" width="128" alt="other-sesion"></p>

# other-sesion

[English](README.md) · **Español**

**Skill de Claude Code** (`claude-code-skill`).

Skill de Claude Code para cerrar una sesión larga sin perder el hilo y gastando pocos tokens: guarda los puntos clave en la memoria del proyecto y deja listo el arranque de la sesión siguiente.

## Comandos

| Comando | Qué hace |
|---|---|
| `/other-sesion` | Guarda traspaso y mapa; explica cómo continuar |
| `/other-sesion clear` | Igual, y deja listo el `/clear` |
| `/other-sesion retomar` / `resume` | En sesión nueva: carga traspaso y mapa, resume y propone el primer pendiente |
| `/other-sesion mapa` / `map` | Crea o actualiza el mapa del proyecto |
| `/other-sesion compactar` / `compact` | Da el texto para pegar en `/compact` |
| `/other-sesion ahorro` / `savings` | Estadísticas de tokens por sesión y entre marcas |
| `/other-sesion estado` / `status` | Contexto actual de la sesión y si conviene cerrar |
| `/other-sesion deshacer` / `undo` | Restaura el traspaso anterior |
| `/other-sesion ayuda` / `help` | Lista los comandos |

Cada comando funciona en español o en inglés (`retomar` = `resume`, `mapa` = `map`, `compactar` = `compact`, `ahorro` = `savings`, `estado` = `status`, `deshacer` = `undo`, `ayuda` = `help`).

## Instalación

Un solo comando (sirve para cualquier usuario; usa tu carpeta personal, sin rutas fijas):

```bash
# macOS / Linux
sh -c "$(curl -fsSL https://raw.githubusercontent.com/Jhezs/other-sesion/v1.2/install.sh)"
```

```powershell
# Windows (PowerShell)
irm https://raw.githubusercontent.com/Jhezs/other-sesion/v1.2/install.ps1 | iex
```

Lee el script antes de ejecutarlo (es corto). O clona el repositorio a mano dentro de la carpeta de skills de Claude Code.

macOS / Linux:

```bash
git clone https://github.com/Jhezs/other-sesion.git ~/.claude/skills/other-sesion
```

Windows (PowerShell):

```powershell
git clone https://github.com/Jhezs/other-sesion.git "$env:USERPROFILE\.claude\skills\other-sesion"
```

Reinicia Claude Code y escribe `/other-sesion ayuda` para comprobar que se cargó.

Para actualizar: `git -C ~/.claude/skills/other-sesion pull`.

`ahorro.py` necesita Python 3 y no usa dependencias externas. Encuentra solo la carpeta del proyecto en `~/.claude/projects` a partir de tu directorio actual.

## Nota

El skill escribe en la memoria del proyecto (`~/.claude/projects/<proyecto>/memory/`). Revisa `SKILL.md` antes de usarlo y ajústalo a tu forma de trabajar. Si el proyecto tiene `graphify-out/` (herramienta opcional graphify), el modo `mapa` lo aprovecha.

Las instrucciones de `SKILL.md` y las respuestas del skill están en español.

## Licencia

MIT. Ver `LICENSE`.

## Contribuidores

- **Claude** (Anthropic): escribió el código y la documentación.
- **Jhezs**: dueño del proyecto; revisó y aprobó el código.
