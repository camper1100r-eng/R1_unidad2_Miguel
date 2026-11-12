# R1U2 — Estudiante 3 (PokéAPI e Inventario Flask)

Estructura de carpetas y **nombres de archivos** adaptados al ZIP `R1U2-main.zip` compartido como referencia. El código corresponde al tema 3 y no reutiliza las evidencias ni los resultados del ejemplo.

## Actividad 1 — PokéAPI
- `Actividad1_JSON_PokeAPI/Actividad 1.docx`: informe con espacios para evidencias.
- `Actividad1_JSON_PokeAPI/analisis_json.py`: recorre páginas y consulta detalles, aplana JSON, valida y calcula estadísticas.
- `Actividad1_JSON_PokeAPI/estadisticas.json`: marcador hasta ejecutar Python.

```
cd Actividad1_JSON_PokeAPI
py -m pip install requests
py analisis_json.py
```

## Actividad 2 — Postman DummyJSON
- `coleccion.json`, `entorno.json` para importar a Postman.
- `Evidencias_Actividad2.odt`: plantilla de evidencias.
- `reporte.html`: marcador, se debe reemplazar mediante Newman.

## Actividad 3 — Flask inventario
La carpeta estaba vacía en la referencia. Aquí sí contiene `app.py`, `requirements.txt`, `README.md` y SQLite se crea al iniciarse.

```
cd Actividad3_Servidor_Flask
py -m pip install -r requirements.txt
py app.py
```
API en http://127.0.0.1:5000. CRUD de categorías y productos, filtros, paginación y `POST /productos/<id>/salidas`; responde 409 cuando el stock no alcanza.

## Actividad 4 — Pruebas
- `pruebas.sh`, `coleccion_flask.json`, `entorno_flask.json`, `salida.txt` y `Actividad4_Reporte.docx`.
- `salida.txt` es un marcador, reemplázalo ejecutando curl.
- Genera reporte real de Newman y realiza prueba cruzada con un compañero.

## Avisos
Las estadísticas del ejemplo no son tus resultados. Los marcadores no son evidencias auténticas; ejecuta las pruebas y captura fecha y hora. Debes hacer al menos 8 commits propios y generar el PDF solicitado para la Actividad 1 a partir del informe.
