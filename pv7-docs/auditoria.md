# Auditoría del servidor Minecraft 1.12.2 (Forge)

- **Fecha:** 2026-11-19
- **Copia auditada:** `%USERPROFILE%\ServidorMinecraft-1.12.2`
- **Modo:** solo lectura. No se modificó, movió ni ejecutó nada del servidor. El único archivo creado es este.

## Leyenda

| Marca | Significado |
|---|---|
| **Verificado** | Comprobado directamente en archivos de esta copia: jars (`mcmod.info`, anotaciones `@Mod`, clases), `logs/latest.log`, `logs/debug.log`, `config/`, `world/level.dat`. |
| **Documentado** | Viene de la documentación o del comportamiento conocido del mod o de Forge. No se comprobó en estos archivos. |
| **Pendiente** | No se puede confirmar sin abrir el juego, sin probarlo en partida o sin más información. |

## Fuentes usadas

| Fuente | Qué contiene |
|---|---|
| `logs/latest.log` / `logs/debug.log` | Ejecución de 02:10:30 a 02:13:41. Arranque correcto en 11,7 s; entró un jugador y el servidor se detuvo de forma normal. |
| `crash-reports/crash-2026-11-19_02.07.13-server.txt` | Ejecución **anterior**. Se cayó por el mod `noel`, que ahora está en `mods-desactivados/`. |
| `consola.txt` | Ejecución intermedia (02:08 a 02:09). Solo se usó como contexto. |
| `world/level.dat` | Copia de los registros de Forge (`FML > Registries > minecraft:entities`). Se leyó para confirmar los IDs de entidades. |

---

## 1. Mods: versión y dependencias

### Resumen

| Dato | Valor | Estado |
|---|---|---|
| Entradas en `mods/` | 93: 91 jars y 2 carpetas (`memory_repo/`, `bookworm animator/`) | Verificado |
| Mods que cargó FML | **101** contenedores (`Forge Mod Loader has successfully loaded 101 mods`). Incluye minecraft/mcp/FML/forge, mods embebidos y submódulos | Verificado |
| Requisitos de dependencias | `All mod requirements are satisfied` (debug.log, línea 1665) | Verificado |
| Mods solo de cliente, no cargados en el servidor | `BetterThanLlamas-1.12.1-1.0.0.jar`, `JustEnoughResources-1.12.2-0.8.7.41.jar`, `jeiintegration_1.12.2-1.5.1.36.jar`. Los tres declaran `clientSideOnly` y no aparecen entre los mods cargados | Verificado |
| Mod desactivado | `mods-desactivados/noel-1.12.2-1.0.2.jar`. Causó el crash de 02:07 (`NoClassDefFoundError: net/minecraft/client/renderer/entity/Render`, es decir, usa código de cliente en el servidor) | Verificado |
| Submódulos de Dark Roleplay | Están embebidos en `drpcore` y `drpmedieval` y se extraen a `mods/memory_repo/` | Verificado |
| Biblioteca embebida de Betweenlands | `memory_repo/angrypixel/TheBetweenlands/3.4.1/…-core.jar` | Verificado |

### Tabla de mods cargados

La versión es la que informa FML en `debug.log`. Si no coincide con el nombre del jar, la columna lo indica con ⚠.

Dependencias: **obl.** = obligatoria (`required-*` en `@Mod` o `requiredMods` en `mcmod.info`). Las dependencias de solo orden (`after:` o `before:`) se listan solo cuando el mod relacionado está instalado. Todo lo de esta tabla está **Verificado**.

