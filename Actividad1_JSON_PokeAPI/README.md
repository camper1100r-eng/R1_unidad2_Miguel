# Actividad 1 — Análisis JSON con PokéAPI (5 puntos)

Ejecuta `py -m pip install requests` y luego `py analisis_json.py` dentro de esta carpeta. El programa sigue la propiedad `next` hasta terminar el listado; descarga detalles, aplana JSON con recursión propia, maneja nulos, valida esquema y calcula estadísticas con `collections` e `itertools`. Genera `estadisticas.json` (no se incluye sin ejecución real).

Para capturas en PowerShell:

```powershell
curl.exe -i "https://pokeapi.co/api/v2/pokemon/?limit=5&offset=0"
curl.exe -i "https://pokeapi.co/api/v2/pokemon/pikachu/"
curl.exe -i "https://pokeapi.co/api/v2/pokemon/no-existe-123456/"
```

Documenta autenticación, paginación, código HTTP, Content-Type y presencia **o ausencia** de Link y X-RateLimit. Revisa https://pokeapi.co/docs/v2 y agrega capturas reales fechadas al PDF que solicita la rúbrica.

Archivo `Actividad 1.docx`: plantilla de reporte; `estadisticas.json` se sustituye al correr el analizador.
