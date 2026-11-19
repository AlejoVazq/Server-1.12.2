# -*- coding: utf-8 -*-
"""
Generador del libro de misiones de Planeta Vegetta VII (Bloque I, capitulos 1 a 5).
Formato: Better Questing 3.5.329 + Standard Expansion 3.4.173 (formato de base de datos "2.0.0").
Uso:  python -I generar_misiones.py <archivo_salida.json>
Fuente del contenido: pv7-docs/03_capitulos_1_a_5.md y 05_recetas_verificadas.md
"""
import json, sys

WILD = 32767  # comodin de variante (cualquier color/madera)

def item(iid, count=1, dmg=0, ore="", tag=None):
    d = {"id:8": iid, "Count:3": count, "Damage:2": dmg, "OreDict:8": ore}
    if tag is not None:
        d["tag:10"] = tag
    return d

def lst(elems):
    """Las listas NBT se guardan como objeto {"0:10": ..., "1:10": ...}."""
    return {"%d:10" % i: e for i, e in enumerate(elems)}

# ---- tareas -----------------------------------------------------------------
def t_checkbox():
    return {"taskID:8": "bq_standard:checkbox"}

def t_retrieval(items, consume=False, ignore_nbt=True):
    return {"taskID:8": "bq_standard:retrieval", "partialMatch:1": 1, "ignoreNBT:1": 1 if ignore_nbt else 0,
            "consume:1": 1 if consume else 0, "groupDetect:1": 0, "autoConsume:1": 0,
            "requiredItems:9": lst(items)}

def t_crafting(items, ignore_nbt=True):
    return {"taskID:8": "bq_standard:crafting", "partialMatch:1": 1, "ignoreNBT:1": 1 if ignore_nbt else 0,
            "allowCraft:1": 1, "allowSmelt:1": 1, "allowAnvil:1": 0,
            "requiredItems:9": lst(items)}

# ---- recompensas ------------------------------------------------------------
def r_xp(levels):
    return {"rewardID:8": "bq_standard:xp", "amount:3": levels, "isLevels:1": 1}

def r_items(items):
    return {"rewardID:8": "bq_standard:item", "rewards:9": lst(items)}

# ---- misiones ---------------------------------------------------------------
QUESTS = []   # (qid, linea, x, y, datos)

def quest(qid, line, x, y, name, desc, icon, tasks, rewards=(), prereq=(), task_logic="AND", main=False):
    QUESTS.append((qid, line, x, y, dict(name=name, desc=desc, icon=icon, tasks=list(tasks),
                   rewards=list(rewards), prereq=list(prereq), task_logic=task_logic, main=main)))

def any_of(items, kind):
    """Una tarea por item + logica OR: se completa con cualquiera."""
    f = t_crafting if kind == "craft" else t_retrieval
    return [f([i]) for i in items]

V = "\n\n§7Verificado en los archivos del servidor (2026-11-19).§r"

# ============================ CAPITULO 1 =====================================
quest(0, 0, 0, 0, "Tu libro de aventuras",
      "Este libro es tu guía. Cada capítulo explica un rincón del mundo y un mod.\n\n"
      "No hay un orden obligatorio: elegí por dónde seguir. Tu progreso es solo tuyo; nadie más puede completar misiones por vos.\n\n"
      "§eCómo se usa:§r abrí una misión, leé, hacé lo que pide y tocá el botón para entregar o marcá la casilla. "
      "Si tiene premio, tocá §a\"Claim\"§r para recibirlo.\n\n"
      "Si perdés el libro, se fabrica con §ebook + stick§r (libro + palo).",
      item("questbook:itemquestbook"), [t_checkbox()], [r_xp(1)], main=True)
quest(1, 0, 48, -36, "Reglas del servidor",
      "§c[Texto pendiente: lo define el administrador]§r\n\n"
      "Acá van las reglas de convivencia: griefing, reclamo de chunks, PvP y qué se puede hacer en bases ajenas.",
      item("minecraft:writable_book"), [t_checkbox()], [], prereq=[0])