| # | Jar | modid | Versión (FML) | Dependencias |
|---|---|---|---|---|
| 1 | `[1.12.2]+SecurityCraft+v1.8.9.jar` | securitycraft | v1.8.9 | obl. forge ≥14.23.3.2694 |
| 2 | `Baubles-1.12-1.5.2.jar` | baubles | 1.5.2 | obl. forge ≥14.21.0.2348 |
| 3 | `astralsorcery-1.12.2-1.10.3.jar` | astralsorcery | 1.10.3 | obl. forge ≥14.23.4.2748, **baubles**. Coremod |
| 4 | `backpacks+1.12.2+-+3.5.4.jar` | backpacks16840 | 3.5.4 | ninguna. Coremod |
| 5 | `MCMultiPart-2.5.3.jar` | mcmultipart | 2.5.3 | ninguna |
| 6 | `RedstoneFlux-1.12-2.0.1.2-universal.jar` | redstoneflux | 2.0.1 | ninguna |
| 7 | `sonarcore-1.12.2-5.0.16-16.jar` | sonarcore | 5.0.16 | carga después de mcmultipart y redstoneflux |
| 8 | `bagelsmore-1.12.2-2.0.1.jar` | bagelsmore | 2.0.1 | obl. **sonarcore** ≥5.0.10, **mcmultipart** ≥2.5.1 |
| 9 | `BetterQuesting-3.5.329.jar` | betterquesting | 3.5.329 | ninguna |
| 10 | `BetterWithLib-1.12-1.5.jar` | betterwithlib | `${version}` ⚠ (jar 1.5) | ninguna. Coremod |
| 11 | `BetterWithMods-1.12-2.3.19-1017.jar` | betterwithmods | 1.12-2.3.19-1017 | solo dependencias opcionales de orden; ninguna de ellas está instalada. La anotación **no** declara BetterWithLib como obligatoria |
| 12 | `bibliotheca-1.3.3-1.12.2.jar` | bibliotheca | 1.3.3-1.12.2 | ninguna |
| 13 | `Bookshelf-1.12.2-2.3.568.jar` | bookshelf | 2.3.568 | ninguna |
| 14 | `zawa+-+1.4.0+(1.12.2).jar` | zawa | 1.12.2-1.4.0 | obl. **bookworm** ≥1.12.2-1.0.0 |
| 15 | `bookworm+-+1.0.0+(1.12.2).jar` | bookworm | 1.12.2-1.0.0 | ninguna |
| 16 | `CodeChickenLib-1.12.2-3.2.2.354-universal.jar` | codechickenlib | 3.2.2.354 | obl. forge ≥14.23.4.2718 |
| 17 | `BrandonsCore-1.12.2-2.4.7.189-universal.jar` | brandonscore | 2.4.7 | obl. **codechickenlib** ≥3.2.0, **redstoneflux** |
| 18 | `campfire-1.12-v1.2.jar` | campfire | 1.2 | ninguna |
| 19 | `Cavern_1.12.2-v1.10.6.jar` | cavern | 1.10.6 | ninguna |
| 20 | `Chameleon-1.12-4.1.3.jar` | chameleon | 1.12-4.1.3 | obl. forge ≥14.21.0.2362 |
| 21 | `ChestTransporter-1.12.2-2.8.8.jar` | chesttransporter | 2.8.8 | ninguna |
| 22 | `craftdev-core-1.12.2-2.2.8.jar` | craftdevcore | 2.2.8 | ninguna. Coremod |
| 23 | `CreativeCore_v1.9.35_mc1.12.2.jar` | creativecore | 1.9.9 ⚠ (jar 1.9.35) | ninguna. Coremod |
| 24 | `creature_whisperer_1.0.2.jar` | cw | 1.0.2 | ninguna |
| 25 | `CyclopsCore-1.12.2-0.11.11.jar` | cyclopscore | 0.11.11 | obl. forge ≥14.23.1.2555 |
| 26 | `Deadly+Monsters+1.71.jar` | dmonsters | 1.7 ⚠ (jar 1.71) | ninguna |
| 27 | `disenchanter-[1.12]1.6.jar` | disenchanter | 1.6 | ninguna |
| 28 | `Draconic-Evolution-1.12.2-2.3.17.321-universal.jar` | draconicevolution | 2.3.17 | obl. **brandonscore** ≥2.4.7 |
| 29 | `ElecCore-1.12.2-1.8.434.jar` | eleccore | 1.8.434 | ninguna |
| 30 | `ElementalCreepers-v4.3.3.g5616356.jar` | elementalcreepers | v4.3.3.g5616356 | ninguna (sin `mcmod.info`) |
| 31 | `mcjtylib-1.12-3.0.7.jar` | mcjtylib_ng | 3.0.7 | ninguna |
| 32 | `elementaldimensions-1.12-0.3.1.jar` | elementaldimensions | 0.3.1 | obl. **mcjtylib_ng** ≥3.0.0, **eleccore** ≥1.7.409 |
| 33 | `EnergeticSheep-1.12.2-1.1.3.jar` | energeticsheep | 1.1.3 | obl. forge ≥14.23.1.2555, **cyclopscore** ≥0.10.21 |
| 34 | `fairylights-2.1.5-1.12.2.jar` | fairylights | 2.1.5 | obl. forge ≥14.23.5.2768 |
| 35 | `FenceOverhaul-1.3.4.jar` | fenceoverhaul | 1.3.4 | ninguna |
| 36 | `Floocraft+1.12.2-1.9.3.jar` | ftfloocraft | 1.9.3 | `mcmod.info` lista `mirage`, que no está instalado. FML no lo exige y el mod cargó |
| 37 | `foamfix-0.10.3-1.12.2.jar` | foamfix | 0.10.3-1.12.2 | obl. forge ≥14.23.3.2673. Coremod |
| 38 | `jei_1.12.2-4.13.1.225.jar` | jei | 4.13.1.225 | obl. forge ≥14.23.1.2594 |
| 39 | `FTBLib-5.4.7.2.jar` | ftblib | 5.4.7.2 | obl. forge ≥**14.23.5.2768**. Carga después de jei |
| 40 | `FTBUtilities-5.4.1.131.jar` | ftbutilities | 5.4.1.131 | obl. **ftblib** ≥5.4.7.1 |
| 41 | `Gargoyles+mod+1.12.2+patch+1.jar` | gargoyles | 1 | ninguna |
| 42 | `mobtotems-1.12.1-0.3.0.jar` | mobtotems | 1.12.1-0.3.0 | carga antes de guideapi. Incluye su propia copia de `Baubles\|API` |
| 43 | `Guide-API-1.12-2.1.8-63.jar` | guideapi | 1.12-2.1.8-63 | ninguna |
| 44 | `Hammer+Time-2.2.0-1.12.2.jar` | hammertime | 2.2.0 | obl. **bibliotheca** ≥1.1.1-1.12.2 |
| 45 | `HarshenUniverse-0.22.12.jar` | harshenuniverse | 0.22.12 | obl. forge ≥14.23.4.2705 |
| 46 | `howlingmoon-1.12.2-0.9.jar` | howlingmoon | 0.9 | ninguna |
| 47 | `HuntingDimension-1.12.2-1.0.36.jar` | huntingdim | 1.0.36 | obl. **bookshelf** ≥2.3.561 |
| 48 | `Hwyla-1.8.26-B41_1.12.2.jar` | waila | 1.8.26 | ninguna |
| 49 | `InfernalMobs-1.12.2.jar` | infernalmobs | 1.7.5 | `mcmod.info` dice "Forge" y no trae versión |
| 50 | `IronBackpacks-1.12.2-3.0.8-12.jar` | ironbackpacks | 1.12.2-3.0.8-12 | ninguna |
| 51 | `ItemPhysic_Full_1.4.17_mc1.12.2.jar` | itemphysic | 1.4.0 ⚠ (jar 1.4.17) | ninguna. Coremod. Usa CreativeCore |
| 52 | `journeymap-1.12.2-5.5.3.jar` | journeymap | 1.12.2-5.5.3 | obl. forge ≥14.23.5.2768 (`mcmod.info`) |
| 53 | `malisiscore-1.12.2-6.4.0.jar` | malisiscore | 1.12.2-6.4.0 | ninguna. Coremod que además carga Mixin 0.7.4 |
| 54 | `malisisdoors-1.12.2-7.3.0.jar` | malisisdoors | 1.12.2-7.3.0 | obl. **malisiscore** |
| 55 | `RadixCore-1.12.x-2.2.1-universal.jar` | radixcore | 1.12.x-2.2.1 | ninguna |
| 56 | `MCA-1.12.x-5.3.1-universal.jar` | mca | 1.12.2-5.3.1 | obl. **radixcore** ≥1.12.x-2.2.1 |
| 57 | `minecolonies-1.12.2-0.10.53-BETA-universal.jar` | minecolonies | 1.12.2-0.10.53-BETA | ninguna |
| 58 | `moon-core+7.0+(1.12).jar` | moon-core | 7.0 | ninguna |
| 59 | `NaturesCompass-1.12.2-1.5.1.jar` | naturescompass | 1.5.1 | ninguna |
| 60 | `NetherPortalFix_1.12.1-5.3.17.jar` | netherportalfix | 5.3.17 | ninguna |
| 61 | `nice-1.12-0.3.1.jar` | nice | 0.3.1 | obl. **mcjtylib_ng** ≥3.0.0 |
| 62 | `Nightmares-1.12.2-1.0.10.jar` | nightmares | 1.0.10 | obl. **bookshelf** ≥2.2.464 |
| 63 | `NoMoreRecipeConflict-0.12(1.12.2).jar` | recipehandler | 0.12 | ninguna |
| 64 | `NotEnoughItems-1.12.2-2.4.2.240-universal.jar` | nei | 2.4.2 | obl. **codechickenlib** ≥3.2.2, **jei** ≥4.12.0, forge ≥14.23.5.2768 |
| 65 | `paintingselgui-PSG+Revamed-1.12.2-1.1.0.1.jar` | paintingselgui + guilib | `$version` ⚠ (jar 1.1.0.1) | carga después de guilib, que viene en el mismo jar |
| 66 | `questbook-3.1.1-1.12.jar` | questbook | 3.1.1-1.12 | obl. **betterquesting** ≥3.5.242 |
| 67 | `QuickLeafDecay-MC1.12.1-1.2.4.jar` | quickleafdecay | 1.2.4 | ninguna |
| 68 | `Re-Zombies-V1.5-Ver-1.12.2.jar` | rezombiesv15ver1122jar | 1.5 | ninguna |
| 69 | `RikMuldsCore_1.3.1.jar` | corerm | 1.3.1 | obl. forge ≥13.20.1.2386 |
| 70 | `ropebridge-1.12-2.0.7.jar` | ropebridge | 2.0.5 ⚠ (jar 2.0.7) | ninguna |
| 71 | `rustic-1.0.13.jar` | rustic | 1.0.13 | solo opcionales (dynamictrees, que no está instalado) |
| 72 | `SpartanShields-1.12.2-1.4.1.jar` | spartanshields | 1.4.1 | carga después de redstoneflux |
| 73 | `spookycraft-1.12.2-1.0.3.jar` | spookycraft | 1.0.3 | obl. forge ≥14.23.0.2489, **craftdevcore** ≥2.2.8 |
| 74 | `StorageDrawers-1.12.2-5.3.7.jar` | storagedrawers | 1.12-5.3.5 ⚠ (jar 5.3.7) | obl. forge, **chameleon** [4.1.0, 5.0.0) |
| 75 | `structpro-4.0-1.12.1.jar` | structpro | 4.0 | ninguna |
| 76 | `switchbow-1.5.5-1.12.2.jar` | switchbow | 1.5.5 | ninguna (su `mcmod.info` tiene JSON inválido) |
| 77 | `teletoro-1.12.2-26.jar` | teletoro | 1.12.2-26 | ninguna |
| 78 | `TheCampingMod_2.4.2.jar` | camping | 2.4.2 | obl. **corerm** ≥1.3.1 |
| 79 | `thutcore-1.12.2-5.19.9.jar` | thutcore + thutcore_compat | 5.19.9 / 1.0 | ninguna |
| 80 | `thuttech-1.12.2-6.1.5.jar` | thuttech | 6.1.5 | obl. **thutcore** |
| 81 | `tombstone-3.3.0-1.12.jar` | tombstone | 3.3.0 | ninguna |
| 82 | `TotemDefender-1.12.2-2.9.jar` | totemdefender | 2.9 | ninguna |
| 83 | `tropicraft-MC1.12.2-7.1.8.105.jar` | tropicraft | 7.1.8.105 | ninguna |
| 84 | `WaterStrainer-1.12-3.2.0.jar` | waterstrainer | 3.2.0 | ninguna |
| 85 | `Wawla-1.12.2-2.5.264.jar` | wawla | 2.5.264 | ninguna declarada |
| 86 | `drpcore-1.12.2-0.4.6.2.jar` | drpcore (+ drplibrary 0.1.3-pre, drpcmblueprints 1.2.3, drpcmmaarg 0.10.0-SNAPSHOT, drpcmguis 0.0.2-SNAPSHOT) | 1.12.2-0.4.6.2 | los submódulos exigen forge ≥14.23.4.2705 y **drplibrary** |
| 87 | `drpmedieval-1.12.2-0.2.8-pre2.jar` | drpmedieval (+ drpcmlocks 1.0.1) | 1.12.2-0.2.8-pre2 | drpcmlocks exige **drplibrary** |
| 88 | `TheBetweenlands-3.4.1-universal.jar` | thebetweenlands | 3.4.1 | obl. forge ≥14.23.4.2767. Carga después de jei |

