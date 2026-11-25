"""Verifica el libro ordenado por ramas: python -I verificar_ramas.py <nuevo.json> <anterior.json>
Comprueba orden de la lista, que no queden referencias "cap. N" y que las misiones no cambiaron."""
import json, re, sys

sys.stdout.reconfigure(encoding="utf-8")

ESPERADO = [
    "[Inicio] Bienvenido a ArreMods",
    "[Historia] Los primeros días", "[Historia] Preparación del aventurero", "[Historia] Explorador",
    "[Historia] Tu primer asentamiento", "[Historia] Grandes expediciones", "[Historia] La última expedición",
    "[Equipo] Taller y mejoras", "[Equipo] Tinkers' Construct",
    "[Recursos] Rustic", "[Recursos] Vida en la aldea", "[Recursos] Mystical Agriculture",
    "[Tecnología] Ender IO", "[Tecnología] Applied Energistics 2", "[Tecnología] Draconic Evolution",
    "[Tecnología] El poder definitivo",
    "[Magia] Maldición lunar", "[Magia] Astral Sorcery", "[Magia] Harshen Universe",
    "[Combate] Guardianes y defensas", "[Combate] Criaturas de la noche", "[Combate] Enemigos infernales",
    "[Combate] Depredadores", "[Combate] Desafíos legendarios",
    "[Exploración] Tropicraft", "[Exploración] Cavern", "[Exploración] Hunting Dimension",
    "[Exploración] The Betweenlands", "[Exploración] Elemental Dimensions", "[Exploración] Maestro de las dimensiones",
    "[Logros] Coleccionista",
]


def sin_color(t):
    return re.sub("§.", "", t)


def lineas(d):
    ls = sorted(d["questLines:9"].values(), key=lambda l: l["order:3"])
    return [(sin_color(l["properties:10"]["betterquesting:10"]["name:8"]),
             l["properties:10"]["betterquesting:10"]["desc:8"],
             sorted(e["id:3"] for e in l["quests:9"].values())) for l in ls]


def misiones(d):
    return {q["questID:3"]: q for q in d["questDatabase:9"].values()}


def main(nuevo, anterior):
    n, a = (json.load(open(p, encoding="utf-8")) for p in (nuevo, anterior))
    fallas = []
    if len(n["questLines:9"]) != 31 or len(n["questDatabase:9"]) != 150:
        fallas.append("cantidad: %d capítulos, %d misiones" % (len(n["questLines:9"]), len(n["questDatabase:9"])))
    nombres = [x[0] for x in lineas(n)]
    if nombres != ESPERADO:
        fallas.append("orden_de_ramas: " + "; ".join(nombres))
    # misiones_intactas
    mn, ma = misiones(n), misiones(a)
    if set(mn) != set(ma):
        fallas.append("misiones_intactas: IDs distintos")
    for qid in ma:
        for k in ("preRequisites:11", "tasks:9", "rewards:9"):
            if qid in mn and mn[qid][k] != ma[qid][k]:
                fallas.append("misiones_intactas: %s cambió en %d" % (k, qid))
    # mismas misiones en cada capítulo (comparando conjuntos, el orden cambia)
    if sorted(x[2] for x in lineas(n)) != sorted(x[2] for x in lineas(a)):
        fallas.append("capitulos_intactos: cambió qué misiones tiene algún capítulo")
    # sin_cap_numerico
    textos = [q["properties:10"]["betterquesting:10"][k] for q in mn.values() for k in ("name:8", "desc:8")]
    textos += [x[0] for x in lineas(n)] + [x[1] for x in lineas(n)]
    restos = sorted({m for t in textos for m in re.findall(r"[Cc]ap\. \d+[^\n]{0,15}", t)})
    if restos:
        fallas.append("sin_cap_numerico: " + " | ".join(restos))
    if fallas:
        print("FALLA\n - " + "\n - ".join(fallas))
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
