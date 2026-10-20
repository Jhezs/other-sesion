# Instala o actualiza other-sesion en %USERPROFILE%\.claude\skills\other-sesion (Windows).
# Install or update other-sesion in %USERPROFILE%\.claude\skills\other-sesion.
$ErrorActionPreference = "Stop"

$repo = "https://github.com/Jhezs/other-sesion.git"
$dest = Join-Path $env:USERPROFILE ".claude\skills\other-sesion"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Falta git / git is required"
}

if (Test-Path (Join-Path $dest ".git")) {
    if (git -C $dest status --porcelain) {
        Write-Error "Cambiaste archivos locales / you changed local files. Ejecuta: git -C '$dest' stash ; vuelve a ejecutar ; git -C '$dest' stash pop"
    }
    git -C $dest pull --ff-only
} else {
    New-Item -ItemType Directory -Force (Split-Path $dest) | Out-Null
    git clone $repo $dest
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Warning "/other-sesion ahorro necesita Python 3 / Python 3 is needed for the savings command"
}
Write-Host "Listo. Reinicia Claude Code y escribe /other-sesion ayuda"