**Mods solo de cliente que están en `mods/` pero no se cargan en el servidor (Verificado):**

| Jar | modid | Versión | Dependencia |
|---|---|---|---|
| `BetterThanLlamas-1.12.1-1.0.0.jar` | betterthanllamas | 1.12.1-1.0.0 | forge ≥13.19.0.2141 |
| `JustEnoughResources-1.12.2-0.8.7.41.jar` | jeresources | 0.8.7 | obl. jei ≥4.7.0 |
| `jeiintegration_1.12.2-1.5.1.36.jar` | jeiintegration | 1.5.1.36 | forge ≥14.21.1.2387 |

### Observaciones

- **Configs huérfanas** (Verificado): `config/` tiene archivos de mods que no están instalados, por ejemplo `LagGoggles-*.cfg`, `mobends.cfg`, `ambientsounds.cfg`, `betterfps.json`, `thejungleMod.cfg`, `worldedit/`, `FBP/`, `MM2/` y `T145/`. No hacen daño.
- **Coremods sin firma o sin anotación `MCVersion`** (Verificado, 16 avisos): astralsorcery, backpacks, BetterWithLib, craftdev-core, CreativeCore, foamfix, ItemPhysic y MalisisCore. Es normal en 1.12.2.

---

## 2. BetterQuesting, Quest Book, FTBUtilities y FTBLib

