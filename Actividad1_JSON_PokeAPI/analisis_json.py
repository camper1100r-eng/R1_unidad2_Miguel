"""Actividad 1 - PokéAPI. Python 3.10+; pip install requests."""
import json
import os
import time
from collections import Counter, defaultdict
from itertools import chain
from pathlib import Path

import requests

BASE = 'https://pokeapi.co/api/v2/pokemon/'
CARPETA = Path('cache_pokemon')
CARPETA.mkdir(exist_ok=True)
SESION = requests.Session()
SESION.headers.update({'Accept': 'application/json', 'User-Agent': 'ProyectoAcademicoPokemon/1.0'})


def obtener(url):
    nombre = url.rstrip('/').split('/')[-1].split('?')[0]
    # Cache simple por URL completa; evita solicitudes repetidas a la API.
    import hashlib
    archivo = CARPETA / (hashlib.sha256(url.encode()).hexdigest() + '.json')
    if archivo.exists():
        return json.loads(archivo.read_text(encoding='utf-8'))
    respuesta = SESION.get(url, timeout=30)
    respuesta.raise_for_status()
    datos = respuesta.json()
    archivo.write_text(json.dumps(datos, ensure_ascii=False), encoding='utf-8')
    time.sleep(0.12)
    return datos


def aplanar(objeto, prefijo=''):
    resultado = {}
    if isinstance(objeto, dict):
        for clave, valor in objeto.items():
            resultado.update(aplanar(valor, f'{prefijo}.{clave}' if prefijo else str(clave)))
    elif isinstance(objeto, list):
        for indice, valor in enumerate(objeto):
            resultado.update(aplanar(valor, f'{prefijo}.{indice}' if prefijo else str(indice)))
    else:
        resultado[prefijo] = objeto
    return resultado


def validar_pokemon(dato):
    reglas = {'id': int, 'name': str, 'height': int, 'weight': int, 'types': list}
    errores = []
    if not isinstance(dato, dict):
        return ['El detalle no es un objeto JSON']
    for campo, tipo in reglas.items():
        if campo not in dato or dato[campo] is None:
            errores.append(f'{campo}: ausente o null')
        elif not isinstance(dato[campo], tipo):
            errores.append(f'{campo}: debería ser {tipo.__name__}')
    for tipo in dato.get('types') or []:
        if not isinstance(tipo, dict) or not isinstance(tipo.get('type'), dict) or not isinstance(tipo['type'].get('name'), str):
            errores.append('types: entrada inválida')
    return errores


def ejecutar():
    url = BASE + '?limit=100&offset=0'
    nombres = []
    paginas = 0
    while url:
        datos = obtener(url)
        if not isinstance(datos.get('results'), list):
            raise ValueError('Lista de resultados inválida')
        nombres.extend(datos['results'])
        paginas += 1
        url = datos.get('next')
        print(f'Páginas: {paginas} | Pokémon listados: {len(nombres)}', flush=True)

    validos = []
    errores = {}
    ejemplo_aplanado = None
    for indice, recurso in enumerate(nombres, 1):
        try:
            detalle = obtener(recurso['url'])
            fallo = validar_pokemon(detalle)
            if fallo:
                errores[recurso.get('name', str(indice))] = fallo
                continue
            validos.append(detalle)
            if ejemplo_aplanado is None:
                ejemplo_aplanado = aplanar({'pokemon': {'name': detalle.get('name'), 'types': detalle.get('types')}})
        except (requests.RequestException, KeyError, ValueError) as exc:
            errores[recurso.get('name', str(indice))] = [str(exc)]
        if indice % 100 == 0:
            print(f'Detalles procesados: {indice}/{len(nombres)}', flush=True)

    tipos = Counter(chain.from_iterable(
    [
        tipo.get('type', {}).get('name', 'desconocido')
        for tipo in (pokemon.get('types') or [])
    ]
    for pokemon in validos
))
    por_tipo = defaultdict(list)
    for pokemon in validos:
        for tipo in pokemon.get('types') or []:
            nombre_tipo = tipo.get('type', {}).get('name', 'desconocido')
            por_tipo[nombre_tipo].append(pokemon.get('weight', 0))
    pesos = [p['weight'] for p in validos]
    alturas = [p['height'] for p in validos]
    estadisticas = {
        'pokemon_listados': len(nombres), 'paginas_recorridas': paginas,
        'pokemon_validos': len(validos), 'pokemon_con_error': len(errores),
        'conteo_por_tipo': dict(sorted(tipos.items())),
        'peso_promedio': round(sum(pesos) / len(pesos), 2) if pesos else None,
        'peso_minimo': min(pesos) if pesos else None,
        'peso_maximo': max(pesos) if pesos else None,
        'altura_promedio': round(sum(alturas) / len(alturas), 2) if alturas else None,
        'altura_minima': min(alturas) if alturas else None,
        'altura_maxima': max(alturas) if alturas else None,
        'peso_promedio_por_tipo': {k: round(sum(v) / len(v), 2) for k, v in sorted(por_tipo.items())},
        'errores_validacion': errores,
        'ejemplo_aplanado': ejemplo_aplanado,
    }
    Path('estadisticas.json').write_text(json.dumps(estadisticas, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Archivo creado: estadisticas.json')

if __name__ == '__main__':
    ejecutar()
