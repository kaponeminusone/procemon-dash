from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey, Enum as SQLAlchemyEnum, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()

# Define enum types
class TipoEnum(str, Enum):
    type1 = 'type1'
    type2 = 'type2'
    type3 = 'type3'

class TipoEnumIndicador(str, Enum):
    indicador1 = 'indicador1'
    indicador2 = 'indicador2'

class TipoEnumEntrada(str, Enum):
    entrada1 = 'entrada1'
    entrada2 = 'entrada2'

class Indicadores(Base):
    __tablename__ = 'indicadores'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String, nullable=False)
    tipo = Column(SQLAlchemyEnum(TipoEnumIndicador), nullable=False)

class Entradas(Base):
    __tablename__ = 'entradas'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String)
    tipo = Column(SQLAlchemyEnum(TipoEnumEntrada))

class Procesos(Base):
    __tablename__ = 'procesos'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String, nullable=False)
    num_etapas = Column(Integer)

class Etapas(Base):
    __tablename__ = 'etapas'

    id = Column(BigInteger, primary_key=True)
    num_etapa = Column(BigInteger, nullable=False)
    id_proceso = Column(BigInteger, ForeignKey('procesos.id'))
    proceso = relationship('Procesos', backref='etapas')

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False)
    tipo = Column(SQLAlchemyEnum(TipoEnum), nullable=False)

class EtapaIndicadores(Base):
    __tablename__ = 'etapa_indicadores'

    id_etapa = Column(BigInteger, ForeignKey('etapas.id'), primary_key=True)
    id_indicador_entrada = Column(BigInteger, ForeignKey('indicadores.id'), primary_key=True)

class EtapasEntradas(Base):
    __tablename__ = 'etapas_entradas'

    id_etapa = Column(BigInteger, ForeignKey('etapas.id'), primary_key=True)
    id_entrada = Column(BigInteger, ForeignKey('entradas.id'), primary_key=True)

class EtapasSalidas(Base):
    __tablename__ = 'etapas_salidas'

    id_etapa = Column(BigInteger, ForeignKey('etapas.id'), primary_key=True)
    id_entrada = Column(BigInteger, ForeignKey('entradas.id'))

class IndicadoresEntradas(Base):
    __tablename__ = 'indicadores_entradas'

    id = Column(BigInteger, primary_key=True)
    id_entrada = Column(BigInteger, ForeignKey('entradas.id'), nullable=False)
    id_indicador = Column(BigInteger, ForeignKey('indicadores.id'))

class Registro(Base):
    __tablename__ = 'registro'

    id = Column(BigInteger, primary_key=True)
    id_usuario = Column(BigInteger, ForeignKey('usuario.id'), nullable=False)
    descripcion = Column(String)
    creado = Column(TIMESTAMP, default="now()")
    modificado = Column(TIMESTAMP, default="now()")

class RegistroEntradas(Base):
    __tablename__ = 'registro_entradas'

    id_registro = Column(BigInteger, ForeignKey('registro.id'), primary_key=True)
    id_entrada = Column(BigInteger, ForeignKey('entradas.id'))

class RegistroIndicadores(Base):
    __tablename__ = 'registro_indicadores'

    id_registro = Column(BigInteger, ForeignKey('registro.id'), primary_key=True)
    id_indicador = Column(BigInteger, ForeignKey('indicadores.id'))

class RegistroProcesos(Base):
    __tablename__ = 'registro_procesos'

    id_registro = Column(BigInteger, ForeignKey('registro.id'), primary_key=True)
    id_proceso = Column(BigInteger, ForeignKey('procesos.id'))


# from sqlalchemy import Table, Column
# from sqlalchemy.sql.sqltypes import Integer, String
# from app.db.database import engine, meta #TODO: add Barrel

# users = Table("users", meta, 
#               Column("id", Integer, primary_key=True), 
#               Column("name", String(255)),
#               Column("email", String(255))
#               )

# meta.create_all(engine)