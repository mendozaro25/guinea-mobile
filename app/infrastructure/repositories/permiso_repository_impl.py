from typing import List, Optional
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from app.core.entities.permiso import Permiso, TipoPermiso, Colaborador
from app.infrastructure.database.models import ColaboradorDBModel, PermisoDBModel, TipoPermisoDBModel

class PermisoRepositoryImpl:
    def __init__(self, db: Session):
        self.db = db

    def _map_permiso_db_to_entity(self, db_permiso: PermisoDBModel) -> Permiso:
        return Permiso(
            id=db_permiso.id,
            id_colaborador=db_permiso.id_colaborador,
            id_tipo_permiso=db_permiso.id_tipopermiso,
            fecha_inicio=db_permiso.fecha_inicio,
            fecha_fin=db_permiso.fecha_fin,
        )

    def create(self, permiso: Permiso) -> Permiso:
        db_permiso = PermisoDBModel(
            id_colaborador=permiso.id_colaborador,
            id_tipopermiso=permiso.id_tipo_permiso,
            fecha_inicio=permiso.fecha_inicio,
            fecha_fin=permiso.fecha_fin,
        )
        self.db.add(db_permiso)
        self.db.commit()
        self.db.refresh(db_permiso)
        return self._map_permiso_db_to_entity(db_permiso)

    def get_by_id(self, permiso_id: int) -> Optional[Permiso]:
        try:
            db_permiso = self.db.query(PermisoDBModel).filter(PermisoDBModel.id == permiso_id).one()
            return self._map_permiso_db_to_entity(db_permiso)
        except NoResultFound:
            return None

    def list(self, skip: int = 0, limit: int = 10) -> List[Permiso]:
        db_permisos = self.db.query(PermisoDBModel).offset(skip).limit(limit).all()
        return [self._map_permiso_db_to_entity(permiso) for permiso in db_permisos]

    def get_tipo_permiso_by_id(self, tipo_permiso_id: int) -> Optional[TipoPermiso]:
        db_tipo_permiso = self.db.query(TipoPermisoDBModel).filter(TipoPermisoDBModel.id == tipo_permiso_id).first()
        if db_tipo_permiso:
            return TipoPermiso(id=db_tipo_permiso.id, descripcion=db_tipo_permiso.descripcion)
        return None

    def get_colaborador(self, colaborador_id: int) -> Optional[Colaborador]:
        return self.db.query(ColaboradorDBModel).filter(ColaboradorDBModel.id == colaborador_id).first()

    def get_tipo_permiso_by_id(self, tipo_permiso_id: int) -> Optional[TipoPermiso]:
        db_tipo_permiso = self.db.query(TipoPermisoDBModel).filter(TipoPermisoDBModel.id == tipo_permiso_id).first()
        return TipoPermiso(id=db_tipo_permiso.id, descripcion=db_tipo_permiso.descripcion) if db_tipo_permiso else None
    
    def get_tipo_permiso(self, tipo_permiso_id: int) -> Optional[TipoPermiso]:
        db_tipo_permiso = self.db.query(TipoPermisoDBModel).filter(TipoPermisoDBModel.id == tipo_permiso_id).first()
        return TipoPermiso(id=db_tipo_permiso.id, descripcion=db_tipo_permiso.descripcion) if db_tipo_permiso else None