from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session  # Asegúrate de que esta es la línea correcta
from app.core.entities.permiso import Permiso, TipoPermiso, Colaborador
from app.infrastructure.database.models import ColaboradorDBModel, PermisoDBModel
from app.infrastructure.http.schemas import PermisoCreate
from app.infrastructure.repositories.permiso_repository_impl import PermisoRepositoryImpl

class PermisoUseCases:
    def __init__(self, permiso_repo: PermisoRepositoryImpl):
        self.permiso_repo = permiso_repo
        
    def get_tipo_permiso_by_id(self, tipo_permiso_id: int) -> Optional[TipoPermiso]:
        return self.permiso_repo.get_tipo_permiso_by_id(tipo_permiso_id)

    def get_permiso(self, permiso_id: int) -> Optional[Permiso]:
        return self.permiso_repo.get_by_id(permiso_id)

    def list_permisos(self, skip: int = 0, limit: int = 10) -> List[Permiso]:
        return self.permiso_repo.list(skip=skip, limit=limit)

    def create_permiso(self, permiso_create: PermisoCreate, db: Session):
        # Verifica si el colaborador existe
        colaborador = db.query(ColaboradorDBModel).filter(ColaboradorDBModel.id == permiso_create.id_colaborador).first()
        if not colaborador:
            raise HTTPException(status_code=404, detail="Colaborador not found")
        
        new_permiso = PermisoDBModel(
            id_colaborador=permiso_create.id_colaborador,
            id_tipopermiso=permiso_create.id_tipo_permiso,
            fecha_inicio=permiso_create.fecha_inicio,
            fecha_fin=permiso_create.fecha_fin
        )
        
        db.add(new_permiso)
        db.commit()
        db.refresh(new_permiso)
        
        return new_permiso





