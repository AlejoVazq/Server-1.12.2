# -*- coding: utf-8 -*-
"""
Generador del libro de misiones de ArreMods — v2 (capítulos 1 a 27).
Formato: Better Questing 3.5.329 + Standard Expansion 3.4.173 (base de datos formato "2.0.0").
Uso:  python -I generar_misiones.py <archivo_salida.json>

Fuentes: pv7-docs/01..05 y datos leídos de los JAR, configs y world/level.dat (2026-11-19).
Los datos del libro se verificaron en los JAR y configs del servidor (ver pv7-docs/07_libro_de_misiones_v3.md).
La v1 (solo capítulos 1-5, sin compactar) está en generar_misiones_v1.py.
"""
import json, sys

WILD = 32767  # comodín de variante

def item(iid, count=1, dmg=0, ore="", tag=None):
    d = {"id:8": iid, "Count:3": count, "Damage:2": dmg, "OreDict:8": ore}
    if tag is not None:
        d["tag:10"] = tag
    return d

def lst(elems):
    return {"%d:10" % i: e for i, e in enumerate(elems)}

# ---- tareas -----------------------------------------------------------------
def t_check():
    return {"taskID:8": "bq_standard:checkbox"}

def t_get(items, consume=False):
    return {"taskID:8": "bq_standard:retrieval", "partialMatch:1": 1, "ignoreNBT:1": 1,
            "consume:1": 1 if consume else 0, "groupDetect:1": 0, "autoConsume:1": 0,
            "requiredItems:9": lst(items)}

def t_craft(items):
    return {"taskID:8": "bq_standard:crafting", "partialMatch:1": 1, "ignoreNBT:1": 1,
            "allowCraft:1": 1, "allowSmelt:1": 1, "allowAnvil:1": 0, "requiredItems:9": lst(items)}

def t_adv(adv_id):
    """Se completa sola cuando el jugador obtiene ese logro del mod."""
    return {"taskID:8": "bq_standard:advancement", "advancement_id:8": adv_id}

def t_dim(dim, name):
    """Se completa al estar en esa dimensión (distancia -1 = cualquier lugar de la dimensión)."""
    return {"taskID:8": "bq_standard:location", "name:8": name, "posX:3": 0, "posY:3": 0, "posZ:3": 0,
            "dimension:3": dim, "biome:8": "", "structure:8": "", "range:3": -1, "visible:1": 0,
            "hideInfo:1": 0, "invert:1": 0, "invertDistance:1": 0, "taxiCabDist:1": 0}

def t_hunt(entity, count=1):
    return {"taskID:8": "bq_standard:hunt", "target:8": entity, "required:3": count, "subtypes:1": 0,
            "ignoreNBT:1": 1, "targetNBT:10": {}, "damageType:8": ""}

# ---- recompensas ------------------------------------------------------------
def r_xp(dificultad):
    """Marca la dificultad de la misión (1 a 50). quest() la convierte en el premio de su nivel."""
    return {"_dificultad": dificultad}

# Niveles de premio. La XP va en PUNTOS, no en niveles: 1400 puntos ≈ pasar del nivel 0 al 30.
# Así una misión vale lo mismo para alguien con nivel 2 que para alguien con nivel 40.
#   (dificultad máxima, puntos de XP, objetos)
NIVELES_PREMIO = [
    (2,  30,   lambda: [item("minecraft:bread", 4)]),
    (4,  60,   lambda: [item("minecraft:iron_ingot", 2)]),
    (6,  120,  lambda: [item("minecraft:iron_ingot", 4), item("minecraft:bread", 4)]),
    (12, 250,  lambda: [item("minecraft:gold_ingot", 4), item("minecraft:ender_pearl", 2)]),
    (20, 500,  lambda: [item("minecraft:diamond", 2), item("minecraft:golden_apple", 1)]),
    (30, 900,  lambda: [item("minecraft:diamond", 4), item("minecraft:golden_apple", 2)]),
    (99, 1400, lambda: [item("minecraft:diamond", 6), item("minecraft:golden_apple", 1, 1)]),
]

def premio(dificultad):
    for tope, puntos, objetos in NIVELES_PREMIO:
        if dificultad <= tope:
            return [{"rewardID:8": "bq_standard:xp", "amount:3": puntos, "isLevels:1": 0}, r_items(objetos())]

def expandir_premios(rewards):
    out = []
    for r in rewards:
        out += premio(r["_dificultad"]) if "_dificultad" in r else [r]
    return out

def r_items(items):
    return {"rewardID:8": "bq_standard:item", "rewards:9": lst(items)}

def r_title(title, lore):
    return r_items([item("minecraft:paper", 1, 0, "", {"display:10": {
        "Name:8": "§6" + title, "Lore:9": {"%d:8" % i: l for i, l in enumerate(lore)}}})])

# ---- misiones ---------------------------------------------------------------
QUESTS = []
LINES = []
_line = [-1]

# ---- descripciones de los capítulos -------------------------------------------
# Se muestran al elegir un capítulo en la lista. Clave = número de capítulo.
DESCRIPCIONES = {
1: "§6Tu guía de ArreMods.§r Cada capítulo es un mod o un tema del servidor.\n\n"
   "§eCómo se usa:§r no hay un orden obligatorio. Las misiones grises se desbloquean al completar otras; "
   "las que tienen marco grande son las principales de cada capítulo.\n\n"
   "§eHerramientas que vas a usar todo el tiempo:§r\n"
   " · §6JEI§r (a la derecha del inventario): §eR§r sobre un objeto = cómo se fabrica, §eU§r = para qué sirve.\n"
   " · §6Hwyla§r: mirá un bloque y te dice qué es y de qué mod viene.\n"
   " · §6JourneyMap§r: §eJ§r abre el mapa, §eB§r crea un waypoint.\n\n"
   "Empezá leyendo las reglas en la primera misión.",
2: "§6Sobrevivir la primera noche.§r Madera, un refugio, un lugar donde dormir, fuego y comida.\n\n"
   "§eMods de este capítulo:§r\n"
   " · §6The Camping Mod§r: tiendas, sacos de dormir, fogatas para cocinar y mochilas.\n"
   " · §6Campfire§r: fogata que da luz y calor, pero se apaga sola a los ~6 minutos.\n"
   " · §6Corail Tombstone§r: si morís, tus cosas quedan en una tumba donde caíste.\n\n"
   "§cOjo con la noche:§r salen criaturas de otros mods (zombis con oficio, creepers elementales, monstruos mortales) "
   "y al dormir hay un 5 % de chance de pesadilla. Dormí con equipo puesto y la vida llena.",
3: "§6Equiparte antes de salir a explorar.§r\n\n"
   "§eMods de este capítulo:§r\n"
   " · §6Spartan Shields§r: escudos de madera, piedra, hierro, oro, obsidiana y diamante. Cada material aguanta más golpes.\n"
   " · §6Hammer Time§r: martillos que rompen 3×3 bloques de una vez. Ideales para minar y abrir túneles.\n"
   " · §6Disenchanter§r: mesa que saca los encantamientos de un objeto y los pasa a un libro.\n"
   " · §6Switch-Bow§r: arco con carcaj para cambiar de tipo de flecha sin abrir el inventario.\n\n"
   "Nada de este capítulo bloquea el resto: es para llegar mejor preparado.",
4: "§6Orientarte y moverte rápido.§r El mundo es grande y hay biomas y estructuras de muchos mods.\n\n"
   "§eMods de este capítulo:§r\n"
   " · §6Nature's Compass§r: elegís un bioma de la lista y la aguja te lleva hasta el más cercano.\n"
   " · §6JourneyMap§r: mapa, minimapa y waypoints. También marca dónde moriste.\n"
   " · §6Rope Bridge§r: dispara un puente de cuerda y madera para cruzar barrancos y ríos.\n"
   " · §6NetherPortalFix§r: cada portal del Nether vuelve al portal desde el que entraste.\n\n"
   "§7Los biomas de Tropicraft y Betweenlands no están en el mundo normal: tienen su propia dimensión.§r",
5: "§6Tu primera base.§r Reclamá el terreno, ordená tus cosas y empezá a cultivar.\n\n"
   "§eMods de este capítulo:§r\n"
   " · §6FTB Utilities§r: reclamo de chunks (nadie puede romper tu base) y §e/sethome§r / §e/home§r.\n"
   " · §6Backpacks§r, §6Iron Backpacks§r y las bolsas del §6Camping Mod§r: más espacio para llevar.\n"
   " · §6Storage Drawers§r: cajones que guardan muchísimo de un solo objeto; con el controlador se unen todos.\n"
   " · §6Chest Transporter§r: levanta un cofre lleno para mudarlo.\n"
   " · §6Water Strainer§r: filtra agua y junta palos, arcilla, arena y grava.\n\n"
   "Al terminar este capítulo, elegís tu rama: dimensiones, magia y tecnología, o combate.",
6: "§6The Betweenlands§r · dimensión 20\n\n"
   "Un pantano oscuro, enorme y con reglas propias. Es uno de los mods más grandes del servidor.\n\n"
   "§eCómo se entra:§r matá §eDruidas Oscuros§r en los altares druídicos de los pantanos del Overworld para juntar "
   "las 4 piezas del talismán. Con el talismán hacés crecer un árbol portal.\n\n"
   "§cReglas del pantano:§r las antorchas comunes no funcionan, las herramientas del Overworld rinden menos y se corroen, "
   "y la comida se pudre. Todo se fabrica de nuevo con materiales locales.\n\n"
   "§eJefes:§r Dreadful Peat Mummy, Spirit Tree y Primordial Malevolence (jefe final de la Wight Fortress).",
7: "§6Tropicraft§r · dimensión -127\n\n"
   "Islas tropicales con playas, volcanes, aldeas Koa, tiburones, tortugas y cócteles.\n\n"
   "§eDos formas de llegar:§r\n"
   " · Sentate en una §esilla de playa§r al atardecer después de tomar una §ePiña Colada§r.\n"
   " · Armá un portal con la §evarita§r: un anillo 5×5 de arenisca con un cuadrado 3×3 de agua adentro. "
   "Este portal sirve para ir y volver.\n\n"
   "Los cócteles se preparan en la §eDrink Mixer§r. Las §eazuritas§r y los §ezircones§r de las islas sirven para la varita.",
8: "§6Elemental Dimensions§r · dimensiones 100 a 104\n\n"
   "Cinco dimensiones en cadena: §eTierra → Agua → Aire → Espíritu → Fuego§r. Cada una tiene su jefe.\n\n"
   "§eCómo funciona:§r cada dimensión se abre con una §eruna§r. La de Tierra la sueltan los Guardias de las "
   "mazmorras-portal del Overworld. Las demás runas tienen 3 partes: las partes 1 y 3 las sueltan los monstruos "
   "y jefes de cada dimensión, y la parte 2 está en un cofre de la mazmorra de la dimensión anterior.\n\n"
   "§eEl viaje:§r poné la runa en el §ePortal Dialer§r de la mazmorra y parate frente a él.\n\n"
   "§eJefe final:§r el Fire Boss, que suelta la Elemental Wand.",
9: "§6Hunting Dimension§r · dimensión 28885\n\n"
   "Una dimensión para cazar: mobs más fuertes que dan más experiencia.\n\n"
   "§eEl portal:§r misma forma que el del Nether, hecho con §eHunting Dimension Frames§r "
   "(8 troncos alrededor de una flecha). Se activa con espada, arco o mechero, y se cruza §eagachado§r.\n\n"
   "§cReglas del servidor ahí adentro:§r los mobs tienen +30 % de vida y ataque y +4 de armadura, "
   "y §cno podés reaparecer en la dimensión§r si morís.\n\n"
   "Con el §eCreeping Moss§r podés cambiar el bioma de un chunk de la dimensión.",
10: "§6Cavern§r · dimensiones -50 a -56\n\n"
    "Siete mundos subterráneos, cada uno con sus minerales y peligros:\n"
    " · §eCavern§r (-50): la principal, con aguamarina y randomita.\n"
    " · §eRuins Cavern§r (-51) · §eAqua Cavern§r (-52) · §eCaveland§r (-53)\n"
    " · §eIce Cavern§r (-54) · §eCavenia§r (-55) · §eHuge Cavern§r (-56)\n\n"
    "§eCómo se entra:§r marco tipo portal del Nether de piedra musgosa o ladrillo de piedra, activado con una esmeralda. "
    "Cada caverna nueva pide su propia llave (aguamarina, hielo compacto, diamante, etc.).\n\n"
    "§aCavenia es zona de práctica:§r ahí no perdés inventario ni experiencia al morir.",
11: "§6Astral Sorcery§r · magia de las estrellas\n\n"
    "Magia que se alimenta de la luz de las estrellas: hace falta cielo abierto y noches despejadas.\n\n"
    "§eCómo empezar:§r conseguí un §eRock Crystal§r y el §eAstral Tome§r, el libro del mod "
    "(la receta está en JEI). El libro se va completando a medida que avanzás.\n\n"
    "§eProgresión:§r Luminous Crafting Table → Starlight Crafting Altar → Celestial Altar → Iridescent Altar. "
    "En el camino te sintonizás con una constelación y desbloqueás habilidades propias.\n\n"
    "§7Usá guías de la versión 1.12.2: el mod cambió mucho en versiones nuevas.§r",
12: "§6Draconic Evolution§r · tecnología dracónica\n\n"
    "Herramientas, armaduras y máquinas cada vez más poderosas, hechas con §edraconio§r y energía.\n\n"
    "§eDónde está el draconio:§r en el Overworld muy profundo (capas 2 a 8), en el Nether y en el End.\n\n"
    "§eProgresión:§r Draconic Core → Fusion Crafting (las recetas grandes del mod) → Wyvern → Awakened → Chaotic.\n\n"
    "§cNecesita el End:§r a partir del Wyvern Core hacen falta recursos del End, que se abre con la "
    "§eexpedición grupal§r del cap. 20.\n\n"
    "§cJefe:§r el Chaos Guardian, en las Chaos Islands del End, con 2000 de vida.",
13: "§6Harshen Universe§r · dimensión Pontus (5)\n\n"
    "Almas, sangre, rituales y accesorios (anillos, collares, pendientes).\n\n"
    "§eLa clave del mod:§r el castillo de §eKazzendre§r en el Overworld. Hay uno solo por mundo. "
    "Después de vencerlo, en la sala del tesoro está el §eSoul Harsher Pickaxe§r, el único pico que mina el "
    "Harshen Soul Ore.\n\n"
    "§eRituales:§r Lightning Ritual, Blood Ritual y Heretic Ritual. Con el Lightning Ritual se arma el "
    "spawner de la puerta a Pontus.\n\n"
    "Las flores de alma del Overworld dan Harshen Crystals.",
14: "§6Rustic§r · alquimia, vino y vida de campo\n\n"
    "Un mod tranquilo para la base:\n"
    " · §eAlquimia:§r el Condensador y la Retorta destilan hierbas (aloe, manzanilla, ginseng y más) en §eelixires§r.\n"
    " · §eBebidas:§r la tina de prensado saca jugo de uvas, manzanas u olivas, y el barril los fermenta en vino, sidra o hidromiel.\n"
    " · §eMiel y cera:§r el colmenar.\n"
    " · §eCultivos:§r tomate y chile (crecen sobre estacas) y uvas.\n\n"
    "También trae muebles y decoración: sillas, mesas, velas y candelabros.",
15: "§6Criaturas de la noche§r\n\n"
    "Varios mods hacen las noches mucho más peligrosas que en Minecraft normal:\n"
    " · §6Nightmares§r: al dormir hay 5 % de chance de pesadilla. Aparece una Hag, una Shadow Person o 8 Phantasmic Spiders.\n"
    " · §6SpookyCraft§r: animales esqueléticos y el Scarecrow.\n"
    " · §6Re-Zombies§r: zombis con oficio (mineros, caballeros, piratas…) y el Zombie King, que a veces suelta su armadura.\n"
    " · §6Elemental Creepers§r: 24 tipos de creepers que explotan con fuego, hielo, rayos y más.\n\n"
    "§eConsejo:§r iluminá bien la base y no salgas de noche sin escudo.",
16: "§6Depredadores§r · Deadly Monsters\n\n"
    "Los monstruos más peligrosos del servidor: la Woman, el Wideman, el Climber, el Mutant Steve y el Topielec, entre otros. "
    "Pegan fuerte y aguantan mucho.\n\n"
    "§eTrofeos:§r algunos sueltan partes raras (Woman's Heart, Wideman's Spine, Soul Eye).\n\n"
    "§cNo vayas solo ni con equipo de hierro.§r",
17: "§6Maldición lunar§r · Howling Moon\n\n"
    "Hombres lobo. Si uno te muerde, te podés contagiar de §elicantropía§r y convertirte en lobo.\n\n"
    "§eLa plata:§r el mod agrega mineral de plata. La §eespada de plata§r es el arma contra los hombres lobo.\n\n"
    "§eLa cura:§r la §ePoción de Wolfsbane§r (poción rara + flor Wolfsbane). Cura la infección o la licantropía, "
    "y si estás sano te vuelve inmune.\n\n"
    "§7Este mod no tiene jefes.§r",
18: "§6Enemigos infernales§r · Infernal Mobs\n\n"
    "Cualquier monstruo puede aparecer con poderes extra. Se reconocen por el §enombre de color§r sobre la cabeza.\n\n"
    "§eRangos:§r Élite (1 de cada 15), Ultra (1 de cada 7 élites) e Infernal (1 de cada 7 ultras). "
    "Hay 27 poderes posibles: veneno, robo de vida, explosiones, invisibilidad y más.\n\n"
    "§aSueltan mejor botín§r, pero §cno dan recompensas si los matás en una granja de mobs§r.",
19: "§6Guardianes y defensas§r\n\n"
    "Tres mods para proteger la base:\n"
    " · §6Totem Defender§r: tótems de madera, hierro, oro o diamante que disparan a lo que elijas (monstruos, animales u otros jugadores).\n"
    " · §6Mob Totems§r: tótems tallados que, con ofrendas, evitan que aparezcan monstruos, prenden fuego o envenenan.\n"
    " · §6SecurityCraft§r: teclados con clave, bloques reforzados, minas, cámaras y más.\n\n"
    "§7Recordá las reglas: las trampas valen, pero no pueden romper ni llevarse cosas de otros.§r",
20: "§6Grandes expediciones§r\n\n"
    "Los jefes de Minecraft, para enfrentar en grupo:\n"
    " · §eEl Wither§r: lo invocás vos. Suelta la estrella del Nether.\n"
    " · §eEl Elder Guardian§r: en los monumentos oceánicos.\n"
    " · §eEl Ender Dragon§r: §cexpedición grupal obligatoria§r. Nadie entra al End antes; se organiza entre todos.\n\n"
    "Después del dragón, el End queda abierto: Chaos Guardian, draconio del End y más.",
21: "§6El poder definitivo§r\n\n"
    "La cima de Draconic Evolution: equipo dracónico, núcleos caóticos y el armamento más fuerte del servidor.\n\n"
    "Se abre con la Fusion Crafting del cap. 12. Necesita muchos recursos, energía y fragmentos del Chaos Guardian.",
22: "§6Maestro de las dimensiones§r\n\n"
    "Pisá todas las dimensiones del servidor: Nether, End, Betweenlands, Trópicos, las 5 elementales, "
    "Hunting Dimension, Cavern y Pontus, y además las 7 cavernas.\n\n"
    "Es un capítulo para coleccionistas: se va completando solo mientras jugás los demás.",
23: "§6Coleccionista§r\n\n"
    "Logros difíciles de los mods grandes: anillos de la Betweenlands, el maestro de los hongos, "
    "el libro de herboristería completo y las herramientas compuestas de Cavern.\n\n"
    "No apurarse: son metas largas.",
24: "§6Arquitecto del mundo§r\n\n"
    " · §6MineColonies§r: fundá una colonia con aldeanos que trabajan para vos. El constructor levanta los edificios, "
    "y cada edificio trae un oficio nuevo (granjero, minero, leñador y más). Arrancás con un SupplyCamp o un SupplyShip.\n"
    " · §6MCA (Minecraft Comes Alive)§r: los aldeanos hablan, trabajan, tienen familia y te podés casar.\n\n"
    "Ideal para jugar tranquilo entre expediciones.",
25: "§6Desafíos legendarios§r\n\n"
    "Los combates más difíciles del servidor:\n"
    " · La trilogía de jefes finales: §ePrimordial Malevolence§r (Betweenlands), §eFire Boss§r (Elemental Dimensions) "
    "y §eChaos Guardian§r (Draconic Evolution).\n"
    " · El Wither tres veces.\n\n"
    "§cVayan en grupo y con el mejor equipo que tengan.§r",
26: "§6La última expedición§r\n\n"
    "El cierre del libro: recorriste todas las dimensiones y venciste a los jefes finales.\n\n"
    "Es opcional y no bloquea nada. Como premio te llevás el título de §6Leyenda de ArreMods§r.",
}

