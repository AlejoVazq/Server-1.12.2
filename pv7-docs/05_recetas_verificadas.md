> **Desactualizado:** este documento es de cuando el servidor tenía Better With Mods. Se quitó el 2026-11-19, así que las recetas normales de Minecraft volvieron (tintes, carbón vegetal, herramientas de diamante, etc.).

# PV7 — Recetas verificadas del Bloque I (capítulos 1 a 5)
**Fecha:** 2026-11-19 · Completa los **[P]** de recetas del documento 03.

**Cómo se verificó:** leyendo los JAR de `mods/` (recetas JSON y, cuando el mod las registra por código, el bytecode), las configs de `config/` y el registro de ítems guardado en `world/level.dat`. Los nombres internos de Minecraft (`field_…`) se tradujeron con los datos de Forge y el JAR del servidor, no de memoria.

**Leyenda:** **[V]** verificado en archivos · **[D]** conocido del mod, no comprobado · **[P]** sigue pendiente (ver lista al final).
Notación de grillas: cada fila es una fila de la mesa de crafteo; `·` = casilla vacía.

---

## Lo que Better With Mods cambia en estas recetas [V]
El log del servidor lista 28 recetas vanilla eliminadas. Las que afectan al Bloque I:
- **Tintes de flores** (rojo, amarillo, etc.): ya no se hacen en la mesa. El tinte rojo y el amarillo se usan en el **cuchillo** y el **kit** del Camping Mod, y en el Disenchanter. Los tintes salen del **Molino de BWM** [V que la receta vanilla no existe / D que el molino muele flores].
- **Azúcar:** sale de moler caña en el Molino [V, `MillRecipes`]. Afecta los malvaviscos del Camping Mod.
- **Polvo de blaze:** sale de moler varas de blaze en el Molino [V]. Afecta el **Ojo de Ender**, que pide el Switch-Bow.
- **Diamante:** herramientas y armaduras vanilla de diamante eliminadas. Las recetas de mods con diamante (martillo de diamante, escudo de diamante) **siguen existiendo** [V].
- **Carbón vegetal en horno desactivado** (`Disable Furnace Charcoal=true`): se hace en el horno de BWM (Kiln) [V config]. Importa para las antorchas del capítulo 2.
- Cocina normal: `HCCooking=false` y `HCFurnace=false`, así que el horno y la comida funcionan como en vanilla [V]. `FoodPoisoning=false` [V].
- La mesa de encantamientos **mantiene su receta** (`HCStructures=false`) [V].

---

## Capítulo 2

### C2-Q01 · Madera
- **Ítem:** cualquier tronco (diccionario `logWood`).
- **Cantidad elegida:** 16 troncos. *Es una decisión de diseño mía (no sale de archivos); ajustala si querés.*

### C2-Q03 · Camping Mod 2.4.2 [V]
| Ítem (ID) | Receta |
|---|---|
| **Navaja suiza** `camping:knife` | `R I R` / `R I R` / `R I R` → 6 **tinte rojo** + 3 lingotes de hierro |
| **Palo de hierro** `camping:parts@1` | 2 lingotes de hierro en vertical |
| **Estaca** `camping:parts@2` | palo de hierro + navaja (sin forma) |
| **Lona** `camping:parts@0` | cáñamo (`camping:hemp`) + navaja (sin forma) |
| **Tienda** `camping:tent` (sale blanca, meta 15) | `L L L` / `L · L` / `E · E` → 5 lonas + 2 estacas. Se tiñe con 1 tinte (sin forma) |
| **Saco de dormir** `camping:sleeping_bag` | navaja arriba (cualquier columna) + 3 lanas de cualquier color abajo |
- El cáñamo crece en el mundo (`Enable Hemp generation=true`, multiplicador 5) [V config].
- **Ojo:** la navaja necesita 6 tintes rojos, que con BWM salen del Molino. Es más cara de lo que parece al inicio. **Recomendación:** que la misión acepte tienda **o** saco, pero avisando que ambos requieren navaja.
- Si la navaja se gasta o se conserva al craftear: [P].