| Mod | ¿Está? | Versión | Evidencia | Estado |
|---|---|---|---|---|
| BetterQuesting | Sí, cargado | 3.5.329 | jar, debug.log y log: `[betterquesting]: Loaded 0 quests / 0 quest lines / 0 parties` | Verificado |
| Quest Book (`questbook`) | Sí, cargado | 3.1.1-1.12 | jar y log `[questbook]: Loading config file.`. Requiere BetterQuesting ≥3.5.242, y se cumple | Verificado |
| FTBUtilities | Sí, cargado | 5.4.1.131 | jar y log: reemplaza el manejador de permisos de Forge por `FTBUtilitiesPermissionHandler` | Verificado |
| FTBLib | Sí, cargado | 5.4.7.2 | jar y log. Requiere Forge ≥14.23.5.2768, y se cumple justo | Verificado |

Detalles:

- **No hay misiones.** `world/betterquesting/QuestDatabase.json` tiene `questDatabase` y `questLines` vacíos, con `hardcore: 0`, `livesdef: 3`, `livesmax: 10` y `party_enable: 1`. Tampoco existe `config/betterquesting/DefaultQuests.json`. **(Verificado)**
- `config/betterquesting/questbook.cfg` tiene `spawnWithBook=false`: los jugadores nuevos no reciben el libro. **(Verificado)**
- Los rangos de FTBUtilities están en `local/ftbutilities/ranks.txt` y `players.txt`. No se revisaron en detalle. **(Pendiente)**
- FTB Quests **no** está instalado. **(Verificado)**