def chapter(name, desc, icon):
    num = int(name.split("Cap. ")[1].split(" ")[0])
    LINES.append((name, DESCRIPCIONES.get(num, desc), icon)); _line[0] = len(LINES) - 1

def quest(qid, x, y, name, desc, icon, tasks, rewards=(), prereq=(), logic="AND", main=False):
    QUESTS.append((qid, _line[0], x, y, dict(name=name, desc=desc, icon=icon, tasks=list(tasks),
                   rewards=expandir_premios(rewards), prereq=list(prereq), task_logic=logic, main=main)))

def any_craft(items): return [t_craft([i]) for i in items]
def any_get(items): return [t_get([i]) for i in items]

V = ""  # antes marcaba los datos verificados; se quitó del libro a pedido del administrador
P = "\n\n§c[en prueba]§r "

# =============================================================================
# BLOQUE I — Comenzando la aventura (compactado en v2)
# =============================================================================
chapter("Cap. 1 · Bienvenido a ArreMods", "El libro, las reglas y qué cambia en este mundo.", item("questbook:itemquestbook"))
quest(0, 0, 0, "Tu libro de aventuras",
      "Este libro es tu guía. No hay orden obligatorio y tu progreso es solo tuyo.\n\n"
      "§eUso:§r abrí una misión, hacé lo que pide y entregala o marcá la casilla. Si tiene premio, tocá §a\"Claim\"§r.\n"
      "Si perdés el libro: §elibro + palo§r.\n\n"
      "§6Reglas del servidor§r\n"
      "§e1.§r Somos todos amigos: buena onda, y si algo molesta se habla.\n"
      "§e2.§r §cNo se roba ni se rompe§r lo que es de otro jugador: casas, cofres, granjas, máquinas. "
      "Las tumbas también son de su dueño. Si rompés algo sin querer, lo arreglás o lo devolvés.\n"
      "§e3.§r §aLas trampas y las bromas valen.§r Si caés en una, te reís y listo; "
      "eso sí, la trampa no puede romper ni llevarse cosas ajenas.\n"
      "§e4.§r §cNadie va al End ni mata al dragón por su cuenta.§r Es la §eexpedición grupal§r "
      "(cap. 20) y se organiza entre todos.\n"
      "§e5.§r Pelear contra otro jugador solo si los dos están de acuerdo.\n"
      "§e6.§r Nada de hacks, x-ray ni programas para sacar ventaja.\n"
      "§e7.§r Si una granja o una máquina hace lagear el servidor, se apaga o se achica.\n"
      "§e8.§r Reclamá los chunks de tu base en el mapa de FTB Utilities: así nadie la puede romper sin querer. "
      "Si vas a construir cerca de otro, avisale antes.",
      item("questbook:itemquestbook"), [t_check()], [r_xp(1)], main=True)
quest(2, 48, 0, "Este mundo no es vanilla",
      "Hay decenas de mods: dimensiones nuevas, jefes, magia y tecnología. Cuando no sepas cómo se hace algo, preguntale a JEI.\n\n"
      "§eHerramientas de consulta:§r\n · JEI: §eR§r = cómo se fabrica, §eU§r = para qué sirve.\n"
      " · Hwyla: mirá un bloque y te dice qué es y de qué mod viene (no muestra el interior de los cajones)." + V,
      item("minecraft:crafting_table"), [t_check()], [], prereq=[0])
quest(5, 96, 0, "Tu primer mapa",
      "Abrí JourneyMap (§eJ§r), creá un waypoint en tu base (§eB§r) y ponele nombre.\n\n"
      "§7El mapa también marca dónde moriste.§r",
      item("minecraft:map"), [t_check()], [r_xp(2)], prereq=[0])

chapter("Cap. 2 · Los primeros días", "Madera, refugio, descanso, fuego y comida.", item("campfire:campfire"))
quest(10, 0, 0, "Madera y refugio",
      "Juntá §e16 troncos§r y armá un refugio con paredes, techo, puerta y luz adentro.\n\n"
      "§eConsejo:§r si no encontrás carbón, quemá troncos en el horno: sale carbón vegetal.",
      item("minecraft:log"), [t_get([item("minecraft:log", 16, WILD, "logWood")])],
      [r_items([item("minecraft:torch", 8)])], prereq=[0], main=True)
quest(12, 48, -24, "Descansar (Camping Mod y Nightmares)",
      "Fabricá una §etienda§r o un §esaco de dormir§r.\n"
      " · §6Navaja suiza:§r 6 tintes rojos + 3 hierro (el tinte rojo sale de las amapolas).\n"
      " · §6Saco:§r navaja arriba + 3 lanas.  §6Tienda:§r 5 lonas + 2 estacas.\n"
      " · Lona = cáñamo + navaja · Estaca = palo de hierro + navaja · Palo de hierro = 2 hierro en vertical.\n\n"
      "§cOjo:§r al dormir hay un §c5 %§r de chance de pesadilla. Dormí con equipo y vida llena." + V,
      item("camping:sleeping_bag"), any_craft([item("camping:tent", 1, WILD), item("camping:sleeping_bag", 1, WILD)]),
      [r_xp(3)], prereq=[10], logic="OR")
quest(13, 48, 24, "La fogata",
      "§6Camp Fire:§r 1 tronco arriba, 3 en el medio y 3 palos abajo (se apaga en ~6 min).\n"
      "También valen las fogatas del Camping Mod (5 palos, o 4 piedras labradas)." + V,
      item("campfire:campfire"),
      any_craft([item("campfire:campfire"), item("camping:campfire_wood_off"), item("camping:campfire_cook")]),
      [r_xp(2)], prereq=[10], logic="OR")
quest(16, 96, 24, "Comer bien y no perder todo",
      "Conseguí §ecualquier comida cocinada§r (carnes, pescado, papa asada, pan o venado del Camping Mod). "
      "\n\n"
      "§6Si morís:§r tu equipo queda en una §etumba§r (Tombstone); volvé a buscarla. "
      "En la §eHunting Dimension§r no podés reaparecer; en §eCavenia§r no perdés inventario ni experiencia." + V,
      item("minecraft:cooked_beef"),
      any_get([item("minecraft:cooked_beef"), item("minecraft:cooked_porkchop"), item("minecraft:cooked_chicken"),
               item("minecraft:cooked_mutton"), item("minecraft:cooked_rabbit"), item("minecraft:cooked_fish", 1, WILD),
               item("minecraft:baked_potato"), item("minecraft:bread"), item("camping:venison_cooked")]),
      [r_xp(2)], prereq=[13], logic="OR")

chapter("Cap. 3 · Preparación del aventurero", "Escudos, martillos y arcos.", item("spartanshields:shield_basic_wood"))
quest(20, 0, 0, "Equipo de verdad (Spartan Shields)",
      "Un escudo bloquea golpes y flechas con clic derecho. Los de Spartan Shields aguantan más que el de Minecraft.\n\n"
      "§6Escudo de madera:§r 6 tablones + 1 palo en diagonal. Para mejorarlo: escudo al centro + 4 del material "
      "(piedra labrada, hierro, oro, obsidiana o diamante)." + V,
      item("spartanshields:shield_basic_wood"), [t_craft([item("spartanshields:shield_basic_wood")])],
      [r_xp(3)], prereq=[0], main=True)
quest(23, 48, 0, "Martillo y desencantador",
      "§6Martillo (Hammer Time):§r rompe 3×3. 5 del material + 2 palos. Madera = §etroncos§r; piedra = §epiedra lisa§r.\n\n"
      "§6Disenchantment Table:§r saca encantamientos a un libro. Fila del medio: tinte amarillo, esmeralda, tinte amarillo; "
      "abajo: esmeralda, mesa de encantamientos, esmeralda. §cProbala antes con algo barato.§r" + V,
      item("hammertime:itemhammerstone"),
      any_craft([item("hammertime:itemhammerwood"), item("hammertime:itemhammerstone"), item("hammertime:itemhammeriron"),
                 item("hammertime:itemhammergold"), item("hammertime:itemhammerdiamond")]),
      [r_xp(3)], prereq=[20], logic="OR")
quest(22, 96, 0, "Switch-Bow §7[avanzado]",
      "Arco con carcaj: cambiás de flecha sin guardar nada.\n"
      "§6Switch-Bow:§r 3 palos + 1 ojo de ender + 3 hilos. §6Carcaj:§r cuero, hilo y un cofre (miralo en JEI).\n\n"
      "Necesita polvo de blaze (vara de blaze del Nether). §aNo bloquea nada.§r" + V,
      item("switchbow:switchbow"), [t_craft([item("switchbow:switchbow")])], [r_xp(5)], prereq=[20])

chapter("Cap. 4 · Explorador", "Orientarte, buscar biomas y moverte rápido.", item("naturescompass:naturescompass"))
quest(30, 0, 0, "Brújula de biomas",
      "§6Nature's Compass:§r 4 brotes en las esquinas, 4 troncos a los lados y una brújula al centro. "
      "Te dice dónde está el bioma que elijas, incluso de otros mods." + V,
      item("naturescompass:naturescompass"), [t_craft([item("naturescompass:naturescompass")])],
      [r_xp(3)], prereq=[0], main=True)
