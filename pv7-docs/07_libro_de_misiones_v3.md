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

## Lo que sigue pendiente
1. **PV7Core** (clanes, puntos y ranking): en pausa hasta definir para qué se quiere.
2. **Probar JourneyMap 6.0.10 con un jugador conectado.**
3. **Probar las recompensas jugando** y ajustar la tabla si hace falta.
