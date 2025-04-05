from fastapi import FastAPI
from app.config import API_PREFIX 
from app.infrastructure.http.auth_controller import router as auth_router

app = FastAPI(title="Guinea Mobile API", openapi_url=f"{API_PREFIX}/openapi.json")

# Registrar el router de autenticación
app.include_router(auth_router, prefix=f"{API_PREFIX}/auth")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.18.139", port=8000, reload=True)
