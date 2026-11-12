# Actividad 3 — Inventario REST con Flask (5 puntos)

En esta carpeta:

```powershell
py -m pip install -r requirements.txt
py app.py
```

`app.py` crea automáticamente `inventario.db` con SQLite. Recursos relacionados: categorías y productos.

| Método | Endpoint | Descripción |
|---|---|---|
| GET, POST | `/categorias` | Listar/crear categorías |
| GET, PUT, DELETE | `/categorias/<id>` | Consultar/editar/borrar categoría |
| GET, POST | `/productos` | Listar/crear productos |
| GET, PUT, DELETE | `/productos/<id>` | Consultar/editar/borrar producto |
| POST | `/productos/<id>/salidas` | Descontar stock; 409 si excede disponible |

Ejemplo JSON para crear categoría: `{"nombre":"Electrónica"}`; crear producto: `{"nombre":"Teclado","precio":250,"stock":5,"categoria_id":1}`; salida: `{"cantidad":2}`.

Filtra, ordena y pagina con `/productos?categoria_id=1&page=1&per_page=5&sort=-precio`.

Los errores siguen la estructura `{"error":{"codigo":422,"mensaje":"...","detalle":["..."]}}` para 400/404/405/409/422 según corresponda. Registra al menos ocho **commits reales** para cumplir la entrega.