quest(31, 48, 0, "Tu primera semana de exploración",
      "Buscá con la brújula un bioma que no conozcas (Savanna, Mesa, Ice Spikes…), llegá y marcalo en JourneyMap. "
      "Anotá cuevas, aldeas y estructuras cerca de tu base.\n\n"
      "§7Los biomas de Tropicraft y Betweenlands están en sus dimensiones.§r",
      item("minecraft:filled_map"), [t_check()], [r_xp(3)], prereq=[30])
quest(32, 96, 0, "Cruzar rápido: puentes y portales",
      "§6Bridge Builder (Rope Bridge):§r gancho (5 hierro) + cañón (6 hierro + 3 cuerdas) + mango, en fila. "
      "Cuerda = 3 hilos + 3 enredaderas → 8. Cada bloque gasta 2 cuerdas, 2 hilos, 1 madera y 1 losa." + V,
      item("ropebridge:bridge_builder"), [t_check()], [], prereq=[30])

chapter("Cap. 5 · Tu primer asentamiento", "Territorio, mochilas, almacén y cultivos.", item("storagedrawers:basicdrawers"))
quest(40, 0, 0, "Reclamá tu terreno",
      "Con FTBUtilities reclamá al menos un chunk (mapa de reclamos, botón de FTB en el inventario). "
      "Usá §e/sethome§r y §e/home§r para volver a tu base.\n\n§7Los límites por jugador los fija el administrador.§r",
      item("minecraft:iron_door"), [t_check()], [], prereq=[0], main=True)
quest(42, 48, -24, "Tu primera mochila",
      "Fabricá §ecualquiera§r:\n · §6Backpacks:§r bolsillo = 5 cuero + 3 hilo; mochila = 7 cuero + placa de presión de oro.\n"
      " · §6Iron Backpacks:§r 4 lanas + 4 cueros + cofre al centro.\n · §6Camping Mod:§r bolsa = 1 hilo + 5 cueros." + V,
      item("backpacks16840:backpack", dmg=3),
      any_craft([item("backpacks16840:backpack", 1, WILD), item("backpacks16840:backpack_pouch", 1, WILD),
                 item("ironbackpacks:backpack", 1, WILD), item("camping:bag", 1, WILD)]),
      [r_xp(3)], prereq=[40], logic="OR")
quest(43, 48, 24, "Almacén ordenado",
      "§6Cajón 1×1 (Storage Drawers):§r 3 tablones arriba, cofre al centro, 3 tablones abajo. "
      "El §6controlador§r (piedra lisa, 2 comparadores, 1 cajón, 1 diamante) une todos los cajones.\n\n"
      "§6Chest Transporter:§r 6 palos; levanta un cofre lleno (da hambre y lentitud mientras lo llevás)." + V,
      item("storagedrawers:basicdrawers"), [t_craft([item("storagedrawers:basicdrawers", 1, WILD)])],
      [r_xp(3)], prereq=[40])
quest(45, 96, 24, "Tu primer cultivo",
      "Cosechá trigo, zanahoria, papa, remolacha, o tomate/chile de §eRustic§r (usan estaca: 3 tablones en vertical).\n\n"
      "§6Water Strainer:§r base (2 barrotes, tablones, tolva y cofre) + filtro (8 palos alrededor de una red): "
      "junta palos, arcilla y piedra; el denso da arena, grava y a veces oro." + V,
      item("rustic:tomato"),
      any_get([item("minecraft:wheat"), item("minecraft:carrot"), item("minecraft:potato"), item("minecraft:beetroot"),
               item("rustic:tomato"), item("rustic:chili_pepper")]),
      [r_xp(2)], prereq=[40], logic="OR")
quest(47, 96, -24, "Elegí tu próxima rama",
      "Tenés base, almacén y territorio. Desde acá todo está abierto: dimensiones (cap. 6-10), magia y tecnología "
      "(cap. 11-14) y combate (cap. 15-20). Elegí.",
      item("minecraft:nether_star"), [t_check()],
      [r_xp(5), r_title("Aventurero de ArreMods", ["Completaste el Bloque I", "de la guía de aventuras."])],
      prereq=[40, 42, 43], main=True)

# =============================================================================
# BLOQUE II — Exploración y dimensiones
# =============================================================================
chapter("Cap. 6 · The Betweenlands", "Un pantano oscuro con reglas propias y tres jefes. Dimensión 20.",
        item("thebetweenlands:swamp_talisman"))
BL = "thebetweenlands:"
quest(600, 0, 0, "El talismán del pantano",
      "En los pantanos del Overworld hay §eAltares Druídicos§r custodiados por §eDruidas Oscuros§r. "
      "Derrotalos: sueltan §ePiezas del Talismán del Pantano§r. Uní las 4 piezas en el Dark Druid Altar.\n\n"
      "Cada Druida Oscuro tiene 50 % de chance de soltar una pieza, y siempre es una que todavía no tenés en el inventario. "
      "Tenés que matarlo vos.\n\nSe completa sola al conseguir el talismán (logro \"Give Me That\")." + V,
      item(BL + "swamp_talisman"), [t_adv(BL + "adventurer/give_me_that")], [r_xp(5)], prereq=[0], main=True)
quest(601, 48, 0, "El árbol portal",
      "Usá el talismán sobre un brote para hacer crecer un §eÁrbol Portal§r y cruzá a la Betweenlands (dimensión 20).\n\n"
      "Logro \"Dank World\"." + V,
      item(BL + "swamp_talisman", dmg=5), [t_adv(BL + "adventurer/dank_world")], [r_xp(5)], prereq=[600])
quest(602, 96, -48, "Sobrevivir al pantano",
      "Acá las §cantorchas comunes no sirven§r, las herramientas del Overworld rinden menos y se corroen, y la comida se pudre. "
      "Juntá §eBalls of Sap§r (savia): curan la podredumbre.\n\nLogro \"A Cure\"." + V,
      item("minecraft:torch"), [t_adv(BL + "survivalist/a_cure")], [r_xp(3)], prereq=[601])
quest(603, 96, 0, "Madera del pantano",
      "Juntá madera local y fabricá una §eWeedwood Crafting Table§r: desde acá se fabrica casi todo.\n\n"
      "Logro \"All Over Again\"." + V,
      item(BL + "weedwood_planks"), [t_adv(BL + "craftsman/all_over_again")], [r_xp(3)], prereq=[601])
quest(604, 144, 0, "Metales del pantano",
      "Bajá a las cuevas y conseguí un lingote de §eSyrmorite§r u §eOctine§r.\n\nLogro \"New Shinies\"." + V,
      item("minecraft:iron_ingot"), [t_adv(BL + "miner/new_shinies")], [r_xp(4)], prereq=[603])
quest(605, 192, -24, "El horno doble de azufre",
      "Fabricá un §eDual Sulfur Furnace§r: funde dos cosas a la vez con azufre.\n\nLogro \"Efficiency\"." + V,
      item("minecraft:furnace"), [t_adv(BL + "craftsman/efficiency")], [r_xp(4)], prereq=[604])
quest(606, 192, 24, "Armas del pantano",
      "Conseguí una espada de la Betweenlands. Las armas del Overworld pegan menos acá.\n\nLogro \"Serious Business\"." + V,
      item("minecraft:iron_sword"), [t_adv(BL + "fighter/serious_business")], [r_xp(4)], prereq=[604])
quest(607, 240, 24, "Luchador sin miedo",
      "Derrotá a una Swamp Hag, un Wight, una Tar Beast, un Sludge y una Peat Mummy.\n\nLogro \"Fearless Fighter\"." + V,
      item("minecraft:skull", dmg=0), [t_adv(BL + "fighter/fearless_fighter")], [r_xp(6)], prereq=[606])
quest(608, 288, 0, "Jefe: Dreadful Peat Mummy",
      "Un jefe con barra de vida que surge de la turba. Llevá equipo de la Betweenlands y amigos.\n\n"
      "ID: thebetweenlands:dreadful_mummy" + V,
      item("minecraft:skull", dmg=2), [t_hunt(BL + "dreadful_mummy")], [r_xp(15)], prereq=[607])
quest(609, 288, 48, "Jefe: Spirit Tree",
      "El gran árbol espíritu defiende su claro. Hay que derrotar su §eCara Grande§r.\n\n"
      "ID: thebetweenlands:spirit_tree_face_large" + V,
      item(BL + "weedwood_planks"), [t_hunt(BL + "spirit_tree_face_large")], [r_xp(15)], prereq=[607])
quest(610, 144, -48, "La fortaleza Wight",
      "Encontrá una §eWight Fortress§r. Adentro espera el jefe final del pantano.\n\nLogro \"Enter The Stronghold\"." + V,
      item("minecraft:stonebrick"), [t_adv(BL + "adventurer/enter_the_stronghold")], [r_xp(5)], prereq=[601])
quest(611, 336, 24, "Jefe final: Primordial Malevolence",
      "El jefe de la Wight Fortress. Tiene torretas, barreras y teletransportes: vayan preparados.\n\n"
      "ID: thebetweenlands:fortress_boss" + V,
      item("minecraft:nether_star"), [t_hunt(BL + "fortress_boss")], [r_xp(30)], prereq=[610, 608], main=True)

chapter("Cap. 7 · Tropicraft", "Islas, cócteles y volcanes. Dimensión -127.", item("tropicraft:chair"))
TC = "tropicraft:"
quest(700, 0, 0, "Silla de playa",
      "§6Silla:§r 6 palos de bambú (columnas de los costados) + 3 lanas (columna del medio). El color depende de la lana." + V,
      item(TC + "chair"), [t_craft([item(TC + "chair", 1, WILD)])], [r_xp(3)], prereq=[0], main=True)
quest(701, 48, 0, "Una Piña Colada",
      "Prepará una §ePiña Colada§r en la §eDrink Mixer§r (8 bloques Chunk O' Head alrededor de una taza de bambú). "
      "Poné una taza de bambú (7 brotes en U) y mezclá §eananá§r (o cubos de ananá) con §ecoco§r (o trozo de coco). No lleva agua." + V,
      item(TC + "bamboo_mug"), [t_check()], [r_xp(2)], prereq=[700])
quest(702, 96, 0, "Viaje a los trópicos",
      "Sentate en la silla de playa §eal atardecer§r y tomá la Piña Colada: con su efecto te lleva a los trópicos (dimensión -127). "
      "El código del mod comprueba las tres cosas: silla, atardecer y efecto." + V,
      item(TC + "chair", dmg=4), [t_dim(-127, "Los Trópicos")], [r_xp(8)], prereq=[701])
quest(703, 144, -24, "Vida en las islas",
      "Explorá: aldeas §eKoa§r, cabezas §eEIH§r, volcanes, tiburones martillo y tortugas. Conseguí §eazurita§r y §ezircón§r.",
      item(TC + "azurite"), [t_get([item(TC + "azurite")]), t_get([item(TC + "zircon")])], [r_xp(4)], prereq=[702])
quest(704, 144, 24, "Varita del portal",
      "§6Tropics Portal Enchanter Wand:§r 3 palos de bambú en el centro, 2 azuritas y 2 zircones a los costados.\n"
      "§6Portal:§r un anillo 5×5 de §earenisca§r con un cuadrado 3×3 de §eagua§r adentro (aire arriba del agua, altura 9 o más). "
      "Hacé clic derecho cerca con la varita en modo construcción: arma el portal y gasta 1 de durabilidad. Sirve para ir y volver." + V,
      item(TC + "portal_enchanter"), [t_craft([item(TC + "portal_enchanter")])], [r_xp(5)], prereq=[703])

chapter("Cap. 8 · Elemental Dimensions", "Cinco dimensiones en línea: Tierra → Agua → Aire → Espíritu → Fuego (100-104).",
        item("elementaldimensions:earthrune"))
ED = "elementaldimensions:"
quest(800, 0, 0, "Polvo elemental",
      "Mineá §eElemental Dust Ore§r y juntá 8 de polvo. Con él y un bloque de oro + esmeralda se hace el §eAltar Center§r." + V,
      item(ED + "elementaldust"), [t_get([item(ED + "elementaldust", 8)])], [r_xp(3)], prereq=[0], main=True)
quest(801, 48, 0, "La Runa de Tierra",
      "Los §eGuardias§r de las mazmorras-portal sueltan la §eRuna de Tierra§r (según su tabla de botín). "
      "Esas mazmorras son raras: usá la brújula y explorá mucho." + V,
      item(ED + "earthrune"), [t_get([item(ED + "earthrune")])], [r_xp(5)], prereq=[800])
quest(802, 96, 0, "Dimensión Tierra",
      "El §ePortal Dialer§r está en las mazmorras-portal (no se fabrica). Con la runa en la mano, hacé clic derecho al dialer: "
      "la runa queda puesta y elige el destino. Parate en el lugar frente al dialer y esperá unos segundos. "
      "Con la mano vacía, clic derecho devuelve la runa. Los dialers de las otras dimensiones solo vuelven al Overworld." + V,
      item(ED + "earthrune"), [t_dim(100, "Tierra")], [r_xp(5)], prereq=[801])
quest(803, 144, -24, "Jefe: Dirt Zombie Boss",
      "Suelta la §eparte 3 de la Runa de Agua§r y el Digging Focus. Los Dirt Zombies comunes sueltan la parte 1." + V,
      item(ED + "focusdigging"), [t_hunt(ED + "ed_dirtzombieboss")], [r_xp(10)], prereq=[802])
quest(804, 144, 24, "Dimensión Agua",
      "Uní las 3 partes en la §eRuna de Agua§r (sin forma) y entrá al Agua (101).\n\n"
      "§6Las partes 2§r están en un cofre de la mazmorra de la dimensión anterior: Agua en la mazmorra de Tierra, "
      "Aire en la de Agua, Espíritu en la de Aire y Fuego en la de Espíritu." + V,
      item(ED + "waterrune"), [t_get([item(ED + "waterrune")]), t_dim(101, "Agua")], [r_xp(5)], prereq=[803])
quest(805, 192, -24, "Jefe: Water Creep Boss",
      "Suelta la §eparte 3 de la Runa de Aire§r y el Damage Focus. Los Water Creeps sueltan la parte 1. "
      "Su semilla de invocación es 4 semillas de trigo alrededor de un diamante." + V,
      item(ED + "focusdamage"), [t_hunt(ED + "ed_watercreepboss")], [r_xp(12)], prereq=[804])
quest(806, 192, 24, "Dimensión Aire",
      "Armá la §eRuna de Aire§r y entrá al Aire (102)." + V,
      item(ED + "airrune"), [t_get([item(ED + "airrune")]), t_dim(102, "Aire")], [r_xp(5)], prereq=[805])
quest(807, 240, -24, "Jefe: Ghost Boss",
      "Suelta la §eparte 3 de la Runa de Espíritu§r y el Teleport Focus. Los Ghosts sueltan la parte 1. "
      "Semilla de invocación: trigo alrededor de una esmeralda." + V,
      item(ED + "focusteleport"), [t_hunt(ED + "ed_ghostboss")], [r_xp(14)], prereq=[806])
quest(808, 240, 24, "Dimensión Espíritu",
      "Armá la §eRuna de Espíritu§r y entrá al Espíritu (103). Los Spirits sueltan partes 1 y 3 de la Runa de Fuego." + V,
      item(ED + "spiritrune"), [t_get([item(ED + "spiritrune")]), t_dim(103, "Espíritu")], [r_xp(5)], prereq=[807])
