"""Actividades 3 y 4: API REST de inventario con SQLite."""
import math
import sqlite3
from pathlib import Path
from flask import Flask, jsonify, request, g

app = Flask(__name__)
DB = Path(__file__).with_name('inventario.db')


def db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB, timeout=10)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys=ON')
    return g.db


@app.teardown_appcontext
def cerrar(error=None):
    conexion = g.pop('db', None)
    if conexion:
        conexion.close()


def iniciar():
    with app.app_context():
        db().executescript('''
            CREATE TABLE IF NOT EXISTS categorias (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              nombre TEXT UNIQUE NOT NULL
            );
            CREATE TABLE IF NOT EXISTS productos (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              nombre TEXT NOT NULL,
              precio REAL NOT NULL CHECK(precio>=0),
              stock INTEGER NOT NULL CHECK(stock>=0),
              categoria_id INTEGER NOT NULL REFERENCES categorias(id)
            );
        ''')
        db().commit()


def error(codigo, mensaje, detalle=None):
    return jsonify(error={'codigo': codigo, 'mensaje': mensaje, 'detalle': detalle or []}), codigo


@app.errorhandler(404)
def no_encontrado(e):
    return error(404, 'Recurso no encontrado')


@app.errorhandler(405)
def metodo_invalido(e):
    return error(405, 'Método no permitido')


def json_entrada():
    if not request.is_json:
        return None, error(400, 'Se requiere un cuerpo JSON')
    valor = request.get_json(silent=True)
    if not isinstance(valor, dict):
        return None, error(400, 'JSON ausente, mal formado o no es un objeto')
    return valor, None


def categoria_existe(id):
    return db().execute('SELECT id FROM categorias WHERE id=?', (id,)).fetchone() is not None


def registro(tabla, id):
    return db().execute(f'SELECT * FROM {tabla} WHERE id=?', (id,)).fetchone()


def validar_categoria(data):
    nombre = data.get('nombre')
    if not isinstance(nombre, str) or not nombre.strip():
        return None, error(422, 'Nombre de categoría inválido', ['nombre debe ser texto no vacío'])
    return nombre.strip(), None


def validar_producto(data):
    nombre, precio, stock, cid = (data.get(k) for k in ('nombre', 'precio', 'stock', 'categoria_id'))
    detalles = []
    if not isinstance(nombre, str) or not nombre.strip():
        detalles.append('nombre debe ser texto no vacío')
    if isinstance(precio, bool) or not isinstance(precio, (int, float)) or not math.isfinite(precio) or precio < 0:
        detalles.append('precio debe ser un número no negativo')
    if isinstance(stock, bool) or not isinstance(stock, int) or stock < 0:
        detalles.append('stock debe ser entero no negativo')
    if isinstance(cid, bool) or not isinstance(cid, int) or cid <= 0:
        detalles.append('categoria_id debe ser entero positivo')
    elif not categoria_existe(cid):
        detalles.append('categoria_id no corresponde a una categoría existente')
    return ((nombre.strip(), precio, stock, cid), None) if not detalles else (None, error(422, 'Datos del producto inválidos', detalles))


def lista(tabla, campos_filtro, campos_sort):
    try:
        page = int(request.args.get('page', '1'))
        per_page = int(request.args.get('per_page', '10'))
    except ValueError:
        return error(422, 'Paginación inválida', ['page y per_page deben ser enteros'])
    if page < 1 or not 1 <= per_page <= 100:
        return error(422, 'Paginación inválida', ['page >= 1 y 1 <= per_page <= 100'])
    sort = request.args.get('sort', 'id')
    desc = sort.startswith('-')
    campo = sort.lstrip('-')
    if campo not in campos_sort:
        return error(422, 'Ordenamiento inválido', ['Campo sort no permitido'])
    condiciones, valores = [], []
    for filtro, columna in campos_filtro.items():
        if filtro in request.args:
            val = request.args[filtro]
            if filtro.endswith('_id'):
                try:
                    val = int(val)
                except ValueError:
                    return error(422, 'Filtro inválido', [f'{filtro} debe ser entero'])
            condiciones.append(f'{columna} = ?' if filtro.endswith('_id') else f'{columna} LIKE ?')
            valores.append(val if filtro.endswith('_id') else f'%{val}%')
    where = ' WHERE ' + ' AND '.join(condiciones) if condiciones else ''
    total = db().execute(f'SELECT COUNT(*) FROM {tabla}' + where, valores).fetchone()[0]
    filas = db().execute(f'SELECT * FROM {tabla}' + where + f' ORDER BY {campo} {"DESC" if desc else "ASC"} LIMIT ? OFFSET ?', (*valores, per_page, (page-1)*per_page)).fetchall()
    return jsonify(datos=[dict(x) for x in filas], page=page, per_page=per_page, total=total, total_pages=math.ceil(total/per_page))