---

## 3. Versión de Forge

| Dato | Valor | Estado |
|---|---|---|
| Forge | **14.23.5.2768** para Minecraft 1.12.2 (`forge-1.12.2-14.23.5.2768-universal.jar` y la línea 4 del log) | Verificado |
| MCP / FML | MCP 9.42 / FML 8.0.99.99 | Verificado (crash report) |
| Java | OpenJDK 1.8.0_332 (JRE de CurseForge), según el log | Verificado |
| Arranque | `iniciar.bat`: `-Xms4G -Xmx6G` con G1GC | Verificado |
| Requisito más alto de los mods | 14.23.5.2768 (FTBLib, Fairy Lights, NEI y JourneyMap). La versión instalada lo cumple justo | Verificado |
| Últimas builds de Forge para 1.12.2 | 14.23.5.2859 (recomendada) y 14.23.5.2860. La versión instalada es más vieja | Documentado |
| `config/forge.cfg` | `removeErroringEntities=true` y `removeErroringTileEntities=true`. Por eso el log avisa "USE AT YOUR OWN RISK": el servidor borra entidades que fallan en lugar de crashear | Verificado |

---

## 4. Errores y advertencias de `logs/latest.log`

**Totales (Verificado):** 63 líneas `ERROR`, 0 `FATAL` y 165 `WARN`. El servidor arrancó (`Done (11.674s)!`), aceptó un jugador y se detuvo sin problemas.

### 4.1 Errores (63)

| Cantidad | Mensaje | Causa e impacto | Estado |
|---|---|---|---|
| 56 | `AdvancementManager: Parsing error loading built-in advancement minecraft:recipes/...` → `Unknown recipe` | Son 28 avances de receta vanilla, cargados dos veces: a las 02:11:35 al cargar el mundo y a las 02:11:42, cuando `FTBLib.reloadServer` recarga (se ve en la traza). Las recetas faltantes son herramientas y armadura de diamante, 15 tintes de flores, azúcar, piedra y ladrillo musgosos, y polvo de blaze. | Verificado |
| | | **Causa probable:** Better With Mods borra esas recetas vanilla. En su config están `HCDiamond=true`, `HCBrewing=true` y `MossGeneration=true`, y BWM pasa tintes y azúcar al molino. Solo afecta a los avances que desbloquean recetas, no al juego. | Documentado (no se cruzó receta por receta) |
| 2 | `Parsing error loading recipe betterwithmods:blocks/redstone/detector_rail_stone` y `..._steel` → `Unknown item` | En la config de BWM está `tweaks > DetectorRail=false`. Probablemente los ítems no se registran pero los JSON de receta siguen en el jar. No tiene impacto. | Verificado (config) / Documentado (relación causa-efecto) |
| 1 | `[harshenuniverse]: Forge Config has no such getter for class java.lang.Float` → NPE en `AccessoryConfig.read` | Falla al leer `config/harshenuniverse/Accessories.cfg` durante el preInit. Puede que algún valor de accesorio quede en su valor por defecto o sin cargar. | Verificado (error) / Pendiente (efecto en el juego) |
| 1 | `The mod spookycraft is expecting signature @FINGERPRINT@` | El jar se compiló sin reemplazar el marcador de firma. Es inofensivo. | Verificado |
| 1 | `[ElementalDimensions]: Error registering TESR: …PortalDialerRenderer` | El mod intenta registrar un renderizador de cliente en el servidor dedicado. No afecta al servidor. | Verificado (error) / Documentado (inocuo) |
| 1 | `[Waila]: Error registering wrapped plugin from storagedrawers` | Falla el plugin de Hwyla de Storage Drawers. Solo afecta la info que se ve con Hwyla sobre los cajones. | Verificado |
| 1 | `FMLIndexedMessageCodec exception` → `Undefined discriminator for message type journeymap.common.network.DimensionPermissionPacket in channel jm_dim_permission` (02:12:41, al entrar `el administrador`) | JourneyMap no pudo mandarle al cliente el paquete de permisos por dimensión. Suele pasar cuando el cliente no tiene JourneyMap o tiene otra versión. El jugador entró igual. | Verificado (error) / Pendiente (versión de JourneyMap en el cliente) |

