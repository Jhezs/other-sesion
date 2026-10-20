#!/usr/bin/env sh
# Instala o actualiza other-sesion en ~/.claude/skills/other-sesion (macOS / Linux).
# Install or update other-sesion in ~/.claude/skills/other-sesion.
set -e

REPO="https://github.com/Jhezs/other-sesion.git"
DEST="${HOME}/.claude/skills/other-sesion"

command -v git >/dev/null 2>&1 || { echo "Falta git / git is required" >&2; exit 1; }

if [ -d "$DEST/.git" ]; then
  git -C "$DEST" pull --ff-only
else
  mkdir -p "${HOME}/.claude/skills"
  git clone "$REPO" "$DEST"
fi

command -v python3 >/dev/null 2>&1 || echo "Aviso: /other-sesion ahorro necesita Python 3 / warning: Python 3 needed for the savings command"
echo "Listo. Reinicia Claude Code y escribe /other-sesion ayuda"
