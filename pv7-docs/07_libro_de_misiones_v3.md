# ArreMods — Libro de misiones v3 (capítulos 1 a 27)
**Fecha:** 2026-11-19 · **Estado:** instalado en el servidor. Reemplaza a `06_libro_de_misiones_v2.md`.

## Qué cambió desde la v2
1. **Se quitaron 26 mods del servidor** ("aligerar", 03:27). Los JAR están en `mods-desactivados/ArreMods-quitados/`:
   CreativeCore, CyclopsCore, EnergeticSheep, FenceOverhaul, Floocraft, Gargoyles, ItemPhysic, MCMultiPart,
   NotEnoughItems, Bagels More, Bookworm, Creature Whisperer, DRP Core, DRP Medieval, Fairy Lights, MalisisCore,
   MalisisDoors, Moon Core, Nice, Painting Selection GUI, SonarCore, StructPro, Teletoro, ThutCore, ThutTech y ZAWA.
   - Copias previas: `backups/arremods-antes-de-aligerar-20261119-032733.tar.gz` (servidor) y `backups/arremods-mundo-apagado-032815.tar.gz` (mundo).
   - Al arrancar, Forge avisa "missing id from the world" por los bloques y criaturas de esos mods que había en el mundo y los borra. Es normal.
2. **El libro dejó de nombrar los mods quitados**: Teletoro (cap. 4), ZAWA (cap. 17) y ThutTech (cap. 25). Quedaban 133 misiones (antes 135). Ver más abajo: ahora son 132.
3. **Se resolvieron los pendientes marcados "[en prueba]"**. Ya no queda ninguno en el libro. Datos leídos del código y de los archivos de cada JAR:

| Cap. | Pendiente | Resultado verificado |
|---|---|---|
| 6 | Piezas del talismán | Las 4 piezas las sueltan los **Druidas Oscuros**: 50 % de chance por muerte, siempre una pieza que el jugador todavía no tiene. Tiene que matarlos el jugador |
| 7 | Piña Colada | En la **Drink Mixer** (8 Chunk O' Head alrededor de una taza de bambú): ananá o cubos de ananá + coco o trozo de coco. No lleva agua |
| 7 | Portal con la varita | Anillo 5×5 de **arenisca** con 3×3 de **agua** adentro (aire arriba, altura ≥ 9). Clic derecho cerca con la varita en "Portal Build Mode"; gasta 1 de durabilidad. El modo "Instant Teleport" solo funciona en creativo |
| 8 | Portal Dialer | Está en las mazmorras-portal (no tiene receta). Clic derecho con la runa: la deja puesta y elige el destino. Hay que pararse frente al dialer. Clic derecho con la mano vacía devuelve la runa. En las otras dimensiones el dialer solo vuelve al Overworld |
| 8 | Partes 2 de runas | En cofres de las mazmorras: Agua en la de Tierra, Aire en la de Agua, Espíritu en la de Aire y Fuego en la de Espíritu |
| 9 | Portal de caza | Misma forma que el portal del Nether. Se activa con espada, arco o mechero. Se cruza agachado |
| 12 | Draconio | Overworld y dimensiones de mods: en piedra, capas 2 a 8. Nether: capas 1 a 125. End: capas 1 a 70. No hay dimensiones excluidas en la config |
| 13 | Error de accesorios | Solo afecta al ajuste `punchy.ring.attack.damage` (es un número decimal y el mod no lo puede leer). El Punchy Ring queda con su valor de fábrica |
| 13 | Soul Ingot | Fragmento de alma al centro, Harshen Crystal a los costados y Emerald Shard arriba y abajo. El fragmento sale del Soul Ore, que solo se mina con el Soul Harsher Pickaxe (sala del tesoro de Kazzendre) |
| 13 | Puerta a Pontus | 3 partes del Gate Spawner (castillo de Kazzendre y santuarios) + fragmento de alma en el **Lightning Ritual**. Usada sobre un bloque, crea la puerta. Es temporal y se reactiva tirándole un Ritual Crystal activo. La versión "Enhanced" es permanente |
| 13 | Kazzendre | No tiene barra de jefe, pero tiene 380 de vida y armadura. Hay uno solo por mundo |
| 15 | Elixires y BWM | No interfieren: los elixires son un ítem propio de Rustic y se hacen en el Alchemic Condenser |
| 16 | Pesadilla | Al dormir hay 5 % de chance. Aparece una de tres, con la misma probabilidad: Hag, Shadow Person u 8 Phantasmic Spiders. **La misión ahora acepta cualquiera de las tres** (antes pedía solo la Sombra) |
| 16 | Armadura del Rey Zombi | 20 % de chance al morir: 5 % por cada pieza |
| 18 | Wolfsbane | Poción rara + flor Wolfsbane en el soporte de pociones. Da 30 s de veneno y náuseas. Cura al hombre lobo o la infección; si no hay ninguna de las dos, da inmunidad o la quita |
| 20 | Mob Totems | Totemic Focus → madera de tótem; Carving Knife → tallado; tótem de 2 o 3 bloques con una Offering Box al lado del bloque de abajo. Efectos y modificadores en el texto de la misión |
| 20 | SecurityCraft | Key Panel (8 botones de piedra + placa de presión pesada). Teclado = Frame (7 hierros + redstone) colocado + clic derecho con el Key Panel |
| 25 | MineColonies | SupplyCamp Chest (5 cofres en U, terreno plano de 16×17) o SupplyShip Chest (5 botes en U, en el agua). Uno por jugador |
| 25 | MCA | Anillo de compromiso: 7 lingotes de oro (o de oro rosa) + 1 diamante |

## Archivos
| Archivo | Qué es |
|---|---|
| `herramientas/generar_misiones.py` | Generador v3. Para cambiar algo, se edita acá y se regenera con `python -I generar_misiones.py ../ArreMods_misiones.json` |
| `ArreMods_misiones.json` | Libro v3. Es el mismo archivo que `world/betterquesting/QuestDatabase.json` y `config/betterquesting/DefaultQuests.json` |
| `ArreMods_misiones_v2.json` | Libro anterior (el que estaba instalado antes de esta versión) |
| `../backups/QuestDatabase.v2-*.json`, `QuestProgress.v2-*.json` | Estado del mundo antes de instalar la v3 |
| `../backups/generar_misiones.antes-pendientes-*.py` | Generador v2 (reproduce exactamente el libro v2) |

El progreso de los jugadores se mantiene: ninguna de las misiones que cambiaron tenía progreso.

## Cambios del 2026-11-19 (tarde)
- **Reglas del servidor** escritas en la misión 0 (cap. 1). Las acordadas con el administrador: somos amigos, no se roba ni se rompe lo ajeno, las trampas valen y nadie va al End antes de la expedición grupal. Las agregó Claude: PvP solo de común acuerdo, sin hacks ni x-ray, granjas sin lag y reclamar los chunks con FTB Utilities (el reclamo de chunks ya está activo en `config/ftbutilities.cfg`).
- **Expedición grupal al End:** la misión 2102 se completa para cada jugador que entra al End. Se quitó la misión 1203, que repetía lo del dragón. El Wyvern Core (1204) ahora pide la 2102. Quedan **132 misiones**.
- **Recompensas nuevas:** el número de `r_xp(n)` del generador ahora es la dificultad de la misión. `quest()` lo cambia por un premio de **puntos** de XP más objetos, según la tabla `NIVELES_PREMIO`:

| Dificultad | Puntos de XP | Objetos | Misiones |
|---|---|---|---|
| 1-2 | 30 | 4 panes | 8 |
| 3-4 | 60 | 2 lingotes de hierro | 32 |
| 5-6 | 120 | 4 de hierro + 4 panes | 39 |
| 8-12 | 250 | 4 de oro + 2 perlas de ender | 29 |
| 14-20 | 500 | 2 diamantes + 1 manzana dorada | 10 |
| 25-30 | 900 | 4 diamantes + 2 manzanas doradas | 6 |
| 40-50 | 1400 (≈ nivel 0 → 30) | 6 diamantes + 1 manzana de Notch | 3 |

  Antes se daban **niveles**, que valen más cuanto más alto está el jugador. Con 50 niveles de golpe alcanzaba para encantar muchas veces. Para cambiar los premios, se edita la tabla y se regenera.
- **JourneyMap 5.5.3 → 6.0.10** en el servidor. El error `jm_dim_permission` era un fallo de la 5.5.3: el servidor nunca registraba ese mensaje (verificado en `PacketHandler.init`). La 6.0.10 usa otro sistema de red y acepta clientes de cualquier versión (`acceptableRemoteVersions = "*"`). Arrancó sin errores nuevos. La 5.5.3 quedó en `mods-desactivados/reemplazados/`.
  - La 6.0.10 dice "Forge 14.23.5.2860" en su changelog, pero no lo exige. Con el Forge actual (2768) arranca bien.
  - Falta probar que entre un jugador. Los clientes que sigan con la 5.5.3 entran igual, pero no reciben las opciones del servidor. Conviene pasarles la 6.0.10 (Modrinth, SHA-1 `6455be4d12b507878067738ccb23cfa02992c719`).

## Aspecto del libro (2026-11-19)
- **Tema "Libro de aventuras"** (`arremods:libro`): tapa de cuero con costura dorada y hojas de pergamino. Lo genera `herramientas/generar_tema_libro.py` en `config/betterquesting/resources/arremods/`. Hereda de `bq_standard:light`, y los marcos de los íconos son los de ese tema.
- **Español:** traducciones de Better Questing y Standard Expansion en `config/betterquesting/resources/{betterquesting,bq_standard}/lang/` (es_ar, es_es, es_mx). Los nombres de objetos y criaturas de otros mods siguen en inglés, porque esos mods no traen español.
- **Sin "[V] Verificado…"** en los textos.
- **Espacio de la descripción:** Better Questing parte la columna izquierda en dos mitades fijas (descripción arriba, recompensa abajo) cuando la misión tiene recompensas. Está fijo en el código de `GuiQuest`. No se puede cambiar con temas ni configs; la descripción tiene barra de desplazamiento.
- Todo esto es del **cliente**: cada jugador necesita la carpeta `config/betterquesting/resources/` y `S:Theme=arremods:libro` en su `config/betterquesting.cfg`.

## Versión preliminar del pack (2026-11-19): sin Better With Mods
- Se quitaron **Better With Mods 2.3.19** y **BetterWithLib 1.5** porque su modo difícil complicaba demasiado el juego para jugadores nuevos. Los JAR están en `mods-desactivados/BWM-quitado/`. Copia del mundo previa: `backups/mundo-antes-quitar-bwm-*.tar.gz`.
- Vuelven las recetas normales de Minecraft: herramientas de diamante, tintes de flores, azúcar, polvo de blaze, piedra musgosa y carbón vegetal en el horno.
- Libro: se quitó el capítulo "Better With Mods" (14 misiones), se renumeraron los capítulos 15-27 a 14-26 y se sacaron las menciones al Molino, el Kiln y las recetas difíciles. Quedan **118 misiones en 26 capítulos**. El progreso de las misiones 1400 y 1401 se perdió con el capítulo.
- Los jugadores tienen que quitar esos dos JAR de su cliente.

## Textos ampliados (2026-11-19, libro v8)
- Se reescribieron las descripciones de unas 80 misiones para que expliquen **cómo** se consigue cada cosa, no solo qué hay que hacer. Están en la tabla `TEXTOS` de `herramientas/generar_misiones.py`, que reemplaza la descripción corta de cada misión al generar el libro.
- Se borraron las líneas de referencia interna: `Logro "…"`, `ID: …`, "Usá solo guías de la versión 1.12.2", "Logro del mod: …", el aviso técnico de Harshen y la mención de PV7Core.
- Astral Sorcery: los 9 textos salen del diario del propio mod (`en_US.lang`). Cada misión tiene su ícono propio (antes todas usaban polvo de piedra luminosa).
- Datos sacados del código y verificados:
  - **Cavern:** el marco es de **piedra musgosa o ladrillo de piedra musgoso** (antes decía "ladrillo de piedra", y está mal). Las llaves de cada portal son esmeralda, aguamarina, Miner's Thought Orb, cualquier brote, hielo compacto y diamante. A **Cavenia** se entra con clic derecho y un **Cavenic Orb** estando en cualquier caverna; el orbe lo sueltan los monstruos cavénicos 1 de cada 8 veces. El Miner's Thought Orb sale en los cofres de las torres-mazmorra (1-2 por cofre). La randomita suelta un objeto al azar. Los Magical Books los sueltan los jefes Crazy de Cavenia (el Crazy Zombie tiene 2000 de vida).
  - **Betweenlands:** el Mummy Bait se arma con un frasco de aspecto Armaniis, una Shimmerstone, un corazón animado de Tar Beast y una bola de lodo. Se tira al suelo en los biomas Sludge Plains o Marsh. La savia sale del Sap Tree Log. Hay recetas confirmadas de la antorcha de azufre, los dos hornos de azufre, la mesa de weedwood y las espadas.
  - **Elemental Dimensions:**
    - El Dirt Zombie Boss aparece solo cerca de la medianoche en la dimensión Tierra.
    - Las semillas de los otros jefes se tiran: la de agua al agua en la dimensión Agua; las de aire y fuego al suelo, en su dimensión. Las de aire y fuego explotan antes de que salga el jefe.
  - **SpookyCraft:** el Scarecrow aparece de noche en las llanuras (Plains). Si de noche llevás una calabaza o una cabeza de mob puesta, aparecen monstruos espeluznantes alrededor; la opción `pumpkinHats` viene activada.
- Siguen cortas (menos de 200 caracteres) 15 misiones que ya tienen la receta completa y no necesitan más.

## Mods nuevos (2026-11-19, noche) — `ArreMods_misiones_v8.json`
- **Mods:**
  - **Quitados:** MineColonies, SpookyCraft (con craftdev-core), Re-Zombies e Immersive Engineering. Los JAR están en `mods-desactivados/quitados-mods-nuevos/`.
  - **Agregados:** Tinkers' Construct, Ender IO, Applied Energistics 2, Mystical Agriculture, Iron Furnaces, Ender Storage, Item Collectors, Baubley Heart Canisters, Simple Voice Chat y OreExcavation (en lugar de FTB Ultimine, que no existe para 1.12.2).
  - **Forge** pasó a 14.23.5.2860.
- **Libro: se quitaron 4 misiones:** el Scarecrow (1601), el Zombie King (1602) y las dos de MineColonies (2500 y 2501). El capítulo de aldeanos quedó solo con MCA ("Vida en la aldea").
- **Capítulos nuevos, en el bloque de magia y tecnología** (los IDs de misión arrancan en 3000, así no se toca el progreso guardado):

| Cap. | Mod | Misiones |
|---|---|---|
| 15 | Tinkers' Construct | Part Builder → Tool Station / pico a medida → Smeltery → Tool Forge / Manyullyn |
| 16 | Ender IO | máquina simple → Stirling / Electrical Steel → conductos → Capacitor Bank / Dark Steel → equipo de Dark Steel |
| 17 | Applied Energistics 2 | certus → brújula de meteoritos / Charger → Inscriber → ME Controller → Drive + celda 1k / Molecular Assembler |
| 18 | Mystical Agriculture | semillas tier 1 → cristal de infusión / semilla de recurso → tier 2 → cristal maestro / semillas de diamante → Supremium |
| 19 | Taller y mejoras | Iron Furnace → Diamond Furnace; Ender Chest → tanque/bolsa; Item Collector; corazón rojo → amuleto + canister |

- **Misiones sueltas:** Voice Chat en el cap. 1 (3500) y OreExcavation en el cap. 3 (3501). Las dos son de marcar la casilla.
- **Renumeración:** los capítulos de combate y maestría pasaron de 15–26 a **20–31**. Todas las referencias "cap. N" de los textos se actualizaron. Por ejemplo, la expedición al End ahora es el cap. 25.
- **Datos usados en los textos nuevos:**
  - **Heart Canisters** (`config/bhc/bhc-drops.json`): el corazón rojo lo suelta cualquier monstruo hostil (5 %), el amarillo los jefes, el verde el dragón y el azul los Evokers. El Wither Bone sale el 15 % de las veces.
  - **Item Collectors:** alcance de 5 bloques (básico) y de 7 con filtro (avanzado).
  - **OreExcavation:** tecla "`", hasta 128 bloques, con TPS Guard.
  - **Ender Storage:** inventario 3×9, y el diamante lo hace personal.
- **Verificación:** todos los IDs de objetos y criaturas del libro se cruzaron con el registro de `world/level.dat`: 0 desconocidos. El servidor arrancó con el libro instalado ("Loaded 150 quests", "Loaded 31 quest lines").
- **150 misiones en 31 capítulos.**

## Lo que sigue pendiente
1. **PV7Core** (clanes, puntos y ranking): en pausa hasta definir para qué se quiere.
2. **Probar JourneyMap 6.0.10 con un jugador conectado.**
3. **Probar las recompensas jugando** y ajustar la tabla si hace falta.
