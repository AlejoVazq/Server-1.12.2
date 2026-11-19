# ArreMods — Servidor Forge 1.12.2

Configuración, mundo, libro de misiones y herramientas propias del servidor ArreMods.

## Qué hay en el repo
| Carpeta / archivo | Contenido |
|---|---|
| `config/` | Configuración de todos los mods |
| `world/` | El mundo, **sin** datos de jugadores (inventarios, estadísticas, progreso del libro) |
| `pv7-docs/` | Documentación, libro de misiones (`ArreMods_misiones.json`) y generadores en `herramientas/` |
| `para-el-cliente/` | Instrucciones para los jugadores |
| `MODS.md` | Lista de los mods con su versión y hash SHA-256 |
| `server.properties`, `iniciar.bat` | Arranque del servidor |

## Qué no está (a propósito)
- Los JAR de Forge, Minecraft y los mods: son de otros autores. Se reponen con `MODS.md`.
- Logs, copias de seguridad, listas de jugadores (`ops`, `whitelist`, `usercache`) y datos de cada jugador.

## Forge
`forge-1.12.2-14.23.5.2768-universal.jar` (Java 8).
