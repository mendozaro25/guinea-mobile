from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Colaborador(BaseModel):
    id: Optional[int] = None
    nombre: str

class TipoPermiso(BaseModel):
    id: Optional[int] = None
    descripcion: str

class Permiso(BaseModel):
    id: Optional[int] = None
    id_colaborador: int
    id_tipo_permiso: int
    fecha_inicio: datetime
    fecha_fin: datetime

    def __str__(self):
        return (f"Permiso(id={self.id}, "
                f"id_colaborador={self.id_colaborador}, "
                f"id_tipo_permiso={self.id_tipo_permiso}, "
                f"fecha_inicio={self.fecha_inicio}, "
                f"fecha_fin={self.fecha_fin})")