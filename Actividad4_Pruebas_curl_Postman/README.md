# Actividad 4 — Pruebas de inventario Flask
Los nombres coinciden con el ejemplo: `coleccion_flask.json`, `entorno_flask.json`, `pruebas.sh`, `salida.txt` y `Actividad4_Reporte.docx`.

Antes de probar, inicia Flask desde la carpeta de Actividad 3. Importa la colección y entorno en Postman.
En Git Bash o WSL:
```
bash pruebas.sh | tee salida.txt
```
En Windows PowerShell puedes ejecutar las mismas solicitudes desde Postman; para el script usa Git Bash o WSL.

Newman:
```
newman run coleccion_flask.json -e entorno_flask.json -r htmlextra --reporter-htmlextra-export reporte_flask.html
```
La salida.txt incluida es un marcador que debe reemplazarse con una ejecución real; la prueba cruzada necesita un compañero.
