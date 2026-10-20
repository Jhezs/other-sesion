"""Estadísticas de tokens de other-sesion.

Uso: python3 ahorro.py informe|estado|marcar [etiqueta] [--carpeta RUTA]

Sin --carpeta, se busca desde el directorio actual hacia arriba: Claude Code guarda cada proyecto en
~/.claude/projects/<ruta del proyecto con todo lo que no es letra o número cambiado por "-">.
Lee las transcripciones .jsonl (campo usage de cada respuesta), sin duplicar mensajes.
Las marcas se guardan en memory/ahorro.json dentro de la carpeta del proyecto.
"""
import json, os, re, sys, time
from pathlib import Path

def carpeta_proyecto(cwd=None, raiz=None):
    raiz = Path(raiz) if raiz else Path.home() / ".claude" / "projects"
    existentes = {p.name.lower(): p for p in raiz.glob("*") if p.is_dir()}
    p = Path(cwd) if cwd else Path.cwd()
    for d in [p, *p.parents]:
        hallada = existentes.get(re.sub(r"[^A-Za-z0-9]", "-", str(d)).lower())
        if hallada:
            return hallada
    return None

def cargar(f):
    vistos, t = set(), dict(turnos=0, entrada=0, escritura=0, lectura=0, salida=0, primero=0, pico=0, ultimo=0)
    for linea in f.open(encoding="utf-8", errors="replace"):
        try:
            o = json.loads(linea)
        except ValueError:
            continue
        m = o.get("message") or {}
        u = m.get("usage")
        if not u or m.get("id") in vistos:
            continue
        vistos.add(m.get("id"))
        ctx = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
        t["turnos"] += 1
        t["entrada"] += u.get("input_tokens", 0)
        t["escritura"] += u.get("cache_creation_input_tokens", 0)
        t["lectura"] += u.get("cache_read_input_tokens", 0)
        t["salida"] += u.get("output_tokens", 0)
        t["primero"] = t["primero"] or ctx
        t["pico"] = max(t["pico"], ctx)
        t["ultimo"] = ctx
    return t

def k(n):
    return f"{n/1000:,.1f}k"

def suma(d):
    return d["entrada"] + d["escritura"] + d["lectura"] + d["salida"]

def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    args, explicita = list(argv), None
    if "--carpeta" in args:
        i = args.index("--carpeta")
        explicita = args[i + 1] if i + 1 < len(args) else None
        del args[i:i + 2]
    modo = args[0] if args else "informe"
    base = Path(explicita) if explicita else carpeta_proyecto()
    if base is None or not base.is_dir():
        print("No encuentro la carpeta del proyecto en ~/.claude/projects. Usa --carpeta RUTA.")
        return
    marcas_f = base / "memory" / "ahorro.json"
    marcas = json.loads(marcas_f.read_text(encoding="utf-8")) if marcas_f.exists() else []
    ses = sorted(base.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    if modo == "estado":
        if not ses:
            print("Sin sesiones todavía.")
            return
        # Hooks o llamadas sueltas crean sesiones de 1 turno que serían "la más reciente": se salta a la última real.
        for p in reversed(ses[-5:]):
            d = cargar(p)
            if d["turnos"] >= 3:
                break
        ctx = d["ultimo"]
        if ctx < 150_000:
            consejo = "Bien: la sesión sigue ligera."
        elif ctx < 300_000:
            consejo = "Conviene cerrar pronto con /other-sesion clear."
        else:
            consejo = "Cierra ya con /other-sesion clear: cada turno paga todo este contexto."
        print(f"Sesión actual: {d['turnos']} turnos · contexto ahora {k(ctx)} · pico {k(d['pico'])} · arrancó en {k(d['primero'])}")
        print(consejo)
        return
    datos = {p.stem: cargar(p) for p in ses}
    total = sum(suma(d) for d in datos.values())
    if modo == "marcar":
        actual = ses[-1].stem if ses else ""
        marcas.append(dict(hora=time.strftime("%Y-%m-%d %H:%M"), etiqueta=args[1] if len(args) > 1 else "sin etiqueta",
                           sesion=actual, total=total, contexto_pico=datos[actual]["pico"] if actual else 0))
        marcas_f.parent.mkdir(exist_ok=True)
        tmp = marcas_f.with_suffix(".tmp")
        tmp.write_text(json.dumps(marcas, indent=1, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, marcas_f)  # un archivo a medio escribir nunca queda como ahorro.json
        print(f"Marca guardada · acumulado {k(total)}")
        return
    print("Sesiones (más antigua primero). 1er contexto = tokens del primer turno; pico = el mayor contexto alcanzado.")
    print(f"{'sesión':10} {'turnos':>6} {'1er contexto':>13} {'pico':>9} {'cache leída':>12} {'cache nueva':>12} {'salida':>8}")
    for s, d in datos.items():
        print(f"{s[:8]:10} {d['turnos']:>6} {k(d['primero']):>13} {k(d['pico']):>9} {k(d['lectura']):>12} {k(d['escritura']):>12} {k(d['salida']):>8}")
    if marcas:
        print("\nMarcas (total = entrada + cache + salida):")
        ant = 0
        for m in marcas:
            print(f"{m['hora']}  {m['etiqueta']:<18} acumulado {k(m['total']):>10}  desde la anterior {k(m['total'] - ant):>10}")
            ant = m["total"]
        print(f"Desde la última marca hasta ahora: {k(total - ant)}")

if __name__ == "__main__":
    main(sys.argv[1:])
