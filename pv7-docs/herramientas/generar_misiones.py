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

def chapter(name, desc, icon):
    LINES.append((name, desc, icon)); _line[0] = len(LINES) - 1

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
      "(cap. 21) y se organiza entre todos.\n"
      "§e5.§r Pelear contra otro jugador solo si los dos están de acuerdo.\n"
      "§e6.§r Nada de hacks, x-ray ni programas para sacar ventaja.\n"
      "§e7.§r Si una granja o una máquina hace lagear el servidor, se apaga o se achica.\n"
      "§e8.§r Reclamá los chunks de tu base en el mapa de FTB Utilities: así nadie la puede romper sin querer. "
      "Si vas a construir cerca de otro, avisale antes.",
      item("questbook:itemquestbook"), [t_check()], [r_xp(1)], main=True)
quest(2, 48, 0, "Este mundo no es vanilla",
      "El modo difícil de §6Better With Mods§r cambia recetas: §cno§r se fabrican herramientas ni armaduras de diamante vanilla, "
      "tintes de flores, azúcar, polvo de blaze ni piedra musgosa. Tintes, azúcar y polvo de blaze salen del §eMolino§r de BWM; "
      "el carbón vegetal, del horno de ladrillo (Kiln).\n\n"
      "§eHerramientas de consulta:§r\n · JEI: §eR§r = cómo se fabrica, §eU§r = para qué sirve.\n"
      " · Hwyla: mirá un bloque y te dice qué es y de qué mod viene (no muestra el interior de los cajones)." + V,
      item("minecraft:crafting_table"), [t_check()], [], prereq=[0])
quest(5, 96, 0, "Tu primer mapa",
      "Abrí JourneyMap (§eJ§r), creá un waypoint en tu base (§eB§r) y ponele nombre.\n\n"
      "§7Todos deben usar JourneyMap 5.5.3, igual que el servidor.§r",
      item("minecraft:map"), [t_check()], [r_xp(2)], prereq=[0])

chapter("Cap. 2 · Los primeros días", "Madera, refugio, descanso, fuego y comida.", item("campfire:campfire"))
quest(10, 0, 0, "Madera y refugio",
      "Juntá §e16 troncos§r y armá un refugio con paredes, techo, puerta y luz adentro.\n\n"
      "§eConsejo:§r el carbón vegetal no sale del horno; buscá carbón mineral para las antorchas.",
      item("minecraft:log"), [t_get([item("minecraft:log", 16, WILD, "logWood")])],
      [r_items([item("minecraft:torch", 8)])], prereq=[0], main=True)
quest(12, 48, -24, "Descansar (Camping Mod y Nightmares)",
      "Fabricá una §etienda§r o un §esaco de dormir§r.\n"
      " · §6Navaja suiza:§r 6 tintes rojos + 3 hierro (el tinte rojo sale del Molino).\n"
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
      "La comida cruda no envenena acá.\n\n"
      "§6Si morís:§r tu equipo queda en una §etumba§r (Tombstone); volvé a buscarla. "
      "En la §eHunting Dimension§r no podés reaparecer; en §eCavenia§r no perdés inventario ni experiencia." + V,
      item("minecraft:cooked_beef"),
      any_get([item("minecraft:cooked_beef"), item("minecraft:cooked_porkchop"), item("minecraft:cooked_chicken"),
               item("minecraft:cooked_mutton"), item("minecraft:cooked_rabbit"), item("minecraft:cooked_fish", 1, WILD),
               item("minecraft:baked_potato"), item("minecraft:bread"), item("camping:venison_cooked")]),
      [r_xp(2)], prereq=[13], logic="OR")

