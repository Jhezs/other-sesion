"""Estadísticas de tokens de other-sesion. Uso: python ahorro.py informe|marcar <etiqueta> <carpeta_del_proyecto>

Lee las transcripciones .jsonl del proyecto (campo usage de cada respuesta), sin duplicar mensajes.
Las marcas se guardan en memory/ahorro.json dentro de la carpeta del proyecto.
"""
import json, sys, time
from pathlib import Path

def cargar(f):
    vistos, t = set(), dict(turnos=0, entrada=0, escritura=0, lectura=0, salida=0, primero=0, pico=0)
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
    return t

def k(n):
    return f"{n/1000:,.1f}k"

def suma(d):
    return d["entrada"] + d["escritura"] + d["lectura"] + d["salida"]

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if len(args) < 2 or not Path(args[-1]).is_dir():
        print("Uso: python ahorro.py informe|marcar <etiqueta> <carpeta_del_proyecto>")
        return
    modo, base = args[0], Path(args[-1])
    marcas_f = base / "memory" / "ahorro.json"
    marcas = json.loads(marcas_f.read_text(encoding="utf-8")) if marcas_f.exists() else []
    ses = sorted(base.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    datos = {p.stem: cargar(p) for p in ses}
    total = sum(suma(d) for d in datos.values())
    if modo == "marcar":
        actual = ses[-1].stem if ses else ""
        marcas.append(dict(hora=time.strftime("%Y-%m-%d %H:%M"), etiqueta=args[1] if len(args) > 2 else "sin etiqueta",
                           sesion=actual, total=total, contexto_pico=datos[actual]["pico"] if actual else 0))
        marcas_f.write_text(json.dumps(marcas, indent=1, ensure_ascii=False), encoding="utf-8")
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

main()
