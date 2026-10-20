---
name: other-sesion
description: >
  Cierra una sesión larga sin perder el hilo y gastando pocos tokens: guarda los puntos clave en la memoria del
  proyecto y deja listo el arranque de la sesión siguiente. Usar con /other-sesion (guardar y preparar el cierre),
  /other-sesion retomar (cargar el traspaso y el mapa en la sesión nueva), /other-sesion mapa (crear o actualizar la
  "biblioteca" que dice dónde está todo en el proyecto) o /other-sesion compactar (dar las instrucciones para /compact), /other-sesion clear (guardar y dar el paso para limpiar) o /other-sesion ahorro (estadísticas de tokens) o /other-sesion ayuda (listar los comandos). Los modos también se aceptan en inglés: resume, map, compact, savings, help. También cuando el usuario diga "guarda los puntos clave", "pasemos a otra sesión" o "se está gastando mucho".
---

# other-sesion

Objetivo: que una sesión nueva retome el trabajo leyendo muy poco (menos de 2.500 tokens entre traspaso y mapa), porque todo lo que se carga
al inicio se vuelve a pagar en cada turno. Esta skill no necesita subagentes. No releas archivos del proyecto para esto: trabaja con lo que ya está en la conversación.

## Alias en inglés

Cada modo acepta su nombre en español o en inglés, con el mismo efecto: `retomar` = `resume`, `mapa` = `map`, `compactar` = `compact`, `ahorro` = `savings`, `ayuda` = `help`. `clear` es igual en ambos. Si el argumento es uno de los nombres en inglés, aplica el modo español equivalente. Responde en el idioma en que escribió el usuario.

## Modo por defecto: `/other-sesion` (guardar y preparar el cierre)

1. **Reúne los puntos clave** de la sesión, sin copiar código ni transcribir conversación:
   - Decisiones tomadas y el porqué (una línea cada una).
   - Estado: qué quedó hecho y comprobado, y qué quedó hecho pero SIN comprobar.
   - Pendientes, en orden de prioridad, con el siguiente paso concreto.
   - Rutas, comandos o archivos que la sesión nueva necesitará (rutas completas), y puertos o servidores que quedaron corriendo.
   - Normas o preferencias nuevas que dio el usuario.
   - Riesgos o trampas que costó descubrir.
   Omite lo que ya está en git, en `CLAUDE.md` o en el código. Convierte fechas relativas a absolutas. Nunca guardes claves,
   tokens ni datos personales.
2. **Escribe UN archivo de traspaso** en el directorio de memoria del proyecto (la ruta está en tu prompt de sistema, en
   «Memory»), con el nombre `project_traspaso.md`. Si ya existe, **sobrescríbelo** (no acumules traspasos viejos).
   Formato:
   ```
   ---
   name: project-traspaso
   description: Estado y pendientes de la última sesión; leer al empezar con /other-sesion retomar
   metadata:
     type: project
   ---
   Fecha: <AAAA-MM-DD>. Tema de la sesión: <una línea>.
   ## Hecho
   - ...
   ## Pendiente (en orden)
   1. <paso concreto>
   ## Dónde está todo
   - <ruta> : <qué es>
   ## Decisiones y normas
   - ... **Why:** ... **How to apply:** ...
   ## Cuidado
   - ...
   ```
   Máximo ~40 líneas. Si algo es una preferencia duradera del usuario, guárdala además como memoria `feedback` propia, y si
   es un dato estable del proyecto, como memoria `project` propia, actualizando una existente en vez de duplicar.
3. **Actualiza el mapa** (modo `mapa`) con las referencias de lo que tocaste o descubriste en la sesión: solo líneas nuevas
   o corregidas, no lo reescribas.
4. **Actualiza `MEMORY.md`** con UNA línea de índice para `project_traspaso.md` y otra para `project_mapa.md` (si no están
   ya), sin pegar contenido.
5. **Responde al usuario** con:
   - Qué guardaste (3 a 6 viñetas) y la ruta del archivo.
   - Cuántos tokens pesa el traspaso (estimación: caracteres / 3,5).
   - Los pasos exactos para continuar: (a) cerrar la sesión o escribir `/clear`; (b) en la sesión nueva escribir
     `/other-sesion retomar`.
   - Qué NO se guardó por decisión (para que el usuario lo corrija).

## `/other-sesion retomar` (en la sesión nueva)

1. Lee SOLO `project_traspaso.md` y `project_mapa.md` (si existe) del directorio de memoria; no leas el resto de la memoria
   ni archivos del proyecto. Con el mapa sabes dónde está todo: úsalo ANTES de buscar o releer código, y para ubicar una
   función usa `graphify explain`/`query` si hay `graphify-out/`, y luego lee solo una ventana de líneas.
2. Resume al usuario en máximo 6 líneas: dónde se quedó, qué sigue y qué hay que confirmar.
3. Pregunta cuál pendiente seguir (o propón el primero) y empieza. Verifica con una lectura puntual cualquier cosa marcada
   «sin comprobar» antes de darla por buena. Si algo del traspaso contradice el código actual, manda el código.

## `/other-sesion compactar`

