"""empty message

Revision ID: 2baf474fd85b
Revises: 4bde0a1e2bbe
Create Date: 2014-04-27 16:00:27.943347

"""

# revision identifiers, used by Alembic.
revision = '2baf474fd85b'
down_revision = '4bde0a1e2bbe'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.rename_table('detail', 'stock')
    op.alter_column('per_share', column_name='code_id', new_column_name='stock_id')
    op.alter_column('bal_sheet', column_name='code_id', new_column_name='stock_id')
    op.alter_column('price_history', column_name='code_id', new_column_name='stock_id')


def downgrade():
    op.rename_table('stock', 'detail')
    op.alter_column('per_share', column_name='stock_id', new_column_name='code_id')
    op.alter_column('bal_sheet', column_name='stock_id', new_column_name='code_id')
    op.alter_column('price_history', column_name='stock_id', new_column_name='code_id')
