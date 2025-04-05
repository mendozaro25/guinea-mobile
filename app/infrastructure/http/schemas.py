from typing import Optional, List, Union
import datetime
from pydantic import BaseModel

# Esquemas de usuario
class UserBase(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = False

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class Response(BaseModel):
    data: Optional[Union[UserResponse, 'PermisoResponse', List[UserResponse]]] = None  # Referencia hacia PermisoResponse
    message: str
    id: int  # 1 para éxito, 0 para error

class ListResponse(BaseModel):
    data: List[UserResponse]
    message: str
    id: int

# Esquemas de permisos
class ColaboradorResponse(BaseModel):
    id: int
    nombre: str

class TipoPermisoResponse(BaseModel):
    id: int
    descripcion: str

class PermisoCreate(BaseModel):
    id_colaborador: int
    id_tipo_permiso: int
    fecha_inicio: datetime.datetime
    fecha_fin: datetime.datetime

    class Config:
        arbitrary_types_allowed = True

class PermisoResponse(BaseModel):
    id: int
    colaborador: ColaboradorResponse  # Cambiado a tipo ColaboradorResponse
    tipo_permiso: TipoPermisoResponse  # Cambiado a tipo TipoPermisoResponse
    fecha_inicio: str
    fecha_fin: str

    class Config:
        arbitrary_types_allowed = True

class PermisoListResponse(BaseModel):
    data: List[PermisoResponse]
    message: str
    id: int

    class Config:
        arbitrary_types_allowed = True