### 4.2 Advertencias (165)

| Cantidad | Tipo | Mods | Estado |
|---|---|---|---|
| 103 | `Potentially Dangerous alternative prefix 'minecraft'`: TileEntities registradas sin dominio del mod | betterwithmods 40, bagelsmore 14, malisisdoors 11, harshenuniverse 11, camping 8, tropicraft 7, switchbow 2, mca 2, disenchanter 2 y otros sueltos | Verificado. Es habitual en mods de 1.12 y no tiene impacto inmediato |
| 20 | `Missing English translation` | FML, betterwithlib, bibliotheca, chameleon, codechickenlib, foamfix, mcjtylib_ng, mcmultipart, moon-core, guilib, paintingselgui, quickleafdecay, radixcore, redstoneflux, corerm, structpro, thutcore_compat y drp* | Verificado. Solo cosmético |
| 16 | Coremods sin firma, sin `MCVersion` o con `FMLCorePluginContainsFMLMod` | ver sección 1 | Verificado |
| 10 | `No types have been added to Biome tropicraft:*` | tropicraft | Verificado. Forge les asigna tipos de bioma por aproximación |
| 4 | MCA usa inglés en el servidor dedicado (`serverLanguageId`), y `Empty phrase value on line 72. Key value: tile.mca` | mca | Verificado |
| 3 | `Cannot check for updates … PENDING` | craftdevcore ×2, elementalcreepers | Verificado. Sin impacto |
| 2 | `Couldn't find resource table dmonsters:zombiechicken` | Deadly Monsters: falta la tabla de botín del Zombie Chicken, que entonces no suelta nada | Verificado |
| 2 | `Enabling removal of erroring (Tile) Entities` | forge.cfg | Verificado |
| 2 | Reemplazo del manejador de permisos por FTBUtilities | ftblib, ftbutilities | Verificado. Es lo esperado |
| 1 | `A mod has attempted to assign Block Block{null} to the Fluid 'tropicraft.portal'` | tropicraft | Verificado. Puede dejar bloques de fluido duplicados |
| 1 | `codechickenlib is missing the required element 'version'` | codechickenlib | Verificado. Inocuo |
| 1 | `No features were detected for mod: brandonscore` | brandonscore | Verificado. Inocuo |

### 4.3 Historial de crashes

- **02:07:13:** `LoaderExceptionModCrash: Caught exception from Noel Mod (noel)`. Usa clases de cliente en el servidor, y el transformer de CraftDev Core también lanzó una NPE en la cadena de errores. Ya está resuelto porque el mod está en `mods-desactivados/`. **(Verificado)**

---

## 5. Configuraciones relevantes

### 5.1 Better With Mods (`config/betterwithmods.cfg`, un solo archivo de 1173 líneas)

| Ajuste | Valor | Estado |
|---|---|---|
| Módulos `compatmodule`, `gameplay`, `hardcore`, `industry` y `tweaks` | todos `true` | Verificado |
| **Hardcore activados (`true`)** | `HCBeacons`, `HCBrewing`, `HCBuoy`, `HCDiamond`, `HCEnchanting`, `HCEndermen`, `HCInfo`, `HCMobEquipment`, `HCSapling` y `ExplosiveRecipes` | Verificado |
| Hardcore desactivados | todos los demás (`HCSpawn`, `HCHunting`, `HCStrata`, `HCOres`, `HCStructures`, `HCVillages`, `HCTools`, `HCArmor`, `HCBeds`, `HCInjury`, `HCGloom`, `HCLumber`, `HCMovement`, etc. están en `false`) | Verificado |
| Acero | `HarderSteelRecipe=true` (requiere End Slag, que solo se consigue después del End) y `Steel Requires Infernal Enchanter=true` | Verificado |
| Aldeas | `Disable Village Iron Golem Spawns=true` y `Replace Villager Spawning with Nitwits=true` | Verificado |
| Spawn de mobs (tweaks) | `MobSpawning=false` como tweak general, con subopciones `Jungle Spider Spawning`, `Limit Nether/Slime/Witch Spawning` en `true` | Verificado. Pendiente si las subopciones aplican con el tweak desactivado |
| Otros tweaks | `MossGeneration=true`, `SaddleRecipe=true`, `SilverfishClay=true`, `DetectorRail=false`, `FoodPoisoning=false` y `EasyBreeding=false` | Verificado |
| Industria | `Pollution=true` y `WeatherControl=true` | Verificado |
| General | `High Efficiency Recipes=true`, `MechanicalBreakage=true` y `Kid Friendly=false` | Verificado |

### 5.2 Infernal Mobs (`config/infernalmobs.cfg`)