quest(2, 0, 48, 0, "Este mundo no es vanilla",
      "Planeta Vegetta cambia las reglas con el modo difícil de §6Better With Mods§r.\n\n"
      "Ya §cno se fabrican en la mesa§r: herramientas y armaduras de diamante, tintes de flores, azúcar, polvo de blaze, "
      "piedra y ladrillo musgosos. Los tintes, el azúcar y el polvo de blaze ahora salen del §eMolino§r de Better With Mods.\n\n"
      "Tampoco se hace carbón vegetal en el horno: se hace en el horno de ladrillo de BWM (Kiln).\n\n"
      "§eConsejo:§r no memorices recetas de otras guías. Si una receta no aparece, mirala en JEI." + V,
      item("betterwithmods:material", dmg=0), [t_checkbox()], [], prereq=[0])
quest(3, 0, 48, 36, "Tu primera consulta de recetas",
      "Abrí el inventario, pasá el cursor sobre un ítem y presioná:\n"
      "§eR§r = cómo se fabrica\n§eU§r = para qué sirve\n\n"
      "(Son los atajos normales de JEI; si no te funcionan, revisá Controles.)\n\n"
      "Si instalaste §7Just Enough Resources§r y §7JEI Integration§r en tu cliente, también vas a ver dónde aparecen minerales y qué sueltan los monstruos.",
      item("minecraft:crafting_table"), [t_checkbox()], [], prereq=[0])
quest(4, 0, 96, 0, "Ojo con lo que mirás (Hwyla)",
      "Mirá un bloque o una criatura: arriba de la pantalla, Hwyla te dice qué es y de qué mod viene.\n\n"
      "§7Aviso: con Storage Drawers el panel no muestra el contenido de los cajones (falla conocida del plugin).§r",
      item("minecraft:spider_eye"), [t_checkbox()], [], prereq=[3])
quest(5, 0, 96, 36, "Tu primer mapa",
      "Abrí JourneyMap (tecla §eJ§r), creá un waypoint en tu punto de partida (tecla §eB§r) y ponele nombre. "
      "Así siempre sabés volver.\n\n"
      "§7Todos deben usar JourneyMap 5.5.3, la misma versión que el servidor.§r",
      item("minecraft:map"), [t_checkbox()], [r_xp(2)], prereq=[0])

# ============================ CAPITULO 2 =====================================
quest(10, 1, 0, 0, "Manos a la obra",
      "Todo aventurero empieza con madera. Juntá §e16 troncos§r (de cualquier árbol).\n\n"
      "§eConsejo:§r las antorchas necesitan carbón. En este servidor el carbón vegetal §cno§r sale del horno: buscá carbón mineral.",
      item("minecraft:log"), [t_retrieval([item("minecraft:log", 16, WILD, "logWood")])],
      [r_items([item("minecraft:torch", 8)])], prereq=[0], main=True)
quest(11, 1, 48, -36, "Un techo sobre tu cabeza",
      "Construí un refugio simple: cuatro paredes, techo, una puerta y luz adentro.\n\n"
      "Iluminá bien el interior para que no aparezcan monstruos.\n\n"
      "§7MalisisDoors y FenceOverhaul pueden cambiar el aspecto de puertas y cercas.§r",
      item("minecraft:wooden_door"), [t_checkbox()], [], prereq=[10])
quest(12, 1, 48, 0, "Hogar portátil (Camping Mod)",
      "Una §etienda§r o un §esaco de dormir§r te dan dónde descansar en cualquier lado. Fabricá cualquiera de los dos.\n\n"
      "§6Primero, la Navaja suiza:§r 6 tintes rojos + 3 lingotes de hierro (tinte, hierro, tinte en cada fila). "
      "El tinte rojo sale del Molino de BWM.\n\n"
      "§6Saco de dormir:§r navaja arriba + 3 lanas abajo.\n"
      "§6Tienda:§r 5 lonas + 2 estacas.\n"
      " · Lona = cáñamo + navaja (el cáñamo crece en el mundo)\n"
      " · Estaca = palo de hierro + navaja\n"
      " · Palo de hierro = 2 lingotes de hierro en vertical" + V,
      item("camping:sleeping_bag"),
      any_of([item("camping:tent", 1, WILD), item("camping:sleeping_bag", 1, WILD)], "craft"),
      [r_xp(3)], prereq=[10], task_logic="OR")
