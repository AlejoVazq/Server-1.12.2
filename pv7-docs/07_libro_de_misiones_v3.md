# ArreMods — Libro de misiones v3 (capítulos 1 a 27)
**Fecha:** 2026-11-19 · **Estado:** instalado en el servidor. Reemplaza a `06_libro_de_misiones_v2.md`.

## Qué cambió desde la v2
1. **Se quitaron 26 mods del servidor** ("aligerar", 03:27). Los JAR están en `mods-desactivados/ArreMods-quitados/`:
   CreativeCore, CyclopsCore, EnergeticSheep, FenceOverhaul, Floocraft, Gargoyles, ItemPhysic, MCMultiPart,
   NotEnoughItems, Bagels More, Bookworm, Creature Whisperer, DRP Core, DRP Medieval, Fairy Lights, MalisisCore,
   MalisisDoors, Moon Core, Nice, Painting Selection GUI, SonarCore, StructPro, Teletoro, ThutCore, ThutTech y ZAWA.
   - Copias previas: `backups/arremods-antes-de-aligerar-20261119-032733.tar.gz` (servidor) y `backups/arremods-mundo-apagado-032815.tar.gz` (mundo).
   - Al arrancar, Forge avisa "missing id from the world" por los bloques y criaturas de esos mods que había en el mundo y los borra. Es normal.
2. **El libro dejó de nombrar los mods quitados**: Teletoro (cap. 4), ZAWA (cap. 17) y ThutTech (cap. 25). Quedan **133 misiones** (antes 135).
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

## Lo que sigue pendiente
1. **Texto de las reglas del servidor** (cap. 1, misión "Tu libro de aventuras"). Lo tiene que escribir el administrador.
2. **Recompensas**: son niveles de XP y pocos ítems. Hay que ajustarlas después de probar el juego.
3. **PV7Core** (clanes, puntos y ranking): queda para su propia sesión.
4. **JourneyMap**: al entrar un jugador, el servidor da un error de red (`jm_dim_permission`), aunque cliente y servidor usan la misma versión (5.5.3). Es un fallo del mod y no impide jugar. Lo único que se pierde es que el servidor no puede mandar los permisos de mapa por dimensión, así que el cliente usa los de fábrica.

## Para los jugadores
- Tienen que tener `para-el-cliente/StandardExpansion-3.4.173.jar` en la carpeta `mods` del cliente.
- Conviene que también borren de su cliente los 26 mods quitados. El cliente del administrador ya coincide con el servidor.
