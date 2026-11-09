# Pruebas automatizadas

Dos ejemplos de backend con datos en memoria. Al reiniciar cada servidor se pierde la informacion.

## FastAPI

API de categorias y productos en la carpeta `app`.

```powershell
python -m venv .venv
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe -m uvicorn app.main:app --port 8005
```

La documentacion de las rutas esta en http://127.0.0.1:8005/docs.

```powershell
./.venv/Scripts/python.exe -m pytest -v
```

| Tipo | Cantidad | Que verifica |
| --- | --- | --- |
| Unitaria | 2 | ID incremental de categoria y rechazo de producto sin categoria |
| Integracion | 2 | API, logica y almacenamiento en memoria; respuesta 404 sin guardar datos |
| E2E | 2 | Crear y listar categorias; rechazar y luego crear y consultar un producto |

Las unitarias usan mocks. Las de integracion usan TestClient con datos nuevos por prueba. Las E2E levantan Uvicorn en otro proceso y envian solicitudes HTTP reales.

El archivo `app/db.json` queda como referencia del ejemplo original; la aplicacion ya no lo usa.

## Express

API de mascotas en `backend-express`. Requiere Node 22 o superior.

```powershell
cd backend-express
npm ci
npm start
```

Rutas: `GET /mascotas`, `GET /mascotas/:id` y `POST /mascotas`. El POST recibe un JSON con `nombre` y `especie`.

```powershell
npm test
```

| Tipo | Cantidad | Que verifica |
| --- | --- | --- |
| Unitaria | 1 | Crear una mascota normalizando espacios |
| Integracion | 1 | Ruta Express, validacion y almacenamiento: no guardar una mascota incompleta |
| E2E | 1 | Servidor en otro proceso: registrar, consultar por ID y listar una mascota por HTTP |

## GitHub Actions

El workflow `pruebas-dev.yml` ejecuta ambos proyectos al subir cambios a `dev`. Cada tipo de prueba aparece en un paso separado. Los reportes XML de Python quedan como artefacto de la ejecucion.