quest(809, 288, 0, "Dimensión Fuego",
      "Armá la §eRuna de Fuego§r y entrá al Fuego (104)." + V,
      item(ED + "firerune"), [t_get([item(ED + "firerune")]), t_dim(104, "Fuego")], [r_xp(6)], prereq=[808])
quest(810, 336, 0, "Jefe final: Fire Boss",
      "El último jefe. Suelta la §eElemental Wand§r. Su semilla usa una §eestrella del Nether§r (wither).\n\n"
      "§7No tiene barra de jefe.§r" + V,
      item(ED + "elementalwand"), [t_hunt(ED + "ed_fireboss")], [r_xp(25)], prereq=[809], main=True)

chapter("Cap. 9 · Hunting Dimension", "Una dimensión de caza con mobs más fuertes. Dimensión 28885.", item("huntingdim:frame"))
quest(900, 0, 0, "El marco del cazador",
      "§6Hunting Dimension Frame:§r 8 troncos alrededor de una flecha. El portal tiene la misma forma que el del Nether "
      "(marco de 4×5 como mínimo). Se activa con clic derecho usando una §eespada, un arco o un mechero§r. Para cruzar hay que §eagacharse§r." + V,
      item("huntingdim:frame"), [t_craft([item("huntingdim:frame", 1, WILD)])], [r_xp(3)], prereq=[0], main=True)
quest(901, 48, 0, "La cacería",
      "Entrá a la Hunting Dimension. Reglas del servidor: los mobs tienen §c+30 % de vida y ataque y +4 de armadura§r, "
      "dan más experiencia (×2,5 con 20 % de chance) y §cno podés reaparecer ahí§r si morís." + V,
      item("minecraft:bow"), [t_dim(28885, "Hunting Dimension")], [r_xp(6)], prereq=[900])
quest(902, 96, 0, "Musgo trepador",
      "El §eCreeping Moss§r cambia el bioma de un chunk dentro de la dimensión. "
      "Se hace con 8 bloques de piedra musgosa alrededor de un ingrediente (brote, hojas, enredadera, arena, hielo…)." + V,
      item("huntingdim:biome_changer"), [t_craft([item("huntingdim:biome_changer", 1, WILD)])], [r_xp(4)], prereq=[901])

chapter("Cap. 10 · Cavern", "Siete dimensiones subterráneas (-50 a -56).", item("cavern:cave_block"))
CV = "cavern:"
quest(1000, 0, 0, "El portal a la Caverna",
      "Armá un marco tipo portal del Nether con §epiedra musgosa o ladrillo de piedra§r y activalo con una §eesmeralda§r.\n\n"
      "Logro \"Cavern\" (entrar a la dimensión)." + V,
      item("minecraft:emerald"), [t_adv(CV + "root")], [r_xp(5)], prereq=[0], main=True)
quest(1001, 48, -24, "Cazador cavénico",
      "Derrotá a uno de cada monstruo cavénico.\n\nLogro \"Cavenic Hunter\"." + V,
      item("minecraft:bone"), [t_adv(CV + "kill_cavenic_mobs")], [r_xp(8)], prereq=[1000])
quest(1002, 48, 24, "Aguamarina y Aqua Cavern",
      "Conseguí §eaguamarina§r y entrá a la Aqua Cavern.\n\nLogros \"Aquamarine\" y \"Aqua Cavern\"." + V,
      item("cavern:aquamarine_pickaxe"), [t_adv(CV + "mine_aquamarine"), t_adv(CV + "enter_the_aqua_cavern")],
      [r_xp(5)], prereq=[1000])
quest(1003, 96, -48, "Ruins Cavern",
      "Mineá randomita, conseguí un §eMiner's Thought Orb§r y entrá a la Ruins Cavern.\n\nLogro \"Ruins Cavern\"." + V,
      item("minecraft:mossy_cobblestone"), [t_adv(CV + "enter_the_ruins_cavern")], [r_xp(5)], prereq=[1000])
quest(1004, 96, 0, "Caveland",
      "Juntá un brote en la caverna y entrá a Caveland.\n\nLogro \"Caveland\"." + V,
      item("cavern:perverted_sapling"), [t_adv(CV + "enter_the_caveland")], [r_xp(5)], prereq=[1000])
quest(1005, 96, 48, "Ice Cavern",
      "Conseguí hielo compacto y entrá a la Ice Cavern.\n\nLogro \"Ice Cavern\"." + V,
      item("minecraft:packed_ice"), [t_adv(CV + "enter_the_ice_cavern")], [r_xp(5)], prereq=[1000])
quest(1006, 144, 0, "Huge Cavern",
      "Con un diamante como llave, entrá a la Huge Cavern.\n\nLogro \"Huge Cavern\"." + V,
      item("minecraft:diamond"), [t_adv(CV + "enter_the_huge_cavern")], [r_xp(6)], prereq=[1000])
quest(1007, 144, -48, "Cavenia, zona de práctica",
      "Entrá a §eCavenia§r. En este servidor ahí §ano perdés inventario ni experiencia§r al morir: ideal para practicar combate.\n\n"
      "Logro \"Cavenia\"." + V,
      item("cavern:cavenic_bow"), [t_adv(CV + "cavenia/root")], [r_xp(5)], prereq=[1000])
quest(1008, 144, 48, "Magia de la caverna",
      "Conseguí un §eMagical Book§r: hechizos de teletransporte, invocación, fuego y más.\n\nLogro \"Study Magic\"." + V,
      item("cavern:magical_book"), [t_adv(CV + "get_magical_book")], [r_xp(5)], prereq=[1000])

# =============================================================================
# BLOQUE III — Artes, magia y tecnología
# =============================================================================
chapter("Cap. 11 · Astral Sorcery", "Magia de las estrellas (mecánicas clásicas de 1.12.2).", item("minecraft:glowstone_dust"))
AS = "astralsorcery:"
astral = [
    (1100, "Cristal de roca", "Conseguí un §eRock Crystal§r.", "rock_crystals", []),
    (1101, "Constelación brillante", "Descubrí una constelación brillante con el Looking Glass.", "find_constellation", [1100]),
    (1102, "Sintonizarte", "Sintonizate con una constelación brillante.", "attune_self", [1101]),
    (1103, "Altar de luz estelar", "Mejorá la Luminous Crafting Table a Starlight Crafting Altar.", "craft_t2_altar", [1102]),
    (1104, "Cristal sintonizado", "Sintonizá un cristal con una constelación.", "attune_crystal", [1103]),
    (1105, "Constelación tenue", "Descubrí una constelación tenue con el Telescope.", "find_weak_constellation", [1103]),
    (1106, "Altar celestial", "Fabricá un Celestial Altar.", "craft_t3_altar", [1104]),
    (1107, "Altar iridiscente", "Fabricá un Iridescent Altar.", "craft_t4_altar", [1106, 1105]),
    (1108, "Luz interior", "Llevá tu luz estelar personal a nivel 20.", "perk_level_medium", [1102]),
]
for i, (qid, nm, ds, adv, pre) in enumerate(astral):
    quest(qid, 48 * i, 0 if i % 2 == 0 else 24, nm,
          ds + "\n\n§7Usá solo guías de la versión 1.12.2 (no del rework moderno).§r\nLogro del mod: " + adv + V,
          item("minecraft:glowstone_dust"), [t_adv(AS + adv)], [r_xp(4 + i)], prereq=pre or [0], main=(i == 0))

chapter("Cap. 12 · Draconic Evolution", "Tecnología dracónica. Requiere ir al End y vencer al dragón.",
        item("draconicevolution:draconic_core"))
DE = "draconicevolution:"
quest(1200, 0, 0, "Draconio",
      "Mineá §eDraconium Ore§r y fundí 4 lingotes. Dónde aparece: §eOverworld§r y otras dimensiones de mods, en piedra, muy profundo (capas 2 a 8); "
      "§eNether§r (capas 1 a 125) y §eEnd§r (capas 1 a 70, vetas más grandes)." + V,
      item(DE + "draconium_ingot"), [t_get([item(DE + "draconium_ingot", 4)])], [r_xp(4)], prereq=[0], main=True)
quest(1201, 48, 0, "Núcleo dracónico",
      "Fabricá un §eDraconic Core§r (receta en JEI).",
      item(DE + "draconic_core"), [t_craft([item(DE + "draconic_core")])], [r_xp(5)], prereq=[1200])
quest(1202, 96, 0, "Fusion Crafting",
      "Fabricá el §eFusion Crafting Core§r y sus inyectores: así se hacen las recetas grandes del mod.",
      item(DE + "fusion_crafting_core"), [t_craft([item(DE + "fusion_crafting_core")])], [r_xp(6)], prereq=[1201])
quest(1204, 144, 0, "Núcleo Wyvern",
      "Fabricá un §eWyvern Core§r. Necesita recursos del End: se desbloquea con la §eexpedición grupal§r del cap. 20.",
      item(DE + "wyvern_core"), [t_craft([item(DE + "wyvern_core")])], [r_xp(8)], prereq=[1202, 2102])
quest(1205, 192, 0, "Equipo Wyvern",
      "Conseguí cualquier pieza de equipo Wyvern.",
      item(DE + "wyvern_pick"),
      any_get([item(DE + x) for x in ("wyvern_pick", "wyvern_sword", "wyvern_axe", "wyvern_shovel", "wyvern_bow",
                                       "wyvern_helm", "wyvern_chest", "wyvern_legs", "wyvern_boots")]),
      [r_xp(10)], prereq=[1204], logic="OR")
quest(1206, 240, -48, "Jefe legendario: Chaos Guardian",
      "Vive en las §eChaos Islands§r del End. En este servidor tiene §c2000 de vida§r y su isla §cexplota§r al romper el cristal del caos." + V,
      item(DE + "chaos_shard"), [t_hunt(DE + "chaosguardian")], [r_xp(40)], prereq=[1205], main=True)
quest(1207, 288, 0, "Núcleo despertado",
      "Con draconio despertado y fragmentos del caos, fabricá un §eAwakened Core§r.",
      item(DE + "awakened_core"), [t_craft([item(DE + "awakened_core")])], [r_xp(15)], prereq=[1206])

chapter("Cap. 13 · Harshen Universe", "Almas, sangre y la dimensión Pontus (5).", item("harshenuniverse:harshen_soul_fragment"))
HU = "harshenuniverse:"
quest(1300, 0, 0, "Un universo de almas",
      "Harshen Universe agrega almas, sangre, accesorios (anillos, pendientes) y la dimensión §ePontus§r.\n\n"
      "§7Aviso técnico: el error del archivo de accesorios solo afecta al ajuste de daño del §ePunchy Ring§r, que queda con su valor de fábrica. Los demás accesorios funcionan.§r" + V,
      item(HU + "harshen_soul_fragment"), [t_check()], [r_xp(2)], prereq=[0], main=True)
quest(1301, 48, 0, "Mineral de almas",
      "§6Harshen Soul Ingot:§r Harshen Soul Fragment al centro, Harshen Crystal a los costados y Emerald Shard arriba y abajo. "
      "El fragmento sale del §eHarshen Soul Ore§r, que solo se mina con el §eSoul Harsher Pickaxe§r (botín del castillo de Kazzendre). "
      "El cristal sale de la §eHarshen Soul Flower§r del Overworld." + V,
      item(HU + "harshen_soul_ingot"), [t_get([item(HU + "harshen_soul_ingot")])], [r_xp(5)], prereq=[1300])
quest(1302, 96, 0, "Pontus",
      "Juntá las §e3 partes del Pontus World Gate Spawner§r (cofres del castillo de Kazzendre y santuarios del Overworld) "
      "y unilas con un fragmento de alma en el §eLightning Ritual§r. Usá el spawner sobre un bloque: aparece la §eHarshen Dimensional Gate§r. "
      "La normal dura un tiempo limitado; para reactivarla, tirale un §eRitual Crystal activo§r. La versión mejorada es permanente." + V,
      item(HU + "pontus_cube"), [t_dim(5, "Pontus")], [r_xp(8)], prereq=[1301])
quest(1303, 144, 0, "Kazzendre",
      "El señor del castillo del Overworld (hay uno solo por mundo). No tiene barra de jefe, pero tiene §c380 de vida§r y armadura. "
      "Después de él hay una sala del tesoro con el Soul Harsher Pickaxe." + V,
      item(HU + "harshen_crystal"), [t_hunt(HU + "kazzendre")], [r_xp(15)], prereq=[1302])

chapter("Cap. 14 · Rustic", "Alquimia, vino, miel y decoración medieval.", item("rustic:elixir"))
RU = "rustic:"
quest(1500, 0, 0, "Condensador",
      "§6Condenser:§r ladrillos alrededor de un balde, con arcilla endurecida blanca abajo al centro. "
      "Destila hierbas para hacer §eelixires§r." + V,
      item(RU + "condenser"), [t_craft([item(RU + "condenser")])], [r_xp(4)], prereq=[0], main=True)
quest(1501, 48, -24, "Retorta",
      "§6Retort:§r 2 ladrillos, 1 hierro y 1 balde. Va al lado del condensador." + V,
      item(RU + "retort"), [t_craft([item(RU + "retort")])], [r_xp(3)], prereq=[1500])
quest(1502, 96, -24, "Tu primer elixir",
      "Destilá un §eelixir§r con hierbas de Rustic (aloe, chamomile, ginseng, etc.). Se hacen en el condensador, no en el soporte de pociones." + V,
      item(RU + "elixir"), [t_get([item(RU + "elixir", 1, WILD)])], [r_xp(6)], prereq=[1501])
quest(1503, 48, 24, "Tina de prensado",
      "§6Crushing Tub:§r tablones, hierro y losas. Pisá uvas, manzanas u olivas para hacer jugo." + V,
      item(RU + "crushing_tub"), [t_craft([item(RU + "crushing_tub")])], [r_xp(3)], prereq=[1500])
quest(1504, 96, 24, "Barril de fermentación",
      "§6Brewing Barrel:§r tablones, hierro y losas. Fermenta jugos en vino, sidra o hidromiel." + V,
      item(RU + "brewing_barrel"), [t_craft([item(RU + "brewing_barrel")])], [r_xp(4)], prereq=[1503])
quest(1505, 144, 0, "Colmenar",
      "§6Apiary:§r troncos arriba y abajo, tablones a los costados. Da miel y cera de abeja." + V,
      item(RU + "apiary"), [t_craft([item(RU + "apiary")])], [r_xp(3)], prereq=[1500])

# =============================================================================
# BLOQUE IV — Combate y desafíos
# =============================================================================
chapter("Cap. 15 · Criaturas de la noche", "Pesadillas, esqueletos espeluznantes y zombis especiales.", item("minecraft:skull", dmg=2))
quest(1600, 0, 0, "Pesadillas",
      "Cuando dormís hay §e5 % de chance§r de pesadilla: te despierta y aparece una de tres, con la misma probabilidad: "
      "una §eHag§r, una §eShadow Person§r o 8 §ePhantasmic Spiders§r. Derrotá a cualquiera." + V,
      item("minecraft:bed", dmg=15), [t_hunt("nightmares:hag"), t_hunt("nightmares:shadow"), t_hunt("nightmares:spider")],
      [r_xp(6)], prereq=[0], logic="OR", main=True)