quest(13, 1, 96, 0, "La fogata",
      "Cociná y calentate junto al fuego. Fabricá una fogata:\n\n"
      "§6Camp Fire:§r 1 tronco arriba, 3 troncos en el medio, 3 palos abajo.\n"
      "§7Se apaga sola después de unos 6 minutos.§r\n\n"
      "También valen las fogatas del Camping Mod (5 palos, o 4 de piedra labrada para la de cocinar)." + V,
      item("campfire:campfire"),
      any_of([item("campfire:campfire"), item("camping:campfire_wood_off"), item("camping:campfire_cook")], "craft"),
      [r_xp(2)], prereq=[10], task_logic="OR")
quest(14, 1, 48, 36, "Dormir con cuidado (Nightmares)",
      "Cada vez que dormís hay un §c5 %§r de probabilidad de que te reciba una pesadilla.\n\n"
      "No es un castigo, es un desafío: dormí con el equipo puesto y la vida llena." + V,
      item("minecraft:bed", dmg=14), [t_checkbox()], [], prereq=[10])
quest(15, 1, 96, 36, "Si morís (Tombstone)",
      "Cuando caés, tu equipo queda guardado en una §etumba§r. Volvé a buscarlo.\n\n"
      "§cOjo:§r en la §eHunting Dimension§r no podés reaparecer ahí. "
      "En §eCavenia§r (Cavern) no perdés ni el inventario ni la experiencia." + V,
      item("minecraft:skull", dmg=0), [t_checkbox()], [], prereq=[14])
quest(16, 1, 144, 0, "Primera comida decente",
      "Un aventurero con hambre no llega lejos. Conseguí §ecualquier comida cocinada§r: carne de vaca, cerdo, pollo, cordero, "
      "conejo, pescado, papa asada, pan o venado cocido del Camping Mod.\n\n"
      "§7La comida cruda no te envenena en este servidor.§r",
      item("minecraft:cooked_beef"),
      any_of([item("minecraft:cooked_beef"), item("minecraft:cooked_porkchop"), item("minecraft:cooked_chicken"),
              item("minecraft:cooked_mutton"), item("minecraft:cooked_rabbit"), item("minecraft:cooked_fish", 1, WILD),
              item("minecraft:baked_potato"), item("minecraft:bread"), item("camping:venison_cooked")], "retrieval"),
      [r_xp(2)], prereq=[13], task_logic="OR")

# ============================ CAPITULO 3 =====================================
quest(20, 2, 0, 0, "Lo que cambió en armas y armaduras",
      "El diamante ya no se trabaja como antes: las herramientas y armaduras de diamante vanilla §cno§r tienen receta.\n\n"
      "Las de §emods§r (martillos, escudos) sí siguen usando diamante.\n\n"
      "Para ver la ruta de herramientas del servidor, leé el manual de Better With Mods o usá JEI." + V,
      item("minecraft:iron_sword"), [t_checkbox()], [], prereq=[0], main=True)
quest(21, 2, 48, -36, "Un escudo de verdad (Spartan Shields)",
      "Los escudos tienen niveles según el material y permiten golpear con ellos.\n\n"
      "§6Escudo de madera:§r 6 tablones + 1 palo (en diagonal).\n"
      "§6Los demás:§r el escudo de madera en el centro + 4 del material alrededor (piedra labrada, hierro, oro, obsidiana o diamante)." + V,
      item("spartanshields:shield_basic_wood"),
      [t_crafting([item("spartanshields:shield_basic_wood")])], [r_xp(3)], prereq=[20])
quest(22, 2, 96, -36, "Arco de varias flechas (Switch-Bow) §7[avanzado]",
      "Un arco, un carcaj y varios tipos de flecha: cambiás de munición sin guardar nada.\n\n"
      "§6Switch-Bow:§r 3 palos + 1 ojo de ender + 3 hilos.\n"
      "§6Carcaj:§r cuero, hilo y un cofre (miralo en JEI).\n\n"
      "§cOjo:§r el ojo de ender necesita polvo de blaze (Molino de BWM + varas del Nether). "
      "Esta misión es para más adelante; §ano bloquea nada§r." + V,
      item("switchbow:switchbow"), [t_crafting([item("switchbow:switchbow")])], [r_xp(5)], prereq=[20])
