from app import crud


def test_integracion_crear_categoria_y_producto(client):
    respuesta_categoria = client.post("/categorias", params={"nombre": "Jardineria"})
    assert respuesta_categoria.status_code == 200
    categoria = respuesta_categoria.json()

    respuesta_producto = client.post(
        "/productos", params={"nombre": "Tijeras", "categoria_id": categoria["id"]}
    )
    assert respuesta_producto.status_code == 200
    producto = respuesta_producto.json()
    assert producto == {"id": 101, "nombre": "Tijeras", "categoria_id": categoria["id"]}
    assert crud.get_categorias() == [categoria]
    assert crud.get_productos() == [producto]


def test_integracion_categoria_inexistente_no_guarda_producto(client):
    respuesta = client.post("/productos", params={"nombre": "Laptop", "categoria_id": 99})

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Categoría no encontrada"}
    assert crud.get_categorias() == []
    assert crud.get_productos() == []
