> **Reemplazado por `07_libro_de_misiones_v3.md`** (se quitaron mods y se resolvieron los pendientes).

# PV7 — Libro de misiones v2 (capítulos 1 a 27)
**Fecha:** 2026-11-19 · **Estado:** cargado en el servidor y verificado (`Loaded 135 quests`, `Loaded 27 quest lines`, sin errores nuevos).

## Archivos
| Archivo | Qué es |
|---|---|
| `herramientas/generar_misiones.py` | Generador v2: todo el contenido del libro. Para cambiar algo, se edita acá y se regenera |
| `herramientas/generar_misiones_v1.py` | Versión anterior (solo caps. 1-5 sin compactar) |
| `PV7_misiones_completo.json` | Libro v2. Copiado a `world/betterquesting/QuestDatabase.json` y `config/betterquesting/DefaultQuests.json` |
| `PV7_Bloque1_misiones_v1.json` | Libro v1 (32 misiones) |
| `../backups/QuestDatabase.v1-*.json`, `QuestProgress.v1-*.json` | Estado anterior del mundo |

## Cómo se verificó
- Los 148 ítems, 24 criaturas y 46 logros usados existen en el servidor (registro de `world/level.dat` y archivos de logros de cada JAR).
- Recetas citadas: leídas de los JAR (JSON o código). Dimensiones: de las configs.
- El servidor cargó el libro y lo reexportó (`config/betterquesting/saved_quests/PV7_verificacion_v2.json`) sin perder datos.

## Tipos de tarea usados
- **Logro** (`bq_standard:advancement`): se completa sola al conseguir el logro oficial del mod. Se usó en Betweenlands, Cavern, Astral Sorcery y Better With Mods, que traen su propia progresión.
- **Ubicación** con distancia −1: se completa al entrar a la dimensión.
- **Cazar** (`hunt`): cuenta solo las muertes que causa el propio jugador.
- **Fabricar**, **Conseguir** y **Casilla**. "Cualquiera de estos" se arma con varias tareas y lógica OR.

## Cambios en el Bloque I (compactado: de 32 a 18 misiones)
- Cap. 1: libro + reglas, "no vanilla" + JEI + Hwyla, mapa.
- Cap. 2: madera + refugio, descanso + pesadillas, fogata, comida + qué pasa al morir.
- Cap. 3: escudo, martillo + desencantador, Switch-Bow (opcional).
- Cap. 4: brújula, exploración, puentes + Teletoro.
- Cap. 5: terreno + /home, mochila, almacén + Chest Transporter, cultivo + Water Strainer, final.
- Se conservó el progreso de las misiones que siguen existiendo (IDs 0, 2, 5 y 40). Se quitó el de las fusionadas.

## Capítulos nuevos
| Cap. | Tema | Misiones | Notas |
|---|---|---|---|
| 6 | Betweenlands | 12 | Talismán (druidas), portal, metales, 3 jefes |
| 7 | Tropicraft | 5 | Entrada verificada en código: silla + atardecer + efecto de la Piña Colada |
| 8 | Elemental Dimensions | 11 | Dims 100-104; qué criatura suelta cada parte de runa (tablas de botín) |
| 9 | Hunting Dimension | 3 | Marco = 8 troncos + flecha; reglas de la config |
| 10 | Cavern | 9 | Portal: piedra musgosa/ladrillo + esmeralda (código) |
| 11 | Astral Sorcery | 9 | Logros oficiales |
| 12 | Draconic Evolution | 8 | Dependencia real: Ender Dragon; Chaos Guardian 2000 de vida |
| 13 | Harshen Universe | 4 | Mayormente en prueba |
| 14 | Better With Mods | 14 | Logros oficiales, del cáñamo al Infernal Enchanter |
| 15 | Rustic | 6 | Recetas verificadas |
| 16 | Criaturas de la noche | 4 | Nightmares, SpookyCraft, Re-Zombies, Elemental Creepers |
| 17 | Depredadores y fauna | 3 | Deadly Monsters, ZAWA |
| 18 | Howling Moon | 4 | Sin jefes |
| 19 | Infernal Mobs | 2 | Rarezas de la config; la 2.ª confía en la palabra del jugador |
| 20 | Defensas | 3 | Totem Defender (receta verificada), Mob Totems, SecurityCraft |
| 21 | Grandes expediciones | 4 | Wither, Ender Dragon, Elder Guardian |
| 22 | El poder definitivo | 3 | Draconic final |
| 23 | Maestro de dimensiones | 2 | 12 dimensiones + 7 cavernas |
| 24 | Coleccionista | 4 | Logros difíciles |
| 25 | Arquitecto | 4 | MineColonies, MCA, ThutTech |
| 26 | Desafíos legendarios | 2 | Trilogía de jefes finales |
| 27 | La última expedición | 1 | Opcional, título final |

## Pendientes (marcados §c[en prueba]§r dentro del libro)
1. Betweenlands: de dónde salen las piezas 2 a 4 del talismán.
2. Tropicraft: receta exacta de la Piña Colada y cómo arma el portal la varita.
3. Elemental Dimensions: pasos del Portal Dialer y de dónde sale cada parte 2 de runa.
4. Hunting Dimension: forma y activación del portal.
5. Draconic: en qué dimensiones genera el draconio.
6. Harshen Universe: soul ingot, activación de la puerta a Pontus y si Kazzendre es jefe.
7. Rustic: interacción de los elixires con `HCBrewing`.
8. Recetas de Mob Totems, SecurityCraft, MineColonies, MCA, ThutTech y la guía de ZAWA (se remite a JEI).
9. Nightmares: cómo es la pesadilla. Re-Zombies: chance de la armadura del rey.
10. Texto de las reglas del servidor (cap. 1).
11. Recompensas: son niveles de XP y pocos ítems; ajustarlas con pruebas de juego.

## Lo que no se hizo
- **PV7Core** (clanes, puntos, ranking): queda para su sesión aparte, como estaba acordado.
