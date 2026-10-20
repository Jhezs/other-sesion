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
| `/other-sesion retomar` | En sesión nueva: carga traspaso y mapa, resume y propone el primer pendiente |
| `/other-sesion mapa` | Crea o actualiza el mapa del proyecto |
| `/other-sesion compactar` | Da el texto para pegar en `/compact` |
| `/other-sesion ahorro` | Estadísticas de tokens por sesión y entre marcas |
| `/other-sesion ayuda` | Lista los comandos |

## Instalación

Clona el repositorio dentro de la carpeta de skills de Claude Code.

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

`ahorro.py` necesita Python 3 y no usa dependencias externas.

## Nota

El skill escribe en la memoria del proyecto (`~/.claude/projects/<proyecto>/memory/`). Revisa `SKILL.md` antes de usarlo y ajústalo a tu forma de trabajar. Si el proyecto tiene `graphify-out/` (herramienta opcional graphify), el modo `mapa` lo aprovecha.

Las instrucciones de `SKILL.md` y las respuestas del skill están en español.

## Licencia

MIT. Ver `LICENSE`.

## Contribuidores

- **Claude** (Anthropic): escribió el código y la documentación.
- **Jhezs**: dueño del proyecto; revisó y aprobó el código.