### C2-Q04 · Fogata
| Mod | Ítem (ID) | Receta |
|---|---|---|
| **Campfire 1.2** | `campfire:campfire` | `· T ·` / `T T T` / `P P P` → 4 troncos + 3 palos [V] |
| Camping Mod (alternativa) | `camping:campfire_wood_off` | `· P ·` / `P · P` / `P · P` → 5 palos [V] |
| Camping Mod (para cocinar) | `camping:campfire_cook` | `· C ·` / `C · C` / `· C ·` → 4 piedra labrada [V] |
- Campfire 1.2: se apaga a los 7000 ticks (≈ 6 min) (`burnout_time=7000`) [V config].

### C2-Q07 · Primera comida
- Cualquier comida cocinada en horno vanilla vale: carne de vaca, cerdo, pollo, cordero, conejo, pescado, papa asada; o pan. También **venado cocido** del Camping Mod (`camping:venison_cooked`) [V ID].
- **Propuesta para la misión:** aceptar cualquiera de estos (tarea "cualquiera de la lista").

---

## Capítulo 3

### C3-Q02 · Spartan Shields 1.4.1 [V]
| Ítem (ID) | Receta |
|---|---|
| **Escudo de madera** `spartanshields:shield_basic_wood` | `T T ·` / `T P T` / `· T T` (o en espejo) → 6 tablones + 1 palo |
| Escudo de piedra / hierro / oro / obsidiana / diamante | `· M ·` / `M E M` / `· M ·` → 4 del material alrededor del **escudo de madera** |
- Piedra = piedra labrada (`cobblestone`). Diamante sigue disponible (es receta del mod).
- **Mod-compat que NO aparece:** los escudos de Botania, Thermal, AbyssalCraft, etc. solo se activan si el mod está; aquí no están. El de **acero de BWM** (`shield_basic_soulforged_steel`) sí existe, pero exige acero de alma (muy tarde).

### C3-Q03 · Switch-Bow 1.5.5 [V]
`Easy Crafting=false` en la config, así que se usan las recetas difíciles:
| Ítem (ID) | Receta |
|---|---|
| **Switch-Bow** `switchbow:switchbow` | `· P H` / `P O H` / `· P H` → 3 palos + 1 **ojo de ender** + 3 hilos |
| **Carcaj** `switchbow:quiver` | `C H C` / `C B C` / `· C` → cuero, hilo y un **cofre** (la última fila se ve corta en el código; confirmá la forma en JEI) |
| Switch-Crossbow `switchbow:switchcrossbow` | `O L L` / `L T H` / `L H T` → ojo de ender, hierro, tablones, hilo |
- **Ojo:** el ojo de ender necesita polvo de blaze, que con BWM sale del Molino. El Switch-Bow es de mitad de juego (requiere Nether), **no** del inicio. Recomiendo mover C3-Q03 a "opcional" o al bloque de combate.

### C3-Q04 · Hammer Time 2.2.0 [V]
| Ítem (ID) | Receta |
|---|---|
| **Martillo** `hammertime:itemhammer{wood,stone,iron,gold,diamond}` | `M M M` / `M P M` / `· P ·` → 5 del material + 2 palos |
- Madera = **troncos** (no tablones). Piedra = **piedra lisa** (`stone`), no piedra labrada.
- `Durability Modifier=3.0` en la config: más durabilidad que la herramienta normal [V config; efecto exacto D].
- También hay hachas grandes, palas y hoces del mismo mod.