quest(1601, 48, -24, "El espantapájaros",
      "SpookyCraft agrega animales esqueléticos y un §eScarecrow§r. Derrotalo.\n\nID: spookycraft:scarecrow" + V,
      item("minecraft:pumpkin"), [t_hunt("spookycraft:scarecrow")], [r_xp(5)], prereq=[1600])
quest(1602, 48, 24, "El Rey Zombi",
      "Re-Zombies agrega zombis con oficio: mineros, caballeros, piratas… Derrotá al §eZombie King§r: "
      "al morir tiene §e20 % de chance§r de soltar una pieza de su armadura (5 % cada una: casco, peto, pantalón o botas).\n\n"
      "ID: rezombiesv15ver1122jar:zombieking" + V,
      item("rezombiesv15ver1122jar:kingarmourhelmet"), [t_hunt("rezombiesv15ver1122jar:zombieking")], [r_xp(8)], prereq=[1600])
quest(1603, 96, 0, "Creepers elementales",
      "Hay 24 tipos de creepers elementales. Derrotá a uno de fuego, uno de hielo y uno eléctrico." + V,
      item("minecraft:gunpowder"),
      [t_hunt("elementalcreepers:firecreeper"), t_hunt("elementalcreepers:icecreeper"), t_hunt("elementalcreepers:lightningcreeper")],
      [r_xp(8)], prereq=[1600])

chapter("Cap. 16 · Depredadores", "Deadly Monsters: los monstruos más peligrosos.", item("dmonsters:souleye"))
quest(1700, 0, 0, "Monstruos mortales",
      "Deadly Monsters trae criaturas muy peligrosas. Derrotá a §ecualquiera§r de: Woman, Wideman, Climber, Mutant Steve o Topielec.\n\n"
      "§7El Zombie Chicken no suelta botín (falta su tabla).§r" + V,
      item("dmonsters:souleye"),
      [t_hunt("dmonsters:" + e) for e in ("woman", "wideman", "climber", "mutantsteve", "topielec")],
      [r_xp(8)], prereq=[0], logic="OR", main=True)
quest(1701, 48, 0, "Coleccionista de trofeos",
      "Conseguí un trofeo: §eWoman's Heart§r, §eWideman's Spine§r o §eSoul Eye§r.",
      item("dmonsters:womanheart"), any_get([item("dmonsters:womanheart"), item("dmonsters:widemanspine"), item("dmonsters:souleye")]),
      [r_xp(6)], prereq=[1700], logic="OR")

chapter("Cap. 17 · Maldición lunar", "Howling Moon: licantropía. Sin jefes.", item("howlingmoon:moonstone"))
HM = "howlingmoon:"
quest(1800, 0, 0, "Plata",
      "Conseguí un §elingote de plata§r (mineral de plata de Howling Moon).",
      item(HM + "ingot_silver"), [t_get([item(HM + "ingot_silver")])], [r_xp(3)], prereq=[0], main=True)
quest(1801, 48, 0, "Espada de plata",
      "§6Silver Sword:§r 2 lingotes de plata y un palo, en vertical. Efectiva contra hombres lobo." + V,
      item(HM + "silver_sword"), [t_craft([item(HM + "silver_sword")])], [r_xp(4)], prereq=[1800])
quest(1802, 96, -24, "Noche de luna llena",
      "Derrotá a un §ehombre lobo§r.\n\nID: howlingmoon:entitywerewolf" + V,
      item(HM + "moonstone"), [t_hunt(HM + "entitywerewolf")], [r_xp(8)], prereq=[1801])
quest(1803, 96, 24, "La cura",
      "§6Receta:§r poción rara (Awkward Potion) + flor §eWolfsbane§r en el soporte de pociones. Al tomarla te da 30 s de veneno y náuseas, y además: "
      "si sos hombre lobo te cura; si estás infectado, cura la infección; si no, te vuelve inmune (o te quita la inmunidad)." + V,
      item(HM + "potion_wolfsbane"), [t_get([item(HM + "potion_wolfsbane", 1, WILD)])], [r_xp(5)], prereq=[1800])

chapter("Cap. 18 · Enemigos infernales", "Infernal Mobs: monstruos con poderes extra.", item("minecraft:blaze_powder"))
quest(1900, 0, 0, "Reconocer un infernal",
      "Cualquier monstruo puede salir con modificadores. Rarezas del servidor: §eÉlite§r 1 de 15, §6Ultra§r 1 de 7 entre élites, "
      "§cInfernal§r 1 de 7 entre ultra. Hay 27 modificadores activos (veneno, robo de vida, explosión, etc.).\n\n"
      "§cAntigranjas activo:§r si los matás en una trampa de mobs, dejan de dar recompensas." + V,
      item("minecraft:blaze_powder"), [t_check()], [r_xp(2)], prereq=[0], main=True)
quest(1901, 48, 0, "Tu primer infernal",
      "Derrotá a un monstruo con nombre de color (élite, ultra o infernal) y marcá la casilla.\n§7(Esta misión confía en tu palabra.)§r",
      item("minecraft:golden_sword"), [t_check()], [r_xp(8)], prereq=[1900])

chapter("Cap. 19 · Guardianes y defensas", "Totems defensores, tótems espirituales y SecurityCraft.", item("totemdefender:core"))
quest(2000, 0, 0, "Núcleo defensor (Totem Defender)",
      "§6Core:§r 6 lapislázuli, 1 perla de ender y 1 bloque de redstone. Los §eTotems§r (madera, hierro, oro, diamante) "
      "disparan a lo que elijas con sus filtros (enemigos, animales, otros jugadores)." + V,
      item("totemdefender:core"), [t_craft([item("totemdefender:core")])], [r_xp(5)], prereq=[0], main=True)
quest(2001, 48, -24, "Tótems espirituales (Mob Totems)",
      "§6Pasos:§r 1) §eTotemic Focus§r (pólvora, pluma y palos): clic derecho a un tronco lo vuelve madera de tótem. "
      "2) §eCarving Knife§r (pedernal y palo): clic derecho al aire elige el tallado y clic derecho a la madera la talla. "
      "3) Tótem de 2 o 3 bloques con una §eOffering Box§r al lado del bloque de abajo, cargada con ofrendas.\n"
      "Creeper: no aparecen monstruos (radio 32). Cow: no aparecen animales. Blaze: prende fuego. Spider: envenena. "
      "Modificadores: Ocelot +16 de radio, Wither −16, Llama +2 de daño, Rabbit más velocidad. §7El Wolf todavía no funciona.§r" + V,
      item("mobtotems:carving_knife"), [t_get([item("mobtotems:carving_knife")])], [r_xp(4)], prereq=[2000])
quest(2002, 48, 24, "Seguridad (SecurityCraft)",
      "Teclados con contraseña, bloques reforzados, minas y cámaras. Fabricá un §eKey Panel§r (8 botones de piedra alrededor de una placa de presión pesada). "
      "Para el teclado: colocá un §eFrame§r (7 hierros y 1 redstone) y hacé clic derecho con el Key Panel. "
      "Al teclado se le pone una clave y da 3 s de redstone al acertarla." + V,
      item("securitycraft:keypad_item"), [t_get([item("securitycraft:keypad_item")])], [r_xp(4)], prereq=[2000])

chapter("Cap. 20 · Grandes expediciones", "Jefes vanilla y expediciones en grupo.", item("minecraft:nether_star"))
quest(2100, 0, 0, "Expediciones en grupo",
      "Los jefes grandes se enfrentan mejor en equipo. Tu progreso del libro sigue siendo individual: cada uno completa sus misiones.\n\n"
      "§7Los puntos de clan y el ranking llegarán con PV7Core.§r",
      item("minecraft:shield"), [t_check()], [], prereq=[0], main=True)
quest(2101, 48, -24, "El Wither",
      "Invocá y derrotá al §eWither§r. Suelta la estrella del Nether (la pide la semilla del Fire Boss).",
      item("minecraft:nether_star"), [t_hunt("minecraft:wither")], [r_xp(25)], prereq=[2100])
quest(2102, 48, 24, "Expedición grupal: el End",
      "§cRegla del servidor:§r nadie entra al End ni mata al dragón por su cuenta. "
      "La expedición se organiza entre todos: busquen juntos el portal, entren juntos y derroten al §eEnder Dragon§r en grupo.\n\n"
      "Se completa para §ecada jugador que entre al End§r con la expedición. Después del dragón, el End queda abierto para todos "
      "(Chaos Guardian y draconio del End).",
      item("minecraft:dragon_egg"), [t_dim(1, "The End")], [r_xp(20)], prereq=[2100])
quest(2103, 96, 0, "Guardián del templo",
      "Derrotá a un §eElder Guardian§r de un monumento oceánico.",
      item("minecraft:prismarine_shard"), [t_hunt("minecraft:elder_guardian")], [r_xp(12)], prereq=[2100])

# =============================================================================
# BLOQUE V — Maestría
# =============================================================================
chapter("Cap. 21 · El poder definitivo", "La cima de Draconic Evolution.", item("draconicevolution:chaotic_core"))
quest(2200, 0, 0, "Equipo dracónico",
      "Conseguí cualquier pieza de equipo §eDraconic§r.",
      item(DE + "draconic_chest"),
      any_get([item(DE + x) for x in ("draconic_pick", "draconic_sword", "draconic_axe", "draconic_shovel", "draconic_bow",
                                       "draconic_helm", "draconic_chest", "draconic_legs", "draconic_boots")]),
      [r_xp(20)], prereq=[1207], logic="OR", main=True)
quest(2201, 48, 0, "Núcleo caótico",
      "Fabricá un §eChaotic Core§r.",
      item(DE + "chaotic_core"), [t_craft([item(DE + "chaotic_core")])], [r_xp(30)], prereq=[2200])
quest(2202, 48, 48, "Almacén de energía",
      "Fabricá un §eEnergy Storage Core§r para guardar energía en grande.",
      item(DE + "energy_storage_core"), [t_craft([item(DE + "energy_storage_core")])], [r_xp(10)], prereq=[1202])

chapter("Cap. 22 · Maestro de las dimensiones", "Pisá todas las dimensiones del servidor.", item("minecraft:ender_eye"))
dims = [(-1, "Nether"), (1, "End"), (20, "Betweenlands"), (-127, "Trópicos"), (100, "Tierra elemental"),
        (101, "Agua elemental"), (102, "Aire elemental"), (103, "Espíritu elemental"), (104, "Fuego elemental"),
        (28885, "Hunting Dimension"), (-50, "Cavern"), (5, "Pontus")]
quest(2300, 0, 0, "Viajero de mundos",
      "Visitá §e12 dimensiones§r: Nether, End, Betweenlands, Trópicos, las 5 elementales, Hunting Dimension, Cavern y Pontus. "
      "Cada tarea se completa sola al llegar.",
      item("minecraft:ender_eye"), [t_dim(d, n) for d, n in dims], [r_xp(30)], prereq=[0], main=True)
quest(2301, 48, 0, "Todas las cavernas",
      "Entrá a las 7 dimensiones de Cavern.",
      item("cavern:cave_block"),
      [t_adv(CV + a) for a in ("root", "enter_the_aqua_cavern", "enter_the_ruins_cavern", "enter_the_caveland",
                               "enter_the_ice_cavern", "enter_the_huge_cavern", "cavenia/root")],
      [r_xp(15)], prereq=[2300])

chapter("Cap. 23 · Coleccionista", "Logros difíciles de completar.", item("minecraft:chest"))
quest(2400, 0, 0, "Todos los anillos",
      "Conseguí todos los anillos de la Betweenlands.\n\nLogro \"None To Rule Them All\"." + V,
      item("minecraft:gold_nugget"), [t_adv(BL + "adventurer/none_to_rule_them_all")], [r_xp(15)], prereq=[601], main=True)
quest(2401, 48, -24, "Maestro de los hongos",
      "Juntá todos los hongos de la Betweenlands.\n\nLogro \"Mushroom Master\"." + V,
      item("minecraft:brown_mushroom"), [t_adv(BL + "farmer/mushroom_master")], [r_xp(10)], prereq=[2400])
quest(2402, 48, 24, "Libro de herboristería completo",
      "Completá el Herblore Book.\n\nLogro \"Fully Booked\"." + V,
      item("minecraft:book"), [t_adv(BL + "herbalist/fully_booked")], [r_xp(15)], prereq=[2400])
quest(2403, 96, 0, "Herramientas compuestas",
      "Fabricá una herramienta compuesta con magia de Cavern.\n\nLogro \"Fantastic Tools\"." + V,
      item("cavern:composite_pickaxe"), [t_adv(CV + "composite_tools")], [r_xp(12)], prereq=[1008])

chapter("Cap. 24 · Arquitecto del mundo", "Colonias y aldeanos.", item("minecolonies:blockhuttownhall"))
quest(2500, 0, 0, "Fundá una colonia (MineColonies)",
      "Para empezar: §eSupplyCamp Chest§r (5 cofres en U, necesita un terreno plano de 16×17 sin pasto ni flores) "
      "o §eSupplyShip Chest§r (5 botes en U, va en el agua). Cada jugador puede colocar solo uno. Después colocá el §eTown Hall§r." + V,
      item("minecolonies:blockhuttownhall"), [t_get([item("minecolonies:blockhuttownhall")])], [r_xp(8)], prereq=[0], main=True)
quest(2501, 48, 0, "Tu primer constructor",
      "Colocá la choza del §eBuilder§r: es quien construye todo lo demás.",
      item("minecolonies:blockhutbuilder"), [t_get([item("minecolonies:blockhutbuilder")])], [r_xp(6)], prereq=[2500])
quest(2502, 0, 48, "Vida en la aldea (MCA)",
      "MCA cambia a los aldeanos: hablan, trabajan, se casan. §6Anillo de compromiso:§r 7 lingotes de oro (o de oro rosa) en anillo con un diamante arriba al medio." + V,
      item("mca:engagement_ring"), any_get([item("mca:engagement_ring"), item("mca:engagement_ring_rg")]),
      [r_xp(6)], prereq=[0], logic="OR")

chapter("Cap. 25 · Desafíos legendarios", "Los combates más difíciles del servidor.", item("minecraft:diamond_sword"))
quest(2600, 0, 0, "Trilogía de jefes finales",
      "Derrotá a Primordial Malevolence, al Fire Boss y al Chaos Guardian.",
      item("minecraft:diamond_sword"),
      [t_hunt(BL + "fortress_boss"), t_hunt(ED + "ed_fireboss"), t_hunt(DE + "chaosguardian")],
      [r_xp(50)], prereq=[611, 810, 1206], main=True)
quest(2601, 48, 0, "Wither en serie",
      "Derrotá al Wither 3 veces.",
      item("minecraft:nether_star"), [t_hunt("minecraft:wither", 3)], [r_xp(30)], prereq=[2101])

