from copy import deepcopy

_datos = {"categorias": [], "productos": []}


def _load_db():
    return deepcopy(_datos)


def _save_db(datos):
    global _datos
    _datos = deepcopy(datos)


def get_categorias():
    return _load_db()["categorias"]


def get_productos():
    return _load_db()["productos"]


def create_categoria_db(nombre):
    datos = _load_db()
    nuevo_id = max([c["id"] for c in datos["categorias"]] or [0]) + 1
    categoria = {"id": nuevo_id, "nombre": nombre}
    datos["categorias"].append(categoria)
    _save_db(datos)
    return categoria


def create_producto_db(nombre, categoria_id):
    datos = _load_db()
    if not any(c["id"] == categoria_id for c in datos["categorias"]):
        return {"error": "Categoría no encontrada"}

    nuevo_id = max([p["id"] for p in datos["productos"]] or [100]) + 1
    producto = {"id": nuevo_id, "nombre": nombre, "categoria_id": categoria_id}
    datos["productos"].append(producto)
    _save_db(datos)
    return producto
