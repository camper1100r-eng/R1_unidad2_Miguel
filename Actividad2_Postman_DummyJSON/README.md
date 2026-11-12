# Actividad 2 — Postman DummyJSON
Archivos con los mismos nombres que el repositorio de referencia: `coleccion.json`, `entorno.json`, `reporte.html` y `Evidencias_Actividad2.odt`.

Importa colección y entorno en Postman, ejecuta las solicitudes en orden y comprueba sus tests. Usa credenciales de práctica vigentes y nunca publiques tus tokens.

Para generar el reporte real (requiere Node.js):
```
npm install -g newman newman-reporter-htmlextra
newman run coleccion.json -e entorno.json -r htmlextra --reporter-htmlextra-export reporte.html
```
`reporte.html` incluido es SOLO un marcador; debe reemplazarse con el resultado real.