@app.get('/categorias')
def categorias():
    return lista('categorias', {'nombre': 'nombre'}, {'id', 'nombre'})


@app.post('/categorias')
def crear_categoria():
    data, fallo = json_entrada()
    if fallo: return fallo
    nombre, fallo = validar_categoria(data)
    if fallo: return fallo
    try:
        cursor = db().execute('INSERT INTO categorias(nombre) VALUES(?)', (nombre,))
        db().commit()
    except sqlite3.IntegrityError:
        return error(409, 'La categoría ya existe')
    return jsonify(dict(registro('categorias', cursor.lastrowid))), 201


@app.get('/categorias/<int:id>')
def ver_categoria(id):
    fila = registro('categorias', id)
    return jsonify(dict(fila)) if fila else error(404, 'Categoría no encontrada')


@app.put('/categorias/<int:id>')
def editar_categoria(id):
    if not registro('categorias', id): return error(404, 'Categoría no encontrada')
    data, fallo = json_entrada()
    if fallo: return fallo
    nombre, fallo = validar_categoria(data)
    if fallo: return fallo
    try:
        db().execute('UPDATE categorias SET nombre=? WHERE id=?', (nombre, id))
        db().commit()
    except sqlite3.IntegrityError:
        return error(409, 'La categoría ya existe')
    return jsonify(dict(registro('categorias', id)))


@app.delete('/categorias/<int:id>')
def eliminar_categoria(id):
    if not registro('categorias', id): return error(404, 'Categoría no encontrada')
    if db().execute('SELECT 1 FROM productos WHERE categoria_id=?', (id,)).fetchone():
        return error(409, 'La categoría tiene productos asociados')
    db().execute('DELETE FROM categorias WHERE id=?', (id,)); db().commit()
    return '', 204


@app.get('/productos')
def productos():
    return lista('productos', {'nombre': 'nombre', 'categoria_id': 'categoria_id'}, {'id', 'nombre', 'precio', 'stock', 'categoria_id'})


@app.post('/productos')
def crear_producto():
    data, fallo = json_entrada()
    if fallo: return fallo
    valores, fallo = validar_producto(data)
    if fallo: return fallo
    cursor = db().execute('INSERT INTO productos(nombre, precio, stock, categoria_id) VALUES(?,?,?,?)', valores)
    db().commit()
    return jsonify(dict(registro('productos', cursor.lastrowid))), 201


@app.get('/productos/<int:id>')
def ver_producto(id):
    fila = registro('productos', id)
    return jsonify(dict(fila)) if fila else error(404, 'Producto no encontrado')


@app.put('/productos/<int:id>')
def editar_producto(id):
    if not registro('productos', id): return error(404, 'Producto no encontrado')
    data, fallo = json_entrada()
    if fallo: return fallo
    valores, fallo = validar_producto(data)
    if fallo: return fallo
    db().execute('UPDATE productos SET nombre=?,precio=?,stock=?,categoria_id=? WHERE id=?', (*valores,id))
    db().commit()
    return jsonify(dict(registro('productos', id)))


@app.delete('/productos/<int:id>')
def eliminar_producto(id):
    if not registro('productos', id): return error(404, 'Producto no encontrado')
    db().execute('DELETE FROM productos WHERE id=?', (id,)); db().commit()
    return '', 204


@app.post('/productos/<int:id>/salidas')
def registrar_salida(id):
    data, fallo = json_entrada()
    if fallo: return fallo
    cantidad = data.get('cantidad')
    if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
        return error(422, 'Cantidad inválida', ['cantidad debe ser entero positivo'])
    # La actualización condicional hace cumplir la regla de negocio incluso ante solicitudes simultáneas.
    cursor = db().execute('UPDATE productos SET stock=stock-? WHERE id=? AND stock>=?', (cantidad, id, cantidad))
    if cursor.rowcount == 0:
        if not registro('productos', id): return error(404, 'Producto no encontrado')
        return error(409, 'Stock insuficiente', ['No se puede registrar una salida mayor al stock disponible'])
    db().commit()
    return jsonify({'mensaje': 'Salida registrada', 'cantidad': cantidad, 'producto': dict(registro('productos', id))})


iniciar()

if __name__ == '__main__':
    app.run(debug=True)