### C3-Q05 · Disenchanter 1.6 [V]
| Ítem (ID) | Receta |
|---|---|
| **Mesa de desencantar** `disenchanter:disenchantmenttable` | `· · ·` / `A E A` / `E M E` → 2 tintes amarillos + 3 esmeraldas + 1 mesa de encantamientos |
- El tinte amarillo sale del Molino de BWM. La mesa de encantamientos tiene su receta normal.
- Mejoras (automática, en lote, vaciado) activadas en la config.
- Cómo interactúa con `HCEnchanting` de BWM: [P].

---

## Capítulo 4

### C4-Q01 · Nature's Compass 1.5.1 [V]
| Ítem (ID) | Receta |
|---|---|
| `naturescompass:naturescompass` | `S T S` / `T B T` / `S T S` → 4 brotes (cualquiera) + 4 troncos + 1 brújula |
- `allowTeleport=true`: un **operador** puede teletransportarse al bioma desde la brújula [V config; D que solo lo hace un op].

### C4-Q02 · Biomas disponibles [V, registro del mundo]
- 62 biomas vanilla, 10 de Tropicraft, 8 de Betweenlands y 3 de Harshen Universe. Los de Tropicraft y Betweenlands están en **sus dimensiones**, no en el Overworld [D].
- **Propuesta:** la misión pide llegar a cualquier bioma nuevo; si querés uno fijo, uno común y seguro es **Savanna** o **Mesa** (vanilla).

### C4-Q03 · Rope Bridge 2.0.7 [V]
| Ítem (ID) | Receta |
|---|---|
| **Cuerda** `ropebridge:rope` ×8 | `H E ·` / `E H ·` / `H E ·` → 3 hilos + 3 enredaderas |
| Gancho `…bridge_builder_material.hook` | `I · ·` / `I I I` / `I · ·` → 5 hierro |
| Cañón `…bridge_builder_material.barrel` | `I I I` / `C C C` / `I I I` → 6 hierro + 3 cuerdas |
| Mango `…bridge_builder_material.handle` | `I · F` / `C G ·` / `I T T` → 2 hierro, mechero, cuerda, pólvora, 2 tablones de roble |
| **Lanzador de puentes** `ropebridge:bridge_builder` | gancho + cañón + mango en una fila |
- Total ≈ 13 lingotes de hierro: es objetivo de mitad del juego temprano, no del primer día.
- Bonus: el mod agrega 1 lana → 4 hilos.
- Gasto por bloque de puente: 2 cuerdas, 2 hilos, 1 madera, 1 losa; máximo 400 bloques [V config].

### C4-Q04 · Teletoro [V recetas / P comportamiento]
- `teletoro:teletory_portal_linker` = 2 **Teletory Pearl** + 1 **Ender Block** (4 perlas de ender). Botas de Ender = 4 perlas.
- De dónde sale la Teletory Pearl y qué permite el portal: [P].

---

## Capítulo 5

### C5-Q03 · Mochilas [V]
| Mod | Ítem (ID) | Receta |
|---|---|---|
| **Backpacks 3.5.4** | Bolsillo `backpacks16840:backpack_pouch` | `C C H` / `C · H` / `C C H` → 5 cueros + 3 hilos |
| | **Mochila** `backpacks16840:backpack` | `C C C` / `C · C` / `C P C` → 7 cueros + 1 placa de presión de oro (opcional: tinte al centro) |
| **Iron Backpacks 3.0.8** | Mochila básica `ironbackpacks:backpack` | `L Cu L` / `Cu Co Cu` / `L Cu L` → 4 lanas + 4 cueros + 1 cofre |
| Camping Mod | Bolsa `camping:bag` | `· H ·` / `C · C` / `C C C` → 1 hilo + 5 cueros |
- La mochila de Iron Backpacks guarda su tipo en datos internos (NBT): la misión debe **ignorar NBT** al comprobarla.
- Backpacks: "los ojos de ender pueden duplicar mochilas" está activado (`Ender eyes can duplicate backpacks=true`). Probablemente sea para mochilas cuánticas, pero conviene revisarlo por si es un exploit [P].