quest(23, 2, 48, 0, "Minería en grande (Hammer Time)",
      "Un martillo rompe un área de 3×3 de una vez. Fabricá uno de cualquier material.\n\n"
      "§6Receta:§r 5 del material arriba y a los costados + 2 palos en el centro.\n"
      " · Madera = §etroncos§r (no tablones)\n · Piedra = §epiedra lisa§r (no labrada)\n\n"
      "§7Gasta durabilidad más rápido que un pico, pero en este servidor tiene un multiplicador de durabilidad.§r" + V,
      item("hammertime:itemhammerstone"),
      any_of([item("hammertime:itemhammerwood"), item("hammertime:itemhammerstone"), item("hammertime:itemhammeriron"),
              item("hammertime:itemhammergold"), item("hammertime:itemhammerdiamond")], "craft"),
      [r_xp(3)], prereq=[20], task_logic="OR")
quest(24, 2, 96, 0, "Quitar para poner (Disenchanter)",
      "La §eDisenchantment Table§r saca encantamientos de un objeto y los guarda en un libro.\n\n"
      "§6Receta:§r fila del medio: tinte amarillo, esmeralda, tinte amarillo. Fila de abajo: esmeralda, mesa de encantamientos, esmeralda.\n\n"
      "§cOjo:§r el encantamiento funciona distinto con Better With Mods. Probalo antes de gastar algo valioso." + V,
      item("disenchanter:disenchantmenttable"), [t_checkbox()], [], prereq=[23])
quest(25, 2, 48, 36, "Guardar lo importante",
      "Un buen aventurero lleva espacio de sobra. En el §ecapítulo 5§r aprendés a ampliar el tuyo con mochilas y cajones.",
      item("minecraft:chest"), [t_checkbox()], [], prereq=[20])

# ============================ CAPITULO 4 =====================================
quest(30, 3, 0, 0, "Brújula de biomas (Nature's Compass)",
      "La Nature's Compass te dice dónde está el bioma que le pidas, con distancia y coordenadas.\n\n"
      "§6Receta:§r 4 brotes en las esquinas, 4 troncos a los lados y una brújula en el centro.\n\n"
      "§eConsejo:§r usala antes de salir a buscar biomas de otros mods." + V,
      item("naturescompass:naturescompass"), [t_crafting([item("naturescompass:naturescompass")])],
      [r_xp(3)], prereq=[0], main=True)
quest(31, 3, 48, -36, "Encontrá un bioma que no conozcas",
      "Pedile a la brújula un bioma que nunca hayas visto y caminá hasta él. Marcalo en JourneyMap con un waypoint.\n\n"
      "Ideas: Savanna, Mesa, Mega Taiga, Ice Spikes.\n\n"
      "§7Los biomas de Tropicraft y Betweenlands están en sus propias dimensiones.§r",
      item("minecraft:grass"), [t_checkbox()], [r_xp(2)], prereq=[30])
quest(32, 3, 48, 0, "Cruzar el barranco (Rope Bridge)",
      "El §eBridge Builder§r tira un puente de cuerda de un lado al otro.\n\n"
      "§6Se arma con 3 piezas en fila:§r gancho (5 hierro) + cañón (6 hierro + 3 cuerdas) + mango (hierro, mechero, cuerda, pólvora, tablones).\n"
      "§6Cuerda:§r 3 hilos + 3 enredaderas = 8 cuerdas.\n\n"
      "Cada bloque de puente gasta 2 cuerdas, 2 hilos, 1 madera y 1 losa. Necesitás unos 13 lingotes de hierro en total." + V,
      item("ropebridge:bridge_builder"), [t_checkbox()], [], prereq=[30])