| Ajuste | Valor | Estado |
|---|---|---|
| Probabilidades | `eliteRarity=15`, `ultraRarity=7`, `infernoRarity=7` y `mobHealthFactor=1.0` | Verificado |
| Antigranjas | `AntiMobfarmingEnabled=true`, `AntiMobFarmCheckInterval=30` y `mobFarmDamageThreshold=150.0` | Verificado |
| `maxOneShotDamage` | 10.0 | Verificado |
| `dimensionIDBlackList` | vacío: aplica en todas las dimensiones | Verificado |
| Modificadores `MM_*` | los 27 activados | Verificado |
| Identificación de mobs | `useSimpleEntityClassnames=true`, o sea que usa nombres de clase como `EntityWight` y `EntityDragon`, no IDs de registro | Verificado |
| `entitiesalwaysinfernal` | todos en `false` | Verificado |
| `permittedentities` | todas las entidades listadas en `true`. Incluye `EntityDragon` (vanilla) y mobs de Betweenlands (`EntityWight`, `EntitySwampHag`, `EntityTarBeast`, etc.), ElementalDimensions (`EntityDirtZombie`, `EntityGuard`), Harshen (`EntityHarshenSoul`) y Howling Moon (`EntityHunter`) | Verificado |
| Jefes en la lista | **No aparecen** `EntityFortressBoss`, `EntityDreadfulMummy`, `EntitySpiritTreeFaceLarge`, `EntityChaosGuardian`, las clases `*Boss` de ElementalDimensions, `EntityKazzendre` ni `EntityWerewolf`. Infernal Mobs agrega una entidad a este archivo recién cuando la ve aparecer. | Verificado (ausencia) / Pendiente (comportamiento con jefes) |

### 5.3 Hunting Dimension (`config/huntingdim/huntingdim.cfg` y `world_generator_settings.json`)

| Ajuste | Valor | Estado |
|---|---|---|
| `dimensionId` | **28885**. Se carga al arrancar (`Loading dimension 28885`) y existe `world/DIM28885` | Verificado |
| `returnDimension` | 0 (Overworld) | Verificado |
| Generación | `worldType=default`, `initialBiome=minecraft:plains`, `useVoidWorld=false`, `mimicSurfaceWorld=false`. El JSON tiene parámetros estándar y el log confirma que se leyó | Verificado |
| Mobs | `chanceSpawn=2000`, `allowPeacefulMobs=false`, `mobsInSurface=true`, `buffHealth=0.3`, `buffAttack=0.3` y `buffArmor=4` | Verificado |
| Recompensas | `expChance=0.2`, `expModifier=2.5` y `lootingChance=0.25` | Verificado |
| Otros | `allowRespawn=false` y `quickPotionWearOff=true` | Verificado |

### 5.4 Cavern (`config/cavern/*.cfg`)

| Dimensión | ID | Estado | Ajustes clave |
|---|---|---|---|
| Cavern | -50 | activa | altura 256, `monsterSpawn=200`, `caveBrightness=0.035`, mazmorras y torres activadas |
| Ruins Cavern | -51 | activa | `bonusChest=0.2` y `decorateTorches=true` |
| Aqua Cavern | -52 | activa | brillo 0.075 |
| Caveland | -53 | activa | `monsterSpawn=150` |
| Ice Cavern | -54 | activa | `monsterSpawn=100` |
| Cavenia | -55 | activa | altura 128, `keepInventory=true` y `keepExperiences=true` |
| Huge Cavern | -56 | activa | `monsterSpawn=100` |

- Ninguna dimensión tiene `dimensionDisabled=true`, y existen las carpetas `world/DIM-50` a `DIM-56`. **(Verificado)**
- Configuración general: `portalMenu=true`, `cavernEscapeMission=false`, `miningCombo=true`, `caveborn=0`, `sleepWaitTime=300`, y mining assist con `minerRank=2` y `quickMiningLimit=30`. **(Verificado)**
- Estas dimensiones no se cargan al arrancar, solo cuando entra alguien, y eso es normal. **(Documentado)**
- No hay conflictos de ID con otras dimensiones de mods: Betweenlands 20, Howling Moon 24, Harshen (Pontus) 5, ElementalDimensions 100 a 104, Tropicraft -127, TeleToro 16 y Hunting 28885. **(Verificado)**

### 5.5 Nightmares (`config/nightmares.cfg`)

| Ajuste | Valor | Estado |
|---|---|---|
| `attackChance` | 0.05, que es el valor por defecto: 5 % de probabilidad de pesadilla al dormir | Verificado |
| Otras opciones | el archivo no tiene más ajustes | Verificado |

---

## 6. Entidades de jefes

**Método:**

1. **ID de registro:** se leyó del registro `minecraft:entities` guardado en `world/level.dat`. Es el ID que se usa con `/summon` y en los configs.
2. **Jefe confirmado:** la clase de la entidad usa `net.minecraft.world.BossInfoServer`, es decir, tiene barra de jefe. Se comprobó en el bytecode de cada jar.
3. **Nombre visible:** sale de `assets/<mod>/lang/en_us.lang`.