chapter("Cap. 26 · La última expedición", "Opcional. No bloquea nada.", item("minecraft:dragon_egg"))
quest(2700, 0, 0, "Leyenda de ArreMods",
      "Recorriste todas las dimensiones y venciste a los jefes finales. Tu nombre queda en la historia del servidor.",
      item("minecraft:dragon_egg"), [t_check()],
      [r_xp(50), r_title("Leyenda de ArreMods", ["Completaste la guía de aventuras", "de ArreMods."])],
      prereq=[2300, 2600], main=True)


# =============================================================================
# Textos ampliados: reemplazan la descripción corta de cada misión.
# Datos sacados del código y los archivos de cada mod (ver pv7-docs/07).
# =============================================================================
TEXTOS = {
5: "Apretá §eJ§r para abrir JourneyMap. Con §eB§r creás un §ewaypoint§r (un punto guardado) en donde estás parado: "
   "ponele un nombre como \"Casa\" y un color.\n\n"
   "Los waypoints se ven en el mapa y como un marcador en el mundo, así nunca te perdés. "
   "Hacé uno en cada lugar importante: tu base, una aldea, una cueva con minerales, un portal.\n\n"
   "§7Cuando morís, el mapa marca solo el lugar con un waypoint de muerte: ahí está tu tumba.§r",
31: "Abrí la §eNature's Compass§r (clic derecho), elegí un bioma que no conozcas (Savanna, Mesa, Ice Spikes, Mushroom Island…) "
    "y seguí la flecha. Cuando llegues, hacé un waypoint en JourneyMap y marcá la casilla.\n\n"
    "En el camino anotá en el mapa lo que veas: §ecuevas§r con minerales, §ealdeas§r para comerciar, "
    "§etemplos y estructuras§r con cofres. Muchas estructuras de mods también tienen botín.\n\n"
    "§7Los biomas de Tropicraft y Betweenlands no están en el Overworld: viven en sus propias dimensiones (cap. 6 y 7).§r",
40: "Para que nadie rompa tu base sin querer, §ereclamá los chunks§r donde está:\n"
    " · Abrí el inventario y tocá el botón de §eFTB Utilities§r (arriba a la izquierda) → §eClaimed Chunks§r.\n"
    " · En el mapa, hacé §eclic izquierdo§r sobre los cuadrados para reclamarlos (clic derecho los libera).\n\n"
    "Además: §e/sethome§r guarda tu casa y §e/home§r te lleva de vuelta desde cualquier lado. Útil cuando te perdés o se hace de noche.\n\n"
    "§7La cantidad de chunks que podés reclamar la fija el administrador.§r",
47: "Ya tenés base, almacén y territorio. Desde acá el libro se abre y podés seguir por donde quieras:\n"
    " · §6Dimensiones§r (cap. 6 a 10): pantanos, trópicos, cinco mundos elementales, caza y cavernas.\n"
    " · §6Magia y tecnología§r (cap. 11 a 14): estrellas, dragones, almas y alquimia.\n"
    " · §6Combate§r (cap. 15 a 20): monstruos de la noche, depredadores, hombres lobo y jefes.\n\n"
    "§eConsejo:§r si es tu primera vez con mods, empezá por §eCavern§r (cap. 10) o §eTropicraft§r (cap. 7): son los más fáciles.",

# --- Cap. 6 · The Betweenlands ---
600: "La Betweenlands se abre con el §eTalismán del Pantano§r. Cómo conseguirlo:\n"
     " 1. Buscá en los §epantanos del Overworld§r un §eDark Druid Altar§r: un altar de piedra rodeado de pilares.\n"
     " 2. Cerca aparecen §eDruidas Oscuros§r. Matalos vos: cada uno tiene 50 % de chance de soltar una §ePieza del Talismán§r, "
     "y siempre es una que todavía no tenés.\n"
     " 3. Cuando juntes las §e4 piezas§r, ponelas en el altar: se unen en el talismán.\n\n"
     "§eConsejo:§r los druidas se teletransportan y te tiran hacia ellos. Llevá comida y una espada de hierro.",
601: "Con el talismán en la mano, hacé §eclic derecho sobre un brote§r plantado en el Overworld: crece un §eÁrbol Portal§r gigante. "
     "Entrá por el hueco del tronco y cruzás a la Betweenlands.\n\n"
     "El talismán queda §evinculado§r a ese portal (lo dice al pasar el mouse por encima). El mismo árbol sirve para volver.\n\n"
     "§cAntes de cruzar:§r llevá comida, bloques y un pico. Del otro lado la vida es más difícil.",
602: "La Betweenlands castiga a los recién llegados:\n"
     " · Las §cantorchas comunes no prenden§r. Hacé §eSulfur Torches§r: azufre arriba y un palo de weedwood abajo (da 4). "
     "El azufre se mina en las paredes de piedra del pantano.\n"
     " · Las herramientas del Overworld §crinden menos§r y se §ecorroen§r con el uso.\n"
     " · Tenés una barra de §edescomposición§r (decay): si baja, perdés vida máxima. "
     "La bajan las §eBalls of Sap§r (savia), que salen de romper troncos de §eSap Tree Log§r (los árboles de savia).\n\n"
     "Juntá savia para completar la misión y llevá siempre algunas encima.",
603: "Talá árboles de §eweedwood§r (los troncos oscuros del pantano). Cada tronco da tablones de weedwood, "
     "y con tablones hacés palos de weedwood.\n\n"
     "§6Weedwood Crafting Table:§r 4 tablones de weedwood en cuadrado.\n\n"
     "Desde esta mesa se fabrica casi todo el equipo de la dimensión. "
     "Empezá con un §epico de weedwood§r para poder minar piedra.",
604: "En las cuevas de la Betweenlands hay dos metales nuevos:\n"
     " · §eSyrmorite§r: el hierro del pantano. Para armaduras, baldes y escudos.\n"
     " · §eOctine§r: un metal caliente que hasta prende fuego al musgo. Para herramientas mejores.\n\n"
     "Se funden en el §eSulfur Furnace§r: 8 bloques de betweenstone en anillo (como el horno común). "
     "Usa azufre como combustible.\n\n"
     "Conseguí un lingote de cualquiera de los dos.",
605: "§6Dual Sulfur Furnace:§r un Sulfur Furnace al centro y 8 betweenstone alrededor.\n\n"
     "Funde dos cosas a la vez. Si le ponés §eLimestone Flux§r, a veces da lingotes extra.",
606: "Las armas del Overworld pegan menos acá: hacé una propia del pantano. Todas son 2 del material arriba y un palo de weedwood abajo:\n"
     " · §eWeedwood Sword§r: tablones de weedwood. La primera.\n"
     " · §eBone Sword§r: §eSlimy Bones§r, que salen de la §eSlimy Bone Ore§r.\n"
     " · §eOctine Sword§r: lingotes de octine.\n"
     " · §eValonite Sword§r: valonite, de las cuevas más profundas. La mejor.",
607: "Derrotá al menos una vez a cada uno de estos monstruos del pantano:\n"
     " · §eSwamp Hag§r · §eWight§r · §eTar Beast§r · §eSludge§r · §ePeat Mummy§r\n\n"
     "La Peat Mummy sale de la turba cuando caminás cerca; la Tar Beast vive en los pozos de alquitrán.\n\n"
     "Se completa sola cuando hayas matado a los cinco.",
608: "La §eDreadful Peat Mummy§r no aparece sola: se invoca con un §eMummy Bait§r (cebo de momia).\n\n"
     "§6Mummy Bait:§r se arma en la mesa con un frasco de aspecto §eArmaniis§r, una §eShimmerstone§r, "
     "un §ecorazón animado de Tar Beast§r y una §ebola de lodo§r (de los Sludges). Mirá la receta con §eR§r en JEI.\n\n"
     "§eTirá el cebo al suelo§r (tecla §eQ§r) en un bioma §eSludge Plains§r o §eMarsh§r: la momia sale de la tierra. Tiene barra de jefe y pega fuerte: "
     "llevá armadura de syrmorite, comida y amigos.",
609: "El §eSpirit Tree§r es un árbol enorme que vive en un claro del pantano (el mapa lo nombra \"Spirit Tree\" cuando llegás). "
     "Al acercarte despierta: en el tronco aparecen §ecaras§r que te atacan.\n\n"
     "Hay que vencer a la §eCara Grande§r (Large Spirit Tree Face). Las §ecaras chicas§r la ayudan: sacalas del medio primero.\n\n"
     "§eConsejo:§r no te quedes quieto y vayan en grupo.",
610: "Las §eWight Fortresses§r son castillos grandes de piedra oscura en la superficie del pantano. "
     "Están llenas de Wights, trampas y cofres.\n\n"
     "Buscá una, hacé un waypoint en la entrada y marcá el lugar para tu grupo. "
     "Arriba de todo espera el jefe final de la dimensión.\n\n"
     "Se completa sola al encontrarla.",
611: "El jefe de la cima de la Wight Fortress. Pelea desde el centro de la sala con §etorretas§r, §ebarreras§r "
     "que lo vuelven invulnerable y §eteletransportes§r.\n\n"
     "§eCómo ganarle:§r rompé las torretas primero, esquivá los proyectiles y pegale cuando la barrera baja. "
     "Vayan en grupo, con armadura de syrmorite o mejor y mucha comida.\n\n"
     "Es uno de los tres jefes de la §eTrilogía§r del cap. 25.",

# --- Cap. 7 · Tropicraft ---
702: "Con todo listo:\n"
     " 1. Colocá la §esilla de playa§r cerca del mar.\n"
     " 2. Esperá al §eatardecer§r (cuando el sol empieza a bajar).\n"
     " 3. Sentate en la silla y tomá la §ePiña Colada§r.\n\n"
     "El efecto de la bebida te lleva a los trópicos. Se necesitan las tres cosas juntas: silla, atardecer y efecto. "
     "Si no pasa nada, revisá la hora.\n\n"
     "Para volver, más adelante hacés un portal (misión \"Varita del portal\").",
703: "Los trópicos son islas con playas, selvas y volcanes. Para explorar:\n"
     " · §eAldeas Koa§r: casas en la playa con aldeanos para comerciar.\n"
     " · §eCabezas EIH§r: estatuas de piedra gigantes.\n"
     " · §eVolcanes§r: lava y minerales adentro.\n"
     " · En el agua: tiburones martillo, tortugas y peces de colores.\n\n"
     "Conseguí §eazurita§r y §ezircón§r: son minerales de la dimensión y se minan en la piedra de las islas. "
     "Los dos sirven para la varita del portal.",

# --- Cap. 8 · Elemental Dimensions ---
801: "Los §eGuardias§r (Guards) cuidan las §emazmorras-portal§r del Overworld: construcciones de piedra con un Portal Dialer adentro. "
     "Al morir pueden soltar la §eRuna de Tierra§r.\n\n"
     "Esas mazmorras son raras. Explorá lejos, usá el mapa para no repetir zonas y hacé un waypoint cuando encuentres una: "
     "la vas a necesitar para entrar a la dimensión.",
806: "Juntá las 3 partes de la §eRuna de Aire§r y unilas en la mesa de trabajo:\n"
     " · §eParte 1:§r la sueltan los §eWater Creeps§r de la dimensión Agua.\n"
     " · §eParte 2:§r está en un cofre de la mazmorra de la dimensión Agua.\n"
     " · §eParte 3:§r la suelta el §eWater Creep Boss§r.\n\n"
     "Con la runa en la mano, usá el Portal Dialer de la mazmorra-portal del Overworld (igual que con la Runa de Tierra) "
     "y entrá al Aire (dimensión 102).",
808: "Juntá las 3 partes de la §eRuna de Espíritu§r:\n"
     " · §eParte 1:§r la sueltan los §eGhosts§r de la dimensión Aire.\n"
     " · §eParte 2:§r cofre de la mazmorra de la dimensión Aire.\n"
     " · §eParte 3:§r la suelta el §eGhost Boss§r.\n\n"
     "Unilas, usá el Portal Dialer del Overworld y entrá al Espíritu (103). "
     "Ahí los §eSpirits§r sueltan las partes 1 y 3 de la Runa de Fuego.",
809: "La última runa. Juntá las 3 partes de la §eRuna de Fuego§r:\n"
     " · §ePartes 1 y 3:§r las sueltan los §eSpirits§r de la dimensión Espíritu.\n"
     " · §eParte 2:§r cofre de la mazmorra de la dimensión Espíritu.\n\n"
     "Unilas, usá el Portal Dialer del Overworld y entrá al Fuego (104).\n\n"
     "§cCuidado:§r es una dimensión de lava. Llevá pociones de resistencia al fuego.",

# --- Cap. 10 · Cavern ---
1000: "§6Portal a la Caverna:§r armá un marco con la forma del portal del Nether (rectángulo hueco de 4 de ancho por 5 de alto como mínimo) "
      "usando §epiedra musgosa§r o §eladrillo de piedra musgoso§r. Después hacé §eclic derecho adentro del marco con una esmeralda§r.\n\n"
      "Con el mismo marco y otro objeto se abren las otras cavernas:\n"
      " · Aguamarina → Aqua Cavern · Miner's Thought Orb → Ruins Cavern\n"
      " · Un brote → Caveland · Hielo compacto → Ice Cavern · Diamante → Huge Cavern\n\n"
      "La Caverna es una dimensión toda subterránea, sin superficie. Hay §emuchos más minerales§r que en el Overworld.",
1001: "En las cavernas aparecen versiones §ecavénicas§r de los monstruos: más vida, más daño y más alcance. "
      "Matá al menos uno de cada uno:\n"
      " · Cavenic Skeleton · Cavenic Creeper · Cavenic Zombie\n"
      " · Cavenic Spider · Cavenic Witch · Cavenic Bear\n\n"
      "A veces sueltan un §eCavenic Orb§r, la llave de §eCavenia§r. Guardalo.",
1002: "La §eaguamarina§r es un mineral celeste que se mina en la Caverna. Con ella hacés pico, hacha y pala de aguamarina.\n\n"
      "Para la §eAqua Cavern§r: armá otro marco de piedra musgosa y hacé clic derecho adentro con una aguamarina. "
      "Es una caverna inundada: llevá pociones de respiración o un casco con Respiración.",
1003: "La §eRandomite Ore§r es un mineral raro de la Caverna: al romperlo §esuelta un objeto al azar§r de todo el juego. "
      "A veces es basura, a veces un tesoro.\n\n"
      "La llave de la Ruins Cavern es el §eMiner's Thought Orb§r. Sale en los §ecofres de las torres-mazmorra§r de la Caverna "
      "(1 o 2 por cofre) y, con suerte, de la randomita.\n\n"
      "Con el orbe, hacé clic derecho adentro de un marco de piedra musgosa: se abre el portal a las ruinas.",
1004: "La §eCaveland§r es una caverna con árboles y pasto, como un bosque bajo tierra.\n\n"
      "La llave es §ecualquier brote§r (de roble, abedul, de mods…). Hacé clic derecho con el brote adentro de un marco de piedra musgosa.\n\n"
      "Ahí crecen árboles \"pervertidos\" con madera propia y se cosecha la §eacresia§r con tijeras.",
1005: "La §eIce Cavern§r es una caverna helada con hielo resbaladizo.\n\n"
      "La llave es un bloque de §ehielo compacto§r (packed ice). Se consigue con un pico con §eToque de Seda§r en un bioma Ice Spikes, "
      "o comerciando con aldeanos. Hacé clic derecho con él adentro de un marco de piedra musgosa.\n\n"
      "Con el hielo de ahí se cargan herramientas y armas de hielo.",
1006: "La §eHuge Cavern§r es una caverna gigante con techos altísimos y muchos minerales.\n\n"
      "La llave es un §ediamante§r: hacé clic derecho con él adentro de un marco de piedra musgosa. "
      "Si todavía no tenés diamantes, buscalos en la Caverna: aparecen mucho más que en el Overworld.",
1007: "§eCavenia§r es una caverna de combate. Para entrar, hacé §eclic derecho con un Cavenic Orb§r estando en §ecualquier caverna§r: "
      "te lleva directo y el orbe se gasta. El orbe lo sueltan a veces (1 de cada 8) los monstruos cavénicos.\n\n"
      "En este servidor, ahí §ano perdés inventario ni experiencia§r al morir, y si reaparecés sin orbe te dan uno para salir.\n\n"
      "Los jefes de Cavenia son los §eCrazy§r (Crazy Zombie, Skeleton, Creeper y Spider): tienen barra de jefe y muchísima vida (el Crazy Zombie, §c2000§r). Vayan en grupo.",
1008: "Los §eMagical Books§r de Cavern son libros de hechizos: fuego, explosión, rayos, curación, teletransporte, invocación, vuelo y más.\n\n"
      "§eCómo se consiguen:§r los sueltan los jefes §eCrazy§r de Cavenia (Crazy Zombie, Skeleton, Creeper y Spider). "
      "Salen como libro \"???\": usalo para descubrir qué hechizo tiene.\n\n"
      "La magia gasta tus puntos de maná. Cuantos más hechizos usás, más subís de rango como mago.",

# --- Cap. 11 · Astral Sorcery ---
1100: "Los §eRock Crystals§r son la base de toda la magia de Astral Sorcery. Para encontrar el primero:\n"
      " 1. Buscá §eaguamarina§r: brilla en la §earena§r de ríos y playas, cerca de la superficie.\n"
      " 2. Buscá un §eSantuario Antiguo§r de mármol: los grandes están en la cima de colinas y montañas; los chicos, bajo la arena del desierto. "
      "Adentro flota un §eCollector Crystal§r.\n"
      " 3. Poné una §emesa de trabajo al lado del cristal§r: el cristal la ilumina y destraba la receta de la §eResonating Wand§r.\n"
      " 4. §eDe noche§r, con la varita en la mano, aparecen §echispas blancas§r en el suelo. Justo debajo, §emuy profundo§r (cerca de la bedrock), "
      "hay un Rock Crystal Ore.\n"
      " 5. Cavá recto hacia abajo y minalo con un §epico de diamante§r. Las máquinas no lo pueden minar.\n\n"
      "§eConsejo:§r el §eAstral Tome§r (el diario del mod) explica todo y se va completando a medida que avanzás.",
1101: "Las constelaciones se descubren mirando el cielo:\n"
      " 1. En los cofres de los santuarios hay §eConstellation Papers§r: cada uno muestra el dibujo de una constelación.\n"
      " 2. Fabricá el §eLooking Glass§r en la §eLuminous Crafting Table§r (se hace con mármol).\n"
      " 3. §eDe noche y con el cielo despejado§r, usá el Looking Glass. Buscá un grupo de estrellas que coincida con uno de tus papeles.\n"
      " 4. Mantené §eShift§r para fijar la vista y unilas con §eclic izquierdo§r, trazando líneas entre las estrellas.\n\n"
      "El §emármol§r aparece en vetas bajo tierra. La Luminous Crafting Table tiene que estar al aire libre: §ecuanto más alta, más luz junta§r.",
1102: "Sintonizarte con una constelación te da poderes.\n"
      " 1. Fabricá un §eAttunement Altar§r y varios §eSpectral Relays§r (recetas en el Astral Tome).\n"
      " 2. §eDe noche§r, con el Constellation Paper en la mano, se ven en el suelo los lugares donde van los relays: "
      "forman la figura de la constelación alrededor del altar.\n"
      " 3. Cuando está bien armado, el altar y los relays brillan en azul. §ePará arriba del altar§r, en el rayo de luz.\n\n"
      "Solo podés estar sintonizado con §euna constelación brillante§r. Cambiarla después borra el progreso: elegí con calma.",
1103: "La §eLuminous Crafting Table§r se mejora a §eStarlight Crafting Altar§r: guarda más luz estelar y destraba recetas nuevas.\n\n"
      " 1. Poné en la mesa la receta de mejora (está en el Astral Tome) y hacé clic derecho con la Resonating Wand.\n"
      " 2. El altar nuevo necesita una §eestructura de mármol§r alrededor para juntar luz. Si falta algo o está mal, "
      "el indicador de luz se pone §crojo§r.\n"
      " 3. Para fabricar: §ede noche§r, con el cielo a la vista, poné los materiales y hacé clic derecho con la varita.\n\n"
      "La forma exacta de la estructura se ve en el Astral Tome.",
1104: "Los Rock Crystals también se pueden sintonizar, y así canalizan el poder de una constelación.\n\n"
      "Con el §eAttunement Altar§r armado para una constelación, §ede noche§r, tirá un Rock Crystal (§eQ§r) en el rayo de luz del altar. "
      "Sale como un cristal sintonizado.\n\n"
      "Con esos cristales se hacen §erituales§r: estructuras que aplican el efecto de la constelación en una zona.",
1105: "El §eTelescope§r se fabrica en el Starlight Crafting Altar. Deja ver estrellas más lejanas que el Looking Glass.\n\n"
      " 1. Colocalo al aire libre y usalo §ede noche con el cielo despejado§r.\n"
      " 2. Con las flechas de los costados girás la vista para mirar otras partes del cielo.\n"
      " 3. Buscá una §econstelación tenue§r (más chica y oscura) y trazala con clic izquierdo, igual que con el Looking Glass.\n\n"
      "Si dibujás fuera del marco o girás, se borran las líneas. Estar sintonizado ayuda a ver las tenues.",
1106: "El §eCelestial Altar§r es el tercer nivel del altar.\n\n"
      " 1. Necesitás §eStardust§r (polvo estelar): sale de moler §eStarmetal§r en el §eGrindstone§r.\n"
      " 2. La mejora también lleva aguamarina, mármol y un Rock Crystal (receta en el Astral Tome).\n"
      " 3. La estructura de alrededor es §emás grande§r y lleva §eSooty Marble§r (mármol con carbón) a la vista del cielo.\n\n"
      "Igual que antes: de noche, con el cielo despejado y la Resonating Wand.",
1107: "El §eIridescent Altar§r es el altar más alto de Astral Sorcery. Destraba las recetas más poderosas del mod.\n\n"
      "Se fabrica en el Celestial Altar y necesita materiales de constelaciones y una estructura todavía más grande. "
      "La receta y la forma están en el §eAstral Tome§r, en la última sección que se destraba.\n\n"
      "Es una misión de largo plazo: tomátela con calma.",
1108: "Después de sintonizarte, tu cuerpo junta §eluz estelar personal§r y sube de nivel. Cada nivel da puntos para el "
      "§eárbol de perks§r (en el Astral Tome): más vida, daño, velocidad, minería, etc.\n\n"
      "La experiencia de luz estelar se gana haciendo lo que tu constelación premia (por ejemplo, pelear o minar). "
      "Llegá a §enivel 20§r.\n\n"
      "Elegí bien los perks: cambiarlos después cuesta.",

# --- Cap. 12 · Draconic Evolution ---
1201: "El §eDraconic Core§r es la pieza base de todo el mod.\n\n"
      "§6Receta:§r §e4 lingotes de draconio§r, §e4 de oro§r y un §ediamante§r al centro. Mirá la forma exacta con §eR§r en JEI.\n\n"
      "Vas a necesitar muchos: conviene juntar bastante draconio.",
1202: "El §eFusion Crafting§r es como una mesa de trabajo gigante para las recetas grandes de Draconic Evolution:\n"
      " 1. Colocá el §eFusion Crafting Core§r.\n"
      " 2. Poné los §einyectores§r alrededor, en línea con el núcleo y §emirando hacia él§r.\n"
      " 3. Poné el objeto central en el núcleo y los ingredientes en los inyectores.\n"
      " 4. Los inyectores necesitan §eenergía (RF)§r. El §eGenerator§r de Draconic Evolution quema combustible y la produce.\n\n"
      "Cuando todo está listo, abrí el núcleo y arrancá la fusión. Las recetas de JEI muestran qué va en cada lugar.",
1204: "El §eWyvern Core§r es el segundo nivel de núcleo y la base del equipo Wyvern.\n\n"
      "Se arma con §eFusion Crafting§r: lleva §eDraconic Cores§r y una §eestrella del Nether§r (la suelta el Wither). "
      "Mirá la receta completa con §eR§r en JEI.\n\n"
      "Esta misión se abre después de la §eexpedición grupal al End§r (cap. 20).",
1205: "Con Wyvern Cores y draconio se fabrica el equipo §eWyvern§r en el Fusion Crafting: pico, espada, hacha, pala, arco y armadura.\n\n"
      "Las herramientas Wyvern §eminan en área§r y se cargan con energía (RF). La armadura tiene un §eescudo de energía§r que absorbe golpes.\n\n"
      "Conseguí cualquier pieza.",
1206: "El §eChaos Guardian§r es el jefe más fuerte del servidor. Vive en las §eChaos Islands§r, islas flotantes lejos del centro del End.\n\n"
      "Lo protegen §ecristales del caos§r que lo curan y le dan escudo. En este servidor tiene §c2000 de vida§r, "
      "y su isla §cexplota§r cuando rompés el cristal del caos.\n\n"
      "Suelta §eChaos Shards§r, necesarios para el equipo más alto. Vayan en grupo, con equipo Wyvern o mejor.",
1207: "El §eAwakened Core§r es el tercer nivel de núcleo.\n\n"
      "Necesitás §edraconio despertado§r (Awakened Draconium): se hace en Fusion Crafting con draconio y el §ecorazón de dragón§r, "
      "que suelta el Ender Dragon. Después, en otra fusión, armás el núcleo con draconio despertado y fragmentos del caos.\n\n"
      "Mirá las dos recetas con §eR§r en JEI.",

# --- Cap. 13 · Harshen Universe ---
1300: "Harshen Universe agrega:\n"
      " · §eAlmas y sangre§r: se juntan de los monstruos y alimentan rituales.\n"
      " · §eAccesorios§r: anillos y pendientes con efectos (más vida, velocidad, golpes más fuertes).\n"
      " · §eEl castillo de Kazzendre§r: hay uno solo en todo el Overworld.\n"
      " · §ePontus§r: una dimensión propia (dimensión 5).\n\n"
      "Seguí estas misiones en orden: cada una te da lo que necesitás para la siguiente.",

# --- Cap. 14 · Rustic ---
1500: "§6Condenser:§r ladrillos alrededor de un balde, con arcilla endurecida blanca abajo al centro.\n\n"
      "Es el alambique de Rustic: destila §ehierbas§r para hacer §eelixires§r, que son como pociones pero más fuertes y largas.\n\n"
      "Las hierbas crecen solas en el mundo: §ealoe vera§r (desierto), §echamomile§r, §eginseng§r, §ehorsetail§r, §ecohosh§r, "
      "§ewind thistle§r, §emarsh mallow§r, §eblood orchid§r y otras. Cosechalas y replantalas en tu base.",
1501: "§6Retort:§r 2 ladrillos, 1 hierro y 1 balde.\n\n"
      "La retorta va §epegada al condensador§r y forma parte del alambique.",
1502: "Para destilar un elixir:\n"
      " 1. Abrí el condensador (con la retorta al lado).\n"
      " 2. Poné las §ehierbas§r en los espacios de ingredientes.\n"
      " 3. Poné una §ebotella de vidrio§r y §ecombustible§r (carbón o madera).\n"
      " 4. Esperá: sale el elixir.\n\n"
      "Cada combinación de hierbas da un efecto distinto: probá y mirá en JEI. Los elixires §eno§r se hacen en el soporte de pociones.",
1503: "§6Crushing Tub:§r tablones, hierro y losas (receta en JEI).\n\n"
      "Poné fruta adentro (uvas, manzanas, olivas…) con clic derecho y §esaltá encima§r para pisarla. "
      "Se llena de jugo: sacalo con una botella de vidrio o un balde.\n\n"
      "Las uvas y las olivas crecen en Rustic: las uvas en enredaderas, las olivas en árboles.",
1504: "§6Brewing Barrel:§r tablones, hierro y losas (receta en JEI).\n\n"
      "Poné jugo en el barril y esperá varios días del juego: fermenta y se vuelve §evino§r (uvas), §esidra§r (manzanas), "
      "§ehidromiel§r (miel) y otras bebidas. Las bebidas dan efectos buenos, pero tomar mucho emborracha.",
1505: "§6Apiary:§r troncos arriba y abajo, tablones a los costados.\n\n"
      "Las §eabejas§r salen de las §ecolmenas silvestres§r que cuelgan de los árboles. Poné abejas en el colmenar y dejá §eflores cerca§r: "
      "con el tiempo producen panales. De los panales salen §emiel§r y §ecera de abeja§r.\n\n"
      "La miel sirve para comida e hidromiel; la cera, para velas.",

# --- Cap. 15 · Criaturas de la noche ---
1601: "El §eScarecrow§r (espantapájaros) es un monstruo de SpookyCraft. Aparece §ede noche§r en los biomas de §ellanura§r (Plains), "
      "como cualquier otro monstruo.\n\n"
      "§eTruco:§r si de noche usás una §ecalabaza§r o una §ecabeza de mob§r en la cabeza, a veces aparecen monstruos espeluznantes a tu alrededor, "
      "entre ellos el Scarecrow y animales esqueléticos (vacas, cerdos, lobos, llamas…). Andá preparado.",
1602: "Re-Zombies agrega zombis con oficio: mineros, caballeros, piratas y más. Cada uno pelea distinto.\n\n"
      "El jefe es el §eZombie King§r: mucha más vida y armadura propia. Aparece entre los zombis.\n\n"
      "Al morir tiene §e20 % de chance§r de soltar una pieza de su armadura de rey (5 % cada una: casco, peto, pantalón o botas). "
      "Vale la pena cazarlo varias veces.",
1603: "Elemental Creepers agrega §e24 tipos de creepers§r que aparecen de noche como los normales. Cada uno explota distinto:\n"
      " · §eFire Creeper§r: deja todo en llamas.\n"
      " · §eIce Creeper§r: congela el suelo y el agua.\n"
      " · §eLightning Creeper§r (eléctrico): tira rayos.\n\n"
      "Se reconocen por el color. Derrotá a uno de cada uno de estos tres. §eConsejo:§r con arco es más seguro.",

# --- Cap. 16 · Depredadores ---
1700: "Deadly Monsters trae los monstruos más peligrosos del servidor. Salen de noche y en lugares oscuros:\n"
      " · §eWoman§r · §eWideman§r · §eClimber§r · §eMutant Steve§r · §eTopielec§r\n\n"
      "Pegan mucho más fuerte que un zombi y aguantan más golpes.\n\n"
      "Derrotá a §ecualquiera§r. Llevá como mínimo armadura de hierro y escudo.\n\n"
      "§7El Zombie Chicken de este mod no suelta nada al morir.§r",
1701: "Algunos monstruos de Deadly Monsters sueltan §etrofeos§r al morir:\n"
      " · §eWoman's Heart§r: el corazón de la Woman.\n"
      " · §eWideman's Spine§r: la columna del Wideman.\n"
      " · §eSoul Eye§r: un ojo de alma.\n\n"
      "Conseguí cualquiera de los tres. Si no te sale, seguí cazando: no siempre los sueltan.",

# --- Cap. 17 · Howling Moon ---
1800: "La §eplata§r de Howling Moon aparece como §emineral de plata§r bajo tierra."
      "Minalo con pico de hierro o mejor y fundilo en el horno.\n\n"
      "La plata es la mejor arma contra los §ehombres lobo§r: les hace mucho más daño.",
1802: "Los §ehombres lobo§r salen §ede noche§r. Son rápidos y aguantan mucho, pero la plata les hace daño extra.\n\n"
      "Llevá la §eespada de plata§r y armadura. §cOjo:§r si te muerden te pueden §einfectar§r, y con el tiempo te convertís vos también. "
      "La cura está en la misión \"La cura\".",

# --- Cap. 18 · Infernal Mobs ---
1901: "Los monstruos con modificadores tienen el §enombre de color§r arriba de la cabeza, y al lado sus poderes. "
      "Antes de pelear, leelos: algunos explotan, roban vida, te envenenan o te tiran lejos.\n\n"
      "Derrotá a uno (élite, ultra o infernal) y marcá la casilla. Los infernales sueltan buen botín: objetos encantados y más experiencia.\n\n"
      "§7Esta misión confía en tu palabra.§r",

# --- Cap. 20 · Grandes expediciones ---
2100: "Los jefes grandes se enfrentan mejor en equipo. Este capítulo junta los combates pensados para hacer en grupo.\n\n"
      "Tu progreso del libro sigue siendo §eindividual§r: cada uno completa sus misiones, aunque peleen juntos.\n\n"
      "§eConsejo:§r antes de una expedición, pónganse de acuerdo en el horario, lleven comida, pociones y armadura de repuesto.",
2101: "§6Invocar al Wither:§r 4 bloques de §earena de almas§r en forma de T y 3 §ecalaveras de Wither Skeleton§r arriba. "
      "Las calaveras las sueltan, a veces, los esqueletos negros de las §efortalezas del Nether§r.\n\n"
      "§cHacelo lejos de las bases:§r al aparecer explota y rompe bloques. Conviene pelearlo bajo tierra o en el Nether.\n\n"
      "Suelta la §eestrella del Nether§r: la pide la semilla del Fire Boss.",
2103: "Los §emonumentos oceánicos§r son templos bajo el mar en los océanos profundos. Adentro hay §e3 Elder Guardians§r.\n\n"
      "Te dan §efatiga de minería§r (no podés romper bloques rápido) y disparan láseres. "
      "Llevá §epociones de respiración§r, un casco con Respiración y botas con Agilidad Acuática.\n\n"
      "Derrotá a uno. Sueltan una §eesponja mojada§r y prismarina.",

# --- Cap. 21 · Draconic Evolution final ---
2200: "El equipo §eDraconic§r es el nivel más alto: más área de minado, más escudo y más daño que el Wyvern.\n\n"
      "Se fabrica con §eFusion Crafting§r usando §eAwakened Cores§r, §edraconio despertado§r y la pieza Wyvern equivalente. "
      "Mirá cada receta con §eR§r en JEI.\n\n"
      "Conseguí cualquier pieza.",
2201: "El §eChaotic Core§r es el núcleo más poderoso de Draconic Evolution.\n\n"
      "Se arma con §eFusion Crafting§r usando §eAwakened Cores§r y §eChaos Shards§r (los suelta el Chaos Guardian). "
      "Mirá la receta con §eR§r en JEI.",
2202: "El §eEnergy Storage Core§r es una batería gigante de Draconic Evolution. Tiene varios niveles: cada uno guarda muchísimo más.\n\n"
      "Es una estructura: el núcleo al centro, §eestabilizadores§r alrededor y bloques de draconio o redstone según el nivel. "
      "Para sacar y meter energía se usan los §eEnergy Pylons§r.\n\n"
      "La forma de cada nivel la muestra el núcleo en su propio menú.",

# --- Cap. 22 · Maestro de las dimensiones ---
2301: "Entrá a las 7 dimensiones de Cavern. Cada una tiene su llave (clic derecho adentro de un marco de piedra musgosa):\n"
      " · §eCavern§r: esmeralda · §eAqua Cavern§r: aguamarina\n"
      " · §eRuins Cavern§r: Miner's Thought Orb · §eCaveland§r: un brote\n"
      " · §eIce Cavern§r: hielo compacto · §eHuge Cavern§r: diamante\n"
      " · §eCavenia§r: clic derecho con un Cavenic Orb estando en cualquier caverna",

# --- Cap. 23 · Coleccionista ---
2400: "La Betweenlands tiene §e4 anillos mágicos§r . Se encuentran como botín explorando el pantano:\n"
      " · §eRing of Power§r · §eRing of Ascent§r\n"
      " · §eRing of Recruitment§r · §eRing of Summoning§r\n\n"
      "Pasá el mouse por encima de cada uno para ver qué hace. Conseguí los cuatro.",
2401: "Juntá los hongos de la Betweenlands:\n"
      " · §eBlack Hat Mushroom§r · §eBulb-Capped Mushroom§r\n"
      " · §eFlat Head Mushroom§r · §eYellow Dotted Fungus§r\n\n"
      "Crecen en zonas oscuras y húmedas del pantano. Hacé un waypoint donde encuentres cada uno.",
2402: "El §eHerblore Book§r es el libro de herboristería de la Betweenlands. Se completa §edescubriendo los aspectos§r de cada planta:\n"
      " 1. Cosechá plantas del pantano con la §eSickle§r (hoz).\n"
      " 2. Probalas en un §eGecko enjaulado§r para descubrir qué aspectos tienen.\n"
      " 3. Cada descubrimiento se anota en el libro.\n\n"
      "Con los aspectos se hacen elixires e infusiones. Es una misión larga: completá el libro entero.",
2403: "Las §eherramientas compuestas§r son pico, hacha y pala que mezclan varios materiales. Se hacen con el hechizo de "
      "§eCompositing§r de un Magical Book de Cavern.\n\n"
      "Conseguí un libro con ese hechizo (lo sueltan los jefes Crazy de Cavenia), juntá los materiales y lanzalo. "
      "Fabricá cualquiera de las tres.",

# --- Cap. 24 · Arquitecto del mundo ---
2501: "En MineColonies los §eciudadanos§r hacen el trabajo, pero alguien tiene que construir las casas: el §eBuilder§r.\n\n"
      " 1. Colocá la §echoza del Builder§r (Builder's Hut) cerca del Town Hall.\n"
      " 2. Abrila y pedí que se construya: se le asigna un ciudadano.\n"
      " 3. El constructor te pide §emateriales§r: ponelos en el cofre de su choza.\n\n"
      "Después, cada edificio nuevo se coloca con su bloque y el Builder lo levanta solo.",

# --- Cap. 25 · Desafíos legendarios ---
2600: "Los tres jefes finales del servidor:\n"
      " · §ePrimordial Malevolence§r: la cima de la Wight Fortress (Betweenlands, cap. 6).\n"
      " · §eFire Boss§r: la dimensión Fuego (Elemental Dimensions, cap. 8).\n"
      " · §eChaos Guardian§r: las Chaos Islands del End (Draconic Evolution, cap. 12).\n\n"
      "Derrotá a los tres. Cada uno se completa por separado, en el orden que quieras.",
2601: "Derrotá al §eWither 3 veces§r.\n\n"
      "Cada invocación lleva 4 de arena de almas y 3 calaveras de Wither Skeleton. "
      "Con un grupo y buen equipo, una arena preparada bajo tierra lo hace mucho más fácil.\n\n"
      "Las estrellas del Nether sobrantes sirven para Draconic Evolution y para un §efaro§r.",
2700: "Recorriste todas las dimensiones y venciste a los jefes finales.\n\n"
      "Tu nombre queda en la historia del servidor: esta misión te da el título §6Leyenda de ArreMods§r.\n\n"
      "Gracias por jugar.",

# --- Cap. 8 · Elemental Dimensions: cómo aparece cada jefe (código del mod) ---
800: "El §eElemental Dust Ore§r es un mineral del Overworld que suelta §epolvo elemental§r. Juntá 8.\n\n"
     "§6Altar Center:§r una esmeralda arriba al medio, polvo elemental a los costados de un §ebloque de oro§r y una fila de polvo abajo. "
     "Es la pieza central de los altares del mod.\n\n"
     "Este capítulo se juega en orden: Tierra → Agua → Aire → Espíritu → Fuego. Cada dimensión te da lo que necesitás para la siguiente.",
803: "El §eDirt Zombie Boss§r aparece solo en la §edimensión Tierra§r, §ecerca de la medianoche§r, al lado de los jugadores, "
     "si no hay otro vivo. Esperalo de noche con equipo listo.\n\n"
     "Suelta la §eparte 3 de la Runa de Agua§r y el §eDigging Focus§r. Los Dirt Zombies comunes sueltan la parte 1.",
805: "El §eWater Creep Boss§r se invoca con una §eWater Boss Seed§r: 4 semillas de trigo alrededor de un §ediamante§r.\n\n"
     "Andá a la §edimensión Agua§r y §etirá la semilla al agua§r (tecla §eQ§r). Unos segundos después, el jefe sale arriba.\n\n"
     "Suelta la §eparte 3 de la Runa de Aire§r y el §eDamage Focus§r. Los Water Creeps comunes sueltan la parte 1.",
807: "El §eGhost Boss§r se invoca con una §eAir Boss Seed§r: 4 semillas de trigo alrededor de una §eesmeralda§r.\n\n"
     "En la §edimensión Aire§r, §etirá la semilla al suelo§r (tecla §eQ§r). Hay una §cexplosión§r y aparece el jefe: alejate un poco.\n\n"
     "Suelta la §eparte 3 de la Runa de Espíritu§r y el §eTeleport Focus§r. Los Ghosts comunes sueltan la parte 1.",
810: "El último jefe del capítulo. Se invoca con una §eFire Boss Seed§r: 4 semillas de trigo alrededor de una §eestrella del Nether§r "
     "(la suelta el Wither, cap. 20).\n\n"
     "En la §edimensión Fuego§r, §etirá la semilla al suelo§r (tecla §eQ§r) y alejate: hay una explosión antes de que aparezca.\n\n"
     "Suelta la §eElemental Wand§r. §7No tiene barra de jefe: fijate su vida con Hwyla.§r\n\n"
     "Es uno de los tres jefes de la §eTrilogía§r del cap. 25.",
1801: "§6Silver Sword:§r 2 lingotes de plata y un palo, en vertical (como una espada común).\n\n"
      "Les hace §edaño extra a los hombres lobo§r. Con una espada común también se puede, pero tarda mucho más.",
2300: "Visitá §e12 dimensiones§r. Cada tarea se completa sola al llegar:\n"
      " · §eNether§r (portal de obsidiana) · §eEnd§r (expedición grupal, cap. 20)\n"
      " · §eBetweenlands§r (cap. 6) · §eTrópicos§r (cap. 7)\n"
      " · §eTierra, Agua, Aire, Espíritu y Fuego§r (cap. 8)\n"
      " · §eHunting Dimension§r (cap. 9) · §eCavern§r (cap. 10) · §ePontus§r (cap. 13)\n\n"
      "Cada capítulo explica cómo llegar a su dimensión.",
}

