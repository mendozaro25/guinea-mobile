from typing import List, Optional
from sqlalchemy.orm import Session
from app.infrastructure.database.models import PermisoDBModel
from app.core.entities.permiso import Permiso

class PermisoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, permiso: Permiso) -> Permiso:
        db_permiso = PermisoDBModel(
            id_colaborador=permiso.colaborador,
            id_tipopermiso=permiso.tipo_permiso,
            fecha_inicio=permiso.fecha_inicio,
            fecha_fin=permiso.fecha_fin
        )
        self.db.add(db_permiso)
        self.db.commit()
        self.db.refresh(db_permiso)
        return self._to_entity(db_permiso)

    def get_by_id(self, permiso_id: int) -> Optional[Permiso]:
        db_permiso = self.db.query(PermisoDBModel).filter(PermisoDBModel.id == permiso_id).first()
        return self._to_entity(db_permiso) if db_permiso else None

    def list(self, skip: int = 0, limit: int = 10) -> List[Permiso]:
        db_permisos = self.db.query(PermisoDBModel).offset(skip).limit(limit).all()
        return [self._to_entity(db_permiso) for db_permiso in db_permisos]

    def _to_entity(self, db_permiso: PermisoDBModel) -> Permiso:
        return Permiso(
            id=db_permiso.id,
            colaborador=db_permiso.id_colaborador,
            tipo_permiso=db_permiso.id_tipopermiso,
            fecha_inicio=db_permiso.fecha_inicio,
            fecha_fin=db_permiso.fecha_fin
        )


