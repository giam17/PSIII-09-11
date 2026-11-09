def test_e2e_crear_y_consultar_categorias(servidor):
    inicial = servidor.get("/categorias")
    assert inicial.status_code == 200
    assert inicial.json() == []

    primera = servidor.post("/categorias", params={"nombre": "Electronica"})
    segunda = servidor.post("/categorias", params={"nombre": "Hogar"})
    assert primera.status_code == 200
    assert segunda.status_code == 200
    assert primera.json() == {"id": 1, "nombre": "Electronica"}
    assert segunda.json() == {"id": 2, "nombre": "Hogar"}

    final = servidor.get("/categorias")
    assert final.status_code == 200
    assert final.json() == [primera.json(), segunda.json()]


def test_e2e_crear_producto_despues_de_un_rechazo(servidor):
    rechazo = servidor.post("/productos", params={"nombre": "Laptop", "categoria_id": 99})
    assert rechazo.status_code == 404
    assert rechazo.json() == {"detail": "Categoría no encontrada"}

    respuesta_categoria = servidor.post("/categorias", params={"nombre": "Electronica"})
    assert respuesta_categoria.status_code == 200
    categoria = respuesta_categoria.json()

    respuesta_producto = servidor.post(
        "/productos", params={"nombre": "Laptop", "categoria_id": categoria["id"]}
    )
    assert respuesta_producto.status_code == 200
    producto = {"id": 101, "nombre": "Laptop", "categoria_id": categoria["id"]}
    assert respuesta_producto.json() == producto

    consulta = servidor.get("/productos")
    assert consulta.status_code == 200
    assert consulta.json() == [producto]