No guarda nada. Da al usuario el texto listo para pegar (la compactación solo la puede ejecutar él):
`/compact Conserva: decisiones y su porqué, estado de lo hecho y lo no comprobado, pendientes en orden, rutas completas de archivos, normas del usuario. Descarta: salidas largas de herramientas, informes de agentes, explicaciones ya resueltas.`
Recuerda que compactar pronto sale más barato que tarde, y que ejecutar primero el modo por defecto protege lo importante.

## `/other-sesion mapa` (la «biblioteca» del proyecto)

Un archivo corto que dice DÓNDE está cada cosa, para no releer código. Va en la memoria del proyecto como
`project_mapa.md` (nunca dentro del repositorio ni en git). Se crea la primera vez y después SOLO se actualiza con lo nuevo.

1. **Primera vez, si existe `graphify-out/`:** siembra el mapa con lo que el grafo ya sabe, sin gastar IA: lee solo las
   secciones «God Nodes» y «Community Hubs» de `graphify-out/GRAPH_REPORT.md` (no el informe entero). Si no existe,
   arma el mapa con lo que ya conoces de la sesión (no explores el proyecto entero para esto).
2. **Contenido** (máximo ~50 líneas, ~1.000 tokens):
   ```
   ---
   name: project-mapa
   description: Mapa del proyecto: dónde está cada cosa. Leer antes de buscar o releer código
   metadata:
     type: reference
   ---
   Proyecto: <nombre> · Ruta: <ruta> · Stack: <...> · Comandos: <arrancar, probar, compilar>
   ## Carpetas
   - <carpeta/> : <qué responsabilidad tiene>
   ## Puntos de entrada y piezas clave
   - <Nombre> (<archivo>) : <una línea de qué hace y de quién depende>
   ## Datos y reglas importantes
   - <regla/estructura> : <archivo donde vive>
   ## Pruebas, docs y grafo
   - <dónde están; si hay graphify-out/ y cuándo se actualizó por última vez>
   ```
   Referencia por **nombre de archivo y de función**, no por número de línea (las líneas se desfasan; para la línea exacta
   usa `graphify explain "<nodo>"`).
3. **Se va completando:** al cerrar una sesión (modo por defecto) añade o corrige solo las líneas de lo que tocaste o
   descubriste; borra lo que ya no exista. No lo reescribas entero.
4. **Entre proyectos:** mantén también `~/.claude/proyectos-mapa.md` (un solo archivo, una línea por proyecto: nombre, ruta,
   stack, para qué sirve y la ruta de su `project_mapa.md`). Se lee solo cuando el usuario habla de otro proyecto o pide
   contexto cruzado; no lo cargues al iniciar. Créalo si no existe.
5. **Cuidado con el tamaño:** si el mapa pasa de ~60 líneas, resume o divide por módulo (`project_mapa_<modulo>.md`) y deja en
   el principal solo el índice. Un mapa grande se paga en cada turno y deja de ahorrar.
6. **Verifica antes de fiarte:** el mapa es una pista. Si algo no coincide con el código, manda el código y corrige la línea.

## `/other-sesion clear`

Hace el modo por defecto completo (traspaso, mapa, `MEMORY.md`) y termina con una sola instrucción corta: «Listo. Escribe `/clear` y luego `/other-sesion retomar`». Un skill no puede ejecutar `/clear` por el usuario.

## `/other-sesion ahorro`

Mide tokens reales con `ahorro.py` (en esta carpeta; lee el campo `usage` de las transcripciones, no estima). Carpeta del proyecto = `~/.claude/projects/<proyecto>` (la de tu directorio de memoria, un nivel arriba de `memory`).
- Los modos por defecto, `clear` y `retomar` ejecutan al terminar `python <skill>/ahorro.py marcar "<modo>" "<carpeta>"` (una línea, salida ignorada). Así cada cierre y cada retomada quedan como marca.
- `/other-sesion ahorro` ejecuta `python <skill>/ahorro.py informe "<carpeta>"` y muestra la salida tal cual, más 2 líneas de lectura: gasto desde la última marca y si el «1er contexto» de la sesión nueva es menor que el «pico» de la anterior (eso es lo que ahorró el traspaso).
- Tokens ≠ dinero: la cache leída es mucho más barata que la nueva; no sumes todo como si costara igual.

## `/other-sesion ayuda`

Muestra esta tabla y nada más:
| Comando (español / English) | Qué hace |
|---|---|
| `/other-sesion` | Guarda traspaso y mapa; explica cómo continuar |
| `/other-sesion clear` | Igual, y deja listo el `/clear` |
| `/other-sesion retomar` / `resume` | En sesión nueva: carga traspaso y mapa, resume y propone el primer pendiente |
| `/other-sesion mapa` / `map` | Crea o actualiza el mapa del proyecto |
| `/other-sesion compactar` / `compact` | Da el texto para pegar en `/compact` |
| `/other-sesion ahorro` / `savings` | Estadísticas de tokens por sesión y entre marcas |
| `/other-sesion ayuda` / `help` | Esta lista |

Tolera errores de escritura en el argumento (p. ej. «osther», «retomr»): interprétalo por su parecido con un modo.

## Reglas
- Un solo archivo de traspaso, sobrescrito cada vez. Nada de historiales.
- Menos es más: si un dato no cambia lo que haría la sesión nueva, no entra.
- No uses esta skill como excusa para releer el proyecto; el traspaso sale de lo que ya sabes.
