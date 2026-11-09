from unittest.mock import patch

from app.crud import create_categoria_db, create_producto_db


def test_unit_crear_categoria_con_id_incremental():
    datos = {
        "categorias": [{"id": 10, "nombre": "Electronica"}, {"id": 3, "nombre": "Hogar"}],
        "productos": [],
    }

    with patch("app.crud._load_db", return_value=datos) as cargar, patch("app.crud._save_db") as guardar:
        resultado = create_categoria_db("Jardineria")

    assert resultado == {"id": 11, "nombre": "Jardineria"}
    cargar.assert_called_once_with()
    guardar.assert_called_once_with({
        "categorias": [
            {"id": 10, "nombre": "Electronica"},
            {"id": 3, "nombre": "Hogar"},
            {"id": 11, "nombre": "Jardineria"},
        ],
        "productos": [],
    })


def test_unit_rechazar_producto_sin_categoria():
    datos = {"categorias": [], "productos": []}

    with patch("app.crud._load_db", return_value=datos) as cargar, patch("app.crud._save_db") as guardar:
        resultado = create_producto_db("Laptop", 99)

    assert resultado == {"error": "Categoría no encontrada"}
    assert datos == {"categorias": [], "productos": []}
    cargar.assert_called_once_with()
    guardar.assert_not_called()