### C5-Q04 · Storage Drawers [V]
| Ítem (ID) | Receta |
|---|---|
| **Cajón 1×1** `storagedrawers:basicdrawers` | `T T T` / `· C ·` / `T T T` → 6 tablones + 1 cofre → **1** cajón |
| Cajón 1×2 / 2×2 | variantes con 2 o 4 cofres → 2 y 4 cajones (salida según config) |
| Controlador `storagedrawers:controller` | `P P P` / `K X K` / `P D P` → piedra lisa, 2 comparadores, 1 cajón, 1 diamante |
- La madera del cajón depende de los tablones usados. La misión debería aceptar cualquier variante (ignorar meta/NBT).

### C5-Q05 · Chest Transporter 2.8.8 [V]
- **Transportador de madera** `chesttransporter:chesttransporter`: `P · P` / `P P P` / `· P ·` → 6 palos.
- Variantes de hierro, oro, diamante y obsidiana: el palo central se cambia por el material. Las de cobre, plata y estaño **no se pueden fabricar** (no hay esos metales en el pack).
- Al cargar un cofre da hambre, lentitud, fatiga minera y menos salto (`debuff*=true`) [V config]. También permite mover **spawners** (`pickupSpawners=true`): ojo, eso es fuerte [V config].

### C5-Q06 · Cultivos [V IDs]
- Vanilla: trigo, zanahoria, papa, remolacha. Las semillas salen de la hierba normal (`HCSeeds=false`).
- Rustic: **tomate** (`rustic:tomato`), **chile** (`rustic:chili_pepper`), **uvas** (`rustic:grapes`), y semillas de manzana. Tomate y chile usan una **estaca de madera** (`rustic:crop_stake`) [D].
- **Propuesta:** aceptar cualquiera de: trigo, zanahoria, papa, remolacha, tomate, chile.
- `HCSapling=true`: los árboles plantados pasan por etapas extra [D].

### C5-Q07 · Water Strainer 3.2.0 [V]
| Ítem (ID) | Receta |
|---|---|
| Base `waterstrainer:strainer_base` | `B · B` / `T To T` / `T C T` → 2 barrotes de hierro, 4 tablones, 1 tolva, 1 cofre |
| Filtro de supervivencia `waterstrainer:strainer_survivalist` | 8 palos alrededor de una **red** (`waterstrainer:net`, hecha de hilo) |
- Qué da (config `waterstrainer_loottables.cfg`): filtro común → palos, arcilla, piedra, tablones; filtro denso → arena, tierra, grava y a veces pepitas de oro; filtro de pescador → peces, basura y rara vez un libro encantado.
- La forma exacta de la red: [P] (el código registra dos variantes; mirala en JEI).

---

## Capítulos 1 y 5: datos de libro y comandos
- **Libro de misiones:** `questbook:itemquestbook` = libro + palo (sin forma) [V].
- Atajos de JEI (R/U), uso de Hwyla, JourneyMap y `/home` de FTBUtilities: siguen siendo [D]/[P] (se confirman jugando).

---

## Pendientes que NO se pueden cerrar leyendo archivos
1. Si la navaja del Camping Mod se gasta al usarla en recetas.
2. Forma exacta del carcaj de Switch-Bow y de la red del Water Strainer (el código tiene filas cortas; JEI lo muestra bien).
3. Cómo afecta `HCEnchanting` al Disenchanter.
4. De dónde sale la Teletory Pearl y qué permite el portal de Teletoro.
5. Si "ojos de ender duplican mochilas" es un exploit.
6. Qué molino de BWM se necesita para cada tinte (las flores se procesan en un bucle del código que no se puede leer como lista).
7. Qué pasa en una pesadilla (Nightmares), cuánto dura una tumba (Tombstone), los límites de claims y los comandos de FTBUtilities, y si los atajos de JEI están cambiados. Todo eso se ve jugando.
