"""update to enums for indicador and entrada

Revision ID: d4ccbd30cf2e
Revises: e37e47804523
Create Date: 2024-10-07 02:58:02.769723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd4ccbd30cf2e'
down_revision: Union[str, None] = 'e37e47804523'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Crear tipos ENUM si no existen
    tipo_enum_entrada = postgresql.ENUM('type1', 'type2', name='tipoenumentrada')
    tipo_enum_indicador = postgresql.ENUM('type1', 'type2', 'type3', name='tipoenumindicador')

    # Crear los tipos en la base de datos
    tipo_enum_entrada.create(op.get_bind(), checkfirst=True)
    tipo_enum_indicador.create(op.get_bind(), checkfirst=True)

    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'entradas', 
        'tipo',
        existing_type=postgresql.ENUM('type1', 'type2', 'type3', name='tipoenum'),
        type_=tipo_enum_entrada,
        postgresql_using='tipo::text::tipoenumentrada',  # Usar expresión para conversión
        existing_nullable=True
    )
    op.alter_column(
        'indicadores', 
        'tipo',
        existing_type=postgresql.ENUM('type1', 'type2', 'type3', name='tipoenum'),
        type_=tipo_enum_indicador,
        postgresql_using='tipo::text::tipoenumindicador',  # Usar expresión para conversión
        existing_nullable=False
    )
    # ### end Alembic commands ###
def downgrade() -> None:
    # Convertir los valores actuales a tipo de texto antes de hacer la reversión
    op.alter_column(
        'indicadores', 
        'tipo',
        existing_type=postgresql.ENUM('type1', 'type2', 'type3', name='tipoenumindicador'),
        type_=sa.Enum('type1', 'type2', 'type3', name='tipoenum'),
        existing_nullable=False,
        postgresql_using='tipo::text::tipoenum'
    )
    
    op.alter_column(
        'entradas', 
        'tipo',
        existing_type=postgresql.ENUM('type1', 'entrada2', name='tipoenumentrada'),
        type_=sa.Enum('type1', 'type2', 'type3', name='tipoenum'),
        existing_nullable=True,
        postgresql_using='tipo::text::tipoenum'
    )
    
    # Eliminar los tipos ENUM si no se usan en ninguna tabla
    op.execute("DROP TYPE tipoenumentrada CASCADE")
    op.execute("DROP TYPE tipoenumindicador CASCADE")
