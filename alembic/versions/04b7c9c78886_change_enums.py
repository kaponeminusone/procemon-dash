"""change enums

Revision ID: 04b7c9c78886
Revises: d4ccbd30cf2e
Create Date: 2024-10-09 16:06:06.613265

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '04b7c9c78886'
down_revision: Union[str, None] = 'd4ccbd30cf2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
       # Crear tipos ENUM si no existen
    tipo_enum = postgresql.ENUM('admin', 'user', 'guest', name='tipoenum')
    tipo_enum_indicador = postgresql.ENUM('range', 'checkbox', 'criteria', name='tipoenumindicador')
    tipo_enum_entrada = postgresql.ENUM('int', 'float', name='tipoenumentrada')

    # Crear los tipos en la base de datos
    tipo_enum.create(op.get_bind(), checkfirst=True)
    tipo_enum_indicador.create(op.get_bind(), checkfirst=True)
    tipo_enum_entrada.create(op.get_bind(), checkfirst=True)

    # Alterar columnas para usar los nuevos ENUM
    op.alter_column(
        'entradas', 
        'tipo',
        existing_type=postgresql.ENUM('type1', 'type2', name='tipoenumentrada'),
        type_=tipo_enum_entrada,
        postgresql_using='tipo::text::tipoenumentrada',  # Usar expresión para conversión
        existing_nullable=True
    )
    op.alter_column(
        'indicadores', 
        'tipo',
        existing_type=postgresql.ENUM('type1', 'type2', name='tipoenumindicador'),
        type_=tipo_enum_indicador,
        postgresql_using='tipo::text::tipoenumindicador',  # Usar expresión para conversión
        existing_nullable=False
    )
    op.alter_column(
        'usuario', 
        'tipo',
        existing_type=postgresql.ENUM('type1', 'type2', 'type3', name='tipoenum'),
        type_=tipo_enum,
        postgresql_using='tipo::text::tipoenum',  # Usar expresión para conversión
        existing_nullable=False
    )
    # ### end Alembic commands ###

def downgrade() -> None:
     # Convertir los valores actuales a tipo de texto antes de hacer la reversión
    # Convertir los valores actuales a tipo de texto antes de hacer la reversión
    op.alter_column(
        'usuario', 
        'tipo',
        existing_type=postgresql.ENUM('admin', 'user', 'guest', name='tipoenum'),
        type_=sa.Enum('type1', 'type2', 'type3', name='tipoenum'),
        existing_nullable=False,
        postgresql_using='tipo::text::tipoenum'
    )
    
    op.alter_column(
        'indicadores', 
        'tipo',
        existing_type=postgresql.ENUM('range', 'checkbox', 'criteria', name='tipoenumindicador'),
        type_=sa.Enum('type1', 'type2', 'type3', name='tipoenum'),
        existing_nullable=False,
        postgresql_using='tipo::text::tipoenum'
    )
    
    op.alter_column(
        'entradas', 
        'tipo',
        existing_type=postgresql.ENUM('int', 'float', name='tipoenumentrada'),
        type_=sa.Enum('type1', 'type2', name='tipoenumentrada'),
        existing_nullable=True,
        postgresql_using='tipo::text::tipoenumentrada'
    )
    
    # ### end Alembic commands ###
