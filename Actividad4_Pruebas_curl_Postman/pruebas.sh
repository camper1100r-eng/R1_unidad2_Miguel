#!/usr/bin/env bash
# Actividad 4. Ejecutar en Git Bash o Linux: bash pruebas.sh
BASE=http://127.0.0.1:5000
curl -i -X POST "$BASE/categorias" -H 'Content-Type: application/json' -d '{"nombre":"Electronica"}'
curl -i -X POST "$BASE/categorias" -H 'Content-Type: application/json' -d '{"nombre":"Ropa"}'
curl -i "$BASE/categorias?page=1&per_page=5&sort=nombre"
curl -i "$BASE/categorias/1"
curl -i -X PUT "$BASE/categorias/2" -H 'Content-Type: application/json' -d '{"nombre":"Accesorios"}'
curl -i -X POST "$BASE/productos" -H 'Content-Type: application/json' -d '{"nombre":"Teclado","precio":250,"stock":5,"categoria_id":1}'
curl -i -X POST "$BASE/productos" -H 'Content-Type: application/json' -d '{"nombre":"Mouse","precio":150,"stock":8,"categoria_id":1}'
curl -i "$BASE/productos?categoria_id=1&page=1&per_page=5&sort=-precio"
curl -i "$BASE/productos/1"
curl -i -X PUT "$BASE/productos/2" -H 'Content-Type: application/json' -d '{"nombre":"Mouse optico","precio":180,"stock":8,"categoria_id":1}'
curl -i -X POST "$BASE/productos/1/salidas" -H 'Content-Type: application/json' -d '{"cantidad":2}'
curl -i -X POST "$BASE/productos/1/salidas" -H 'Content-Type: application/json' -d '{"cantidad":999}'
curl -i -X POST "$BASE/productos" -H 'Content-Type: application/json' -d '{"nombre":"Invalido","precio":-1,"stock":1,"categoria_id":1}'
curl -i -X POST "$BASE/productos" -H 'Content-Type: application/json' -d '{mal json'
curl -i "$BASE/productos/999999"
curl -s -o /dev/null -w 'Codigo HTTP: %{http_code}\n' "$BASE/productos?page=1&per_page=5"
curl -i -X DELETE "$BASE/productos/2"
curl -i -X DELETE "$BASE/categorias/2"
