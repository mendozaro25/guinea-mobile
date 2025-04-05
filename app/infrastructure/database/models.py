from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.infrastructure.database.config import Base

class UserDBModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    
class ColaboradorDBModel(Base):
    __tablename__ = 'colaborador'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    
class TipoPermisoDBModel(Base):
    __tablename__ = 'tipo_permiso'

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)

class PermisoDBModel(Base):
    __tablename__ = 'permiso'

    id = Column(Integer, primary_key=True, index=True)
    id_colaborador = Column(Integer, ForeignKey('colaborador.id'), nullable=False)
    id_tipopermiso = Column(Integer, ForeignKey('tipo_permiso.id'), nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=False)
    
    colaborador = relationship("ColaboradorDBModel")
    tipo_permiso = relationship("TipoPermisoDBModel")
