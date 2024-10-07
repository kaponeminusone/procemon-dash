from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.api.routes import router_api  # Importa el enrutador central que agrupa todas las rutas

app = FastAPI(title="ProcemonAPI")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/favicon.ico")  # Ajusta la ruta según tu estructura

# Incluir todas las rutas centralizadas en router_api
app.include_router(router_api)

# Ruta de prueba para la raíz
@app.get("/")
async def root():
    return {"message": "Welcome to ProcemonDash API"}
