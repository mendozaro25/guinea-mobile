from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.core.use_cases.permiso_use_cases import PermisoUseCases
from app.infrastructure.database.config import get_db
from app.infrastructure.database.models import ColaboradorDBModel, TipoPermisoDBModel
from app.infrastructure.repositories.permiso_repository_impl import PermisoRepositoryImpl
from app.infrastructure.http.schemas import ColaboradorResponse, ListResponse, PermisoCreate, Response, PermisoResponse, PermisoListResponse, TipoPermisoResponse
from app.core.utils import verify_token
from app.config import API_PREFIX
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix=f"{API_PREFIX}/permission")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_permiso_use_cases(db: Session = Depends(get_db)) -> PermisoUseCases:
    permiso_repo = PermisoRepositoryImpl(db)
    return PermisoUseCases(permiso_repo=permiso_repo)

def get_current_permiso(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = verify_token(token)
        return payload.get("sub")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"{str(e)}")

@router.post("/register", response_model=Response)
async def register_permiso(
    permiso: PermisoCreate,
    use_cases: PermisoUseCases = Depends(get_permiso_use_cases),
    current_permiso: str = Depends(get_current_permiso),
    db: Session = Depends(get_db)
):
    try:
        new_permiso = use_cases.create_permiso(permiso, db)
        
        colaborador = db.query(ColaboradorDBModel).filter(ColaboradorDBModel.id == new_permiso.id_colaborador).first()
        if not colaborador:
            raise HTTPException(status_code=404, detail="Colaborador not found")
        
        tipopermiso = db.query(TipoPermisoDBModel).filter(TipoPermisoDBModel.id == new_permiso.id_tipopermiso).first()
        if not tipopermiso:
            raise HTTPException(status_code=404, detail="Type permission not found")
        
        colaborador_response = ColaboradorResponse(id=colaborador.id, nombre=colaborador.nombre)
        tipo_permiso_response = TipoPermisoResponse(id=tipopermiso.id, descripcion=tipopermiso.descripcion)

        permiso_response = PermisoResponse(
            id=new_permiso.id,
            colaborador=colaborador_response,
            tipo_permiso=tipo_permiso_response,
            fecha_inicio=new_permiso.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
            fecha_fin=new_permiso.fecha_fin.strftime('%Y-%m-%d %H:%M:%S')
        )

        return Response(id=1, data=permiso_response, message="Permission registered successfully")
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=f"Validation error: {ve}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create permiso: {str(e)}")

@router.get("/list", response_model=PermisoListResponse)
def list_permisos(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),  # Inyección de la sesión de la base de datos
    use_cases: PermisoUseCases = Depends(get_permiso_use_cases),
    current_permiso: str = Depends(get_current_permiso)  # Verificación de token aquí
):
    # Obtener permisos usando el caso de uso
    permisos = use_cases.list_permisos(skip=skip, limit=limit)

    permiso_responses = []

    for permiso in permisos:
        # Consultar al colaborador
        colaborador = db.query(ColaboradorDBModel).filter(ColaboradorDBModel.id == permiso.id_colaborador).first()
        if not colaborador:
            raise HTTPException(status_code=404, detail="Colaborador not found")

        # Consultar el tipo de permiso
        tipopermiso = db.query(TipoPermisoDBModel).filter(TipoPermisoDBModel.id == permiso.id_tipo_permiso).first()
        if not tipopermiso:
            raise HTTPException(status_code=404, detail="Type permission not found")

        # Crear las respuestas para colaborador y tipo de permiso
        colaborador_response = ColaboradorResponse(id=colaborador.id, nombre=colaborador.nombre)
        tipo_permiso_response = TipoPermisoResponse(id=tipopermiso.id, descripcion=tipopermiso.descripcion)

        # Crear la respuesta de permiso
        permiso_response = PermisoResponse(
            id=permiso.id,
            colaborador=colaborador_response,
            tipo_permiso=tipo_permiso_response,
            fecha_inicio=permiso.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
            fecha_fin=permiso.fecha_fin.strftime('%Y-%m-%d %H:%M:%S')
        )

        # Agregar la respuesta a la lista
        permiso_responses.append(permiso_response)

    # Devolver la lista de permisos
    return PermisoListResponse(id=1, data=permiso_responses, message="Permissions retrieved successfully")
    
@router.get("/{permiso_id}", response_model=Response)
def read_permiso(
    permiso_id: int,
    use_cases: PermisoUseCases = Depends(get_permiso_use_cases),
    db: Session = Depends(get_db),
    current_permiso: str = Depends(get_current_permiso)
):
    permiso = use_cases.get_permiso(permiso_id)
    if permiso is None:
        return Response(id=0, data=None, message="Permission not found")
    
    tipopermiso = db.query(TipoPermisoDBModel).filter(TipoPermisoDBModel.id == permiso.id_tipo_permiso).first()
    if not tipopermiso:
        raise HTTPException(status_code=404, detail="Type permission not found")
    
    colaborador = db.query(ColaboradorDBModel).filter(ColaboradorDBModel.id == permiso.id_colaborador).first()
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador not found")
    
    colaborador_response = ColaboradorResponse(id=colaborador.id, nombre=colaborador.nombre)
    tipo_permiso_response = TipoPermisoResponse(id=tipopermiso.id, descripcion=tipopermiso.descripcion)
    
    permiso_response = PermisoResponse(
        id=permiso.id,
        colaborador=colaborador_response,
        tipo_permiso=tipo_permiso_response, 
        fecha_inicio=permiso.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
        fecha_fin=permiso.fecha_fin.strftime('%Y-%m-%d %H:%M:%S')
    )

    return Response(id=1, data=permiso_response, message="Permission found")