chapter("Cap. 3 · Preparación del aventurero", "Escudos, martillos y arcos.", item("spartanshields:shield_basic_wood"))
quest(20, 0, 0, "Equipo de verdad (Spartan Shields)",
      "Las herramientas y armaduras de diamante vanilla §cno§r tienen receta; las de mods sí.\n\n"
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
      "Necesita polvo de blaze (Nether + Molino). §aNo bloquea nada.§r" + V,
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
      "§7Las aldeas no generan golems de hierro. Los biomas de Tropicraft y Betweenlands están en sus dimensiones.§r",
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
      "(cap. 11-15) y combate (cap. 16-21). Elegí.",
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
      "Se hace con 8 bloques de piedra musgosa alrededor de un ingrediente (brote, hojas, enredadera, arena, hielo…).\n\n"
      "§7Con BWM la piedra musgosa no se fabrica: crece sola junto al agua.§r" + V,
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
      "Fabricá un §eWyvern Core§r. Necesita recursos del End: se desbloquea con la §eexpedición grupal§r del cap. 21.",
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

chapter("Cap. 14 · Better With Mods", "Ingeniería mecánica: molinos, sierras, hornos y acero de alma.", item("betterwithmods:material"))
BW = "betterwithmods:"
bwm = [
    (1400, "Semillas de cáñamo", "Conseguí semillas de cáñamo (salen al arar pasto).", "hemp_seed", [0]),
    (1401, "Engranaje de madera", "Fabricá un engranaje de madera.", "wood_gear", [1400]),
    (1402, "Piedra de molino", "Fabricá la Mill Stone: tintes, azúcar y polvo de blaze salen de acá.", "millstone", [1401]),
    (1403, "Eje y caja de engranajes", "Fabricá una caja de engranajes para repartir energía.", "gearbox", [1402]),
    (1404, "Molino de viento", "Fabricá un molino de viento.", "horizontal_windmill", [1403]),
    (1405, "La sierra", "Fabricá una sierra.", "saw", [1403]),
    (1406, "Fuego controlado", "Fabricá un Hibachi (fuego permanente) con fuelle.", "hibachi", [1405]),
    (1407, "El Kiln", "Construí un horno de ladrillo (Kiln) sobre un Hibachi.", "kiln", [1406]),
    (1408, "Caldero", "Fabricá un caldero de BWM. §cOjo: hay recetas explosivas.§r", "cauldron", [1402]),
    (1409, "Cuero curtido", "Conseguí cuero curtido.", "tanned_leather", [1408]),
    (1410, "Crisol", "Fabricá un crisol.", "crucible", [1407]),
    (1411, "Acero de alma", "Conseguí un lingote de Soulforged Steel. §cEn este servidor la receta es más difícil y pide End Slag.§r",
     "soul_forged_steel", [1410]),
    (1412, "Yunque de acero", "Fabricá el Soulforged Steel Anvil.", "steel_anvil", [1411]),
    (1413, "Encantador infernal", "Fabricá el Infernal Enchanter. El acero de alma solo se encanta con él.", "infernal_enchanter", [1412]),
]
pos = {1400: (0, 0), 1401: (48, 0), 1402: (96, 0), 1403: (144, 0), 1404: (192, -48), 1405: (192, 0),
       1406: (240, 0), 1407: (288, 0), 1408: (144, 48), 1409: (192, 48), 1410: (336, 0), 1411: (384, 0),
       1412: (432, 0), 1413: (480, 0)}
for qid, nm, ds, adv, pre in bwm:
    quest(qid, pos[qid][0], pos[qid][1], nm, ds + "\n\nLogro del mod: " + adv + V, item("betterwithmods:material"),
          [t_adv(BW + adv)], [r_xp(3 + (qid - 1400) // 2)], prereq=pre, main=(qid in (1400, 1413)))

chapter("Cap. 15 · Rustic", "Alquimia, vino, miel y decoración medieval.", item("rustic:elixir"))
RU = "rustic:"
quest(1500, 0, 0, "Condensador",
      "§6Condenser:§r ladrillos alrededor de un balde, con arcilla endurecida blanca abajo al centro. "
      "Destila hierbas para hacer §eelixires§r." + V,
      item(RU + "condenser"), [t_craft([item(RU + "condenser")])], [r_xp(4)], prereq=[0], main=True)
quest(1501, 48, -24, "Retorta",
      "§6Retort:§r 2 ladrillos, 1 hierro y 1 balde. Va al lado del condensador." + V,
      item(RU + "retort"), [t_craft([item(RU + "retort")])], [r_xp(3)], prereq=[1500])
quest(1502, 96, -24, "Tu primer elixir",
      "Destilá un §eelixir§r con hierbas de Rustic (aloe, chamomile, ginseng, etc.). Los elixires son un ítem propio de Rustic: "
      "los cambios de pociones de Better With Mods (soporte de pociones, pilas de 8) no los afectan." + V,
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
chapter("Cap. 16 · Criaturas de la noche", "Pesadillas, esqueletos espeluznantes y zombis especiales.", item("minecraft:skull", dmg=2))
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

chapter("Cap. 17 · Depredadores", "Deadly Monsters: los monstruos más peligrosos.", item("dmonsters:souleye"))
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

chapter("Cap. 18 · Maldición lunar", "Howling Moon: licantropía. Sin jefes.", item("howlingmoon:moonstone"))
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

chapter("Cap. 19 · Enemigos infernales", "Infernal Mobs: monstruos con poderes extra.", item("minecraft:blaze_powder"))
quest(1900, 0, 0, "Reconocer un infernal",
      "Cualquier monstruo puede salir con modificadores. Rarezas del servidor: §eÉlite§r 1 de 15, §6Ultra§r 1 de 7 entre élites, "
      "§cInfernal§r 1 de 7 entre ultra. Hay 27 modificadores activos (veneno, robo de vida, explosión, etc.).\n\n"
      "§cAntigranjas activo:§r si los matás en una trampa de mobs, dejan de dar recompensas." + V,
      item("minecraft:blaze_powder"), [t_check()], [r_xp(2)], prereq=[0], main=True)
quest(1901, 48, 0, "Tu primer infernal",
      "Derrotá a un monstruo con nombre de color (élite, ultra o infernal) y marcá la casilla.\n§7(Esta misión confía en tu palabra.)§r",
      item("minecraft:golden_sword"), [t_check()], [r_xp(8)], prereq=[1900])

chapter("Cap. 20 · Guardianes y defensas", "Totems defensores, tótems espirituales y SecurityCraft.", item("totemdefender:core"))
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

chapter("Cap. 21 · Grandes expediciones", "Jefes vanilla y expediciones en grupo.", item("minecraft:nether_star"))
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
      "(Chaos Guardian, draconio del End, End Slag de BWM).",
      item("minecraft:dragon_egg"), [t_dim(1, "The End")], [r_xp(20)], prereq=[2100])
quest(2103, 96, 0, "Guardián del templo",
      "Derrotá a un §eElder Guardian§r de un monumento oceánico.",
      item("minecraft:prismarine_shard"), [t_hunt("minecraft:elder_guardian")], [r_xp(12)], prereq=[2100])

# =============================================================================
# BLOQUE V — Maestría
# =============================================================================
chapter("Cap. 22 · El poder definitivo", "La cima de Draconic Evolution.", item("draconicevolution:chaotic_core"))
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

chapter("Cap. 23 · Maestro de las dimensiones", "Pisá todas las dimensiones del servidor.", item("minecraft:ender_eye"))
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

chapter("Cap. 24 · Coleccionista", "Logros difíciles de completar.", item("minecraft:chest"))
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

chapter("Cap. 25 · Arquitecto del mundo", "Colonias y aldeanos.", item("minecolonies:blockhuttownhall"))
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

chapter("Cap. 26 · Desafíos legendarios", "Los combates más difíciles del servidor.", item("minecraft:diamond_sword"))
quest(2600, 0, 0, "Trilogía de jefes finales",
      "Derrotá a Primordial Malevolence, al Fire Boss y al Chaos Guardian.",
      item("minecraft:diamond_sword"),
      [t_hunt(BL + "fortress_boss"), t_hunt(ED + "ed_fireboss"), t_hunt(DE + "chaosguardian")],
      [r_xp(50)], prereq=[611, 810, 1206], main=True)
quest(2601, 48, 0, "Wither en serie",
      "Derrotá al Wither 3 veces.",
      item("minecraft:nether_star"), [t_hunt("minecraft:wither", 3)], [r_xp(30)], prereq=[2101])

chapter("Cap. 27 · La última expedición", "Opcional. No bloquea nada.", item("minecraft:dragon_egg"))
quest(2700, 0, 0, "Leyenda de ArreMods",
      "Recorriste todas las dimensiones y venciste a los jefes finales. Tu nombre queda en la historia del servidor.",
      item("minecraft:dragon_egg"), [t_check()],
      [r_xp(50), r_title("Leyenda de ArreMods", ["Completaste la guía de aventuras", "de ArreMods."])],
      prereq=[2300, 2600], main=True)


def build():
    qdb = {}
    for n, (qid, line, x, y, q) in enumerate(QUESTS):
        props = {"name:8": q["name"], "desc:8": q["desc"], "icon:10": q["icon"],
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