quest(33, 3, 96, 0, "Teletoro",
      "Teletoro agrega portales y perlas de teletransporte.\n\n"
      "§6Teletory Portal Linker:§r 2 Teletory Pearls + 1 Ender Block (4 perlas de ender).\n\n"
      "§c[En prueba]§r todavía no se comprobó de dónde salen las Teletory Pearls ni qué permite el portal.",
      item("teletoro:teletory_portal_linker"), [t_checkbox()], [], prereq=[30])
quest(34, 3, 48, 36, "El mapa de tu primera semana",
      "Explorá en espiral alrededor de tu base sin alejarte demasiado. Marcá cuevas, aldeas y estructuras en JourneyMap.\n\n"
      "§7En este servidor las aldeas no generan golems de hierro.§r",
      item("minecraft:filled_map"), [t_checkbox()], [r_xp(2)], prereq=[30])

# ============================ CAPITULO 5 =====================================
quest(40, 4, 0, 0, "Reclamá tu terreno (FTBUtilities)",
      "Con FTBUtilities podés reclamar chunks para que nadie toque tu base.\n\n"
      "Abrí el mapa de reclamos (desde el inventario, botón de FTB) y reclamá al menos un chunk.\n\n"
      "§7Los límites por jugador los fija el administrador.§r",
      item("minecraft:iron_door"), [t_checkbox()], [], prereq=[0], main=True)
quest(41, 4, 48, -36, "Un lugar al que volver",
      "Usá §e/sethome§r para guardar tu base y §e/home§r para volver.\n\n§7(Comando en prueba.)§r",
      item("minecraft:compass"), [t_checkbox()], [], prereq=[40])
quest(42, 4, 48, 0, "Tu primera mochila",
      "Las mochilas amplían tu inventario. Fabricá §ecualquiera§r:\n\n"
      "§6Backpacks:§r bolsillo = 5 cuero + 3 hilo; mochila = 7 cuero + 1 placa de presión de oro.\n"
      "§6Iron Backpacks:§r 4 lanas + 4 cueros + 1 cofre en el centro.\n"
      "§6Camping Mod:§r bolsa = 1 hilo + 5 cueros." + V,
      item("backpacks16840:backpack", dmg=3),
      any_of([item("backpacks16840:backpack", 1, WILD), item("backpacks16840:backpack_pouch", 1, WILD),
              item("ironbackpacks:backpack", 1, WILD), item("camping:bag", 1, WILD)], "craft"),
      [r_xp(3)], prereq=[40], task_logic="OR")
quest(43, 4, 96, 0, "Cajones inteligentes (Storage Drawers)",
      "Un cajón guarda un solo tipo de ítem en grandes cantidades.\n\n"
      "§6Cajón 1×1:§r 3 tablones arriba, un cofre en el centro, 3 tablones abajo.\n"
      "§6Controlador:§r piedra lisa, 2 comparadores, 1 cajón y 1 diamante. Con él, todos los cajones conectados funcionan como uno." + V,
      item("storagedrawers:basicdrawers"), [t_crafting([item("storagedrawers:basicdrawers", 1, WILD)])],
      [r_xp(3)], prereq=[40])
quest(44, 4, 48, 36, "Mover cofres enteros (Chest Transporter)",
      "Levantá un cofre lleno y llevalo a otro lado.\n\n"
      "§6Transportador de madera:§r 6 palos. Las versiones de hierro, oro, diamante y obsidiana cambian el palo del centro por el material.\n\n"
      "§cOjo:§r mientras cargás un cofre te da hambre y te volvés más lento." + V,
      item("chesttransporter:chesttransporter"), [t_checkbox()], [], prereq=[40])
quest(45, 4, 96, 36, "Tu primer cultivo",
      "Sembrá y cosechá algo propio: trigo, zanahoria, papa, remolacha o los cultivos de §eRustic§r (tomate o chile).\n\n"
      "Rustic es la puerta a la alquimia (capítulo 15).\n\n"
      "§7Los árboles plantados tienen etapas extra de crecimiento.§r",
      item("rustic:tomato"),
      any_of([item("minecraft:wheat"), item("minecraft:carrot"), item("minecraft:potato"), item("minecraft:beetroot"),
              item("rustic:tomato"), item("rustic:chili_pepper")], "retrieval"),
      [r_xp(2)], prereq=[40], task_logic="OR")