ICONOS = {
    1100: ("astralsorcery:itemrockcrystalsimple", 0),
    1101: ("astralsorcery:itemhandtelescope", 0),
    1102: ("astralsorcery:blockattunementaltar", 0),
    1103: ("astralsorcery:blockaltar", 1),
    1104: ("astralsorcery:blockattunementrelay", 0),
    1105: ("astralsorcery:blockmachine", 0),
    1106: ("astralsorcery:blockaltar", 2),
    1107: ("astralsorcery:blockaltar", 3),
    1108: ("astralsorcery:itemjournal", 0),
}


def build():
    qdb = {}
    for n, (qid, line, x, y, q) in enumerate(QUESTS):
        desc = TEXTOS.get(qid, q["desc"])
        icon = item(ICONOS[qid][0], 1, ICONOS[qid][1]) if qid in ICONOS else q["icon"]
        props = {"name:8": q["name"], "desc:8": desc, "icon:10": icon,
                 "isMain:1": 1 if q["main"] else 0, "taskLogic:8": q["task_logic"], "questLogic:8": "AND",
                 "visibility:8": "NORMAL", "repeatTime:3": -1, "autoClaim:1": 0, "isSilent:1": 0,
                 "lockedProgress:1": 0, "simultaneous:1": 0, "globalShare:1": 0, "isGlobal:1": 0}
        tasks = {"%d:10" % i: dict({"index:3": i}, **t) for i, t in enumerate(q["tasks"])}
        rewards = {"%d:10" % i: dict({"index:3": i}, **r) for i, r in enumerate(q["rewards"])}
        qdb["%d:10" % n] = {"questID:3": qid, "preRequisites:11": q["prereq"],
                            "properties:10": {"betterquesting:10": props}, "tasks:9": tasks, "rewards:9": rewards}
    qlines = {}
    for li, (name, desc, icon) in enumerate(LINES):
        entries = {}
        for k, (qid, line, x, y, q) in enumerate([e for e in QUESTS if e[1] == li]):
            entries["%d:10" % k] = {"id:3": qid, "x:3": x, "y:3": y, "sizeX:3": 24, "sizeY:3": 24}
        qlines["%d:10" % li] = {"lineID:3": li, "order:3": li,
                                "properties:10": {"betterquesting:10": {"name:8": name, "desc:8": desc, "icon:10": icon,
                                                                         "visibility:8": "NORMAL", "bg_image:8": "", "bg_size:3": 256}},
                                "quests:9": entries}
    return {"build:8": "3.5.329", "format:8": "2.0.0", "questDatabase:9": qdb, "questLines:9": qlines,
            "questSettings:10": {"betterquesting:10": {
                "livesdef:3": 3, "pack_name:8": "ArreMods", "home_anchor_y:5": 0.0, "livesmax:3": 10,
                "home_anchor_x:5": 0.5, "editmode:1": 0, "hardcore:1": 0,
                "home_image:8": "arremods:textures/gui/portada.png", "party_enable:1": 0,
                "pack_version:3": 2, "home_offset_x:3": -128, "home_offset_y:3": 0}}}

if __name__ == "__main__":
    ids = [q[0] for q in QUESTS]
    assert len(ids) == len(set(ids)), "IDs repetidos"
    for q in QUESTS:
        for p in q[4]["prereq"]:
            assert p in ids, "prerrequisito inexistente %s en %s" % (p, q[0])
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=2)
    print("misiones:", len(QUESTS), "capitulos:", len(LINES))