| Mod | ID de registro | Clase | Nombre visible | ¿Jefe? | Estado |
|---|---|---|---|---|---|
| The Betweenlands 3.4.1 | `thebetweenlands:fortress_boss` | `EntityFortressBoss` | Primordial Malevolence | Sí, con barra de jefe | Verificado |
| | `thebetweenlands:dreadful_mummy` | `EntityDreadfulMummy` | Dreadful Peat Mummy | Sí, con barra de jefe | Verificado |
| | `thebetweenlands:spirit_tree_face_large` | `EntitySpiritTreeFaceLarge` | Large Spirit Tree Face (jefe del Spirit Tree) | Sí, con barra de jefe | Verificado |
| | Auxiliares de Primordial Malevolence: `fortress_boss_turret`, `_projectile`, `_blockade`, `_spawner`, `_teleporter` | — | — | No, son partes o proyectiles del jefe | Verificado |
| Draconic Evolution 2.3.17 | `draconicevolution:chaosguardian` | `EntityChaosGuardian` | Chaos Guardian | Sí, con barra de jefe | Verificado |
| | `draconicevolution:guardiancrystal`, `draconicevolution:guardianprojectile` | — | — | No, son auxiliares del Chaos Guardian | Verificado |
| | El archivo de idioma tiene `entity.draconicevolution:EnderDragon`, pero **no** hay entidad registrada con ese nombre. El dragón es el vanilla `minecraft:ender_dragon` | — | — | — | Verificado |
| Elemental Dimensions 0.3.1 | `elementaldimensions:ed_dirtzombieboss` | `EntityDirtZombieBoss` | Dirt Zombie Boss | Jefe por nombre y diseño. **No** tiene barra de jefe | Verificado (ID y clase) / Documentado (rol de jefe) |
| | `elementaldimensions:ed_watercreepboss` | `EntityWaterCreepBoss` | Water Creep Boss | igual que el anterior | Verificado / Documentado |
| | `elementaldimensions:ed_ghostboss` | `EntityGhostBoss` | Ghost Boss | igual que el anterior | Verificado / Documentado |
| | `elementaldimensions:ed_fireboss` | `EntityFireBoss` | Fire Boss | igual que el anterior | Verificado / Documentado |
| | `ed_waterbossseed`, `ed_airbossseed`, `ed_firebossseed` | `Entity*BossSeed`, que heredan de `EntityItem` | "Boss Seed" | No, son ítems-entidad que invocan al jefe | Verificado (clase) / Documentado (función) |
| Harshen Universe 0.22.12 | `harshenuniverse:kazzendre` | `EntityKazzendre`, que hereda de `EntityMob` | Kazzendre | Probable jefe del mod, pero sin barra de jefe en el código | Verificado (ID) / **Pendiente** (rol de jefe) |
| | `harshenuniverse:harshen_soul`, `soulless_knight`, `soul_shooter`, `soul_part`, `bloody_sheep` | `EntityMob` / `EntityAnimal` | — | No hay evidencia de que sean jefes | Verificado (ID) / Pendiente |
| Howling Moon 0.9 | Registradas: `howlingmoon:entitywerewolf`, `entityhunter`, `entitywerewolfguide`, `entitywolfguide`, `entitywolfspirit`, `entitycarry`, `entitystun` | — | Werewolf, Hunter, … | **Ninguna es jefe.** No hay clases con barra de jefe, y son mobs, NPC o guías | Verificado |

Notas sobre los IDs:

- Draconic y Howling Moon registraron nombres con mayúsculas, como `ChaosGuardian` y `EntityWerewolf`, pero Minecraft 1.12 los guarda en minúsculas. En comandos y configs hay que usar la forma de la tabla. **(Verificado)**
- Infernal Mobs identifica las entidades por nombre de clase (`useSimpleEntityClassnames=true`), así que en su config los jefes aparecerían como `EntityFortressBoss`, `EntityChaosGuardian`, etc. **(Verificado** en la config; **Pendiente** confirmar que los agrega cuando aparecen en el juego)

---

## Pendientes para confirmar en partida

1. Si Infernal Mobs puede convertir a los jefes en infernales y si los agrega a `permittedentities` cuando aparecen.
2. Qué efecto tiene el error de lectura de `harshenuniverse/Accessories.cfg` en los accesorios.
3. Si el rol de jefe de `harshenuniverse:kazzendre` y el comportamiento de los jefes de ElementalDimensions coinciden con lo esperado, ya que ninguno tiene barra de jefe.
4. Qué versión de JourneyMap tiene el cliente, por el error del paquete `jm_dim_permission`.
5. Cuál es el contenido de los rangos de FTBUtilities (`local/ftbutilities/ranks.txt`).
6. Si las subopciones de `mobspawning` de BWM aplican con `MobSpawning=false`.