quest(46, 4, 144, 36, "Agua que trabaja (Water Strainer)",
      "Un filtro en el agua junta recursos con el tiempo.\n\n"
      "§6Base:§r 2 barrotes de hierro arriba, tablones, una tolva y un cofre.\n"
      "§6Filtro:§r 8 palos alrededor de una red (hecha con hilo).\n\n"
      "Da palos, arcilla y piedra; el filtro denso da arena, tierra, grava y a veces pepitas de oro." + V,
      item("waterstrainer:strainer_base"), [t_checkbox()], [], prereq=[45])
quest(47, 4, 144, 0, "Elegí tu próxima rama",
      "Ya sabés lo básico: tenés base, almacén y territorio. Ahora el mundo es tuyo: dimensiones, magia, tecnología. Elegí.\n\n"
      "§7Se desbloquea al terminar: reclamar terreno, tu primera mochila y tus primeros cajones.§r",
      item("minecraft:nether_star"), [t_checkbox()],
      [r_xp(5), r_items([item("minecraft:paper", 1, 0, "", {
          "display:10": {"Name:8": "§6Aventurero de Planeta Vegetta",
                         "Lore:9": {"0:8": "Completaste el Bloque I", "1:8": "de la guía de aventuras."}}})])],
      prereq=[40, 42, 43], main=True)

LINES = [
    ("Cap. 1 · Bienvenido a Planeta Vegetta", "Cómo usar el libro, las reglas y qué cambia en este mundo.", item("questbook:itemquestbook")),
    ("Cap. 2 · Los primeros días", "Refugio, fuego, cama, comida y qué hacer si algo sale mal.", item("campfire:campfire")),
    ("Cap. 3 · Preparación del aventurero", "Equipo para salir al mundo: escudos, arcos y martillos.", item("spartanshields:shield_basic_wood")),
    ("Cap. 4 · Explorador", "Orientarte, buscar biomas y marcar el mundo.", item("naturescompass:naturescompass")),
    ("Cap. 5 · Tu primer asentamiento", "Base, almacén y territorio propio.", item("storagedrawers:basicdrawers")),
]

def build():
    qdb = {}
    for n, (qid, line, x, y, q) in enumerate(QUESTS):
        props = {"name:8": q["name"], "desc:8": q["desc"], "icon:10": q["icon"],
                 "isMain:1": 1 if q["main"] else 0, "taskLogic:8": q["task_logic"], "questLogic:8": "AND",
                 "visibility:8": "NORMAL", "repeatTime:3": -1, "autoClaim:1": 0, "isSilent:1": 0,
                 "lockedProgress:1": 0, "simultaneous:1": 0, "globalShare:1": 0, "isGlobal:1": 0}
        tasks = {}
        for i, t in enumerate(q["tasks"]):
            tasks["%d:10" % i] = dict({"index:3": i}, **t)
        rewards = {}
        for i, r in enumerate(q["rewards"]):
            rewards["%d:10" % i] = dict({"index:3": i}, **r)
        qdb["%d:10" % n] = {"questID:3": qid, "preRequisites:11": q["prereq"],
                            "properties:10": {"betterquesting:10": props},
                            "tasks:9": tasks, "rewards:9": rewards}
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
                "livesdef:3": 3, "pack_name:8": "Planeta Vegetta VII", "home_anchor_y:5": 0.0, "livesmax:3": 10,
                "home_anchor_x:5": 0.5, "editmode:1": 0, "hardcore:1": 0,
                "home_image:8": "betterquesting:textures/gui/default_title.png", "party_enable:1": 0,
                "pack_version:3": 1, "home_offset_x:3": -128, "home_offset_y:3": 0}}}

if __name__ == "__main__":
    ids = [q[0] for q in QUESTS]
    assert len(ids) == len(set(ids)), "IDs repetidos"
    for q in QUESTS:
        for p in q[4]["prereq"]:
            assert p in ids, "prerrequisito inexistente %s" % p
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False, indent=2)
    print("misiones:", len(QUESTS), "lineas:", len(LINES))
