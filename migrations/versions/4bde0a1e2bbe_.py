"""empty message

Revision ID: 4bde0a1e2bbe
Revises: 290fea97fea6
Create Date: 2014-04-27 15:45:26.239330

"""

# revision identifiers, used by Alembic.
revision = '4bde0a1e2bbe'
down_revision = '290fea97fea6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('stock_balsheet_code_id', table_name='bal_sheet')
    op.drop_index('stock_detail_code_like', table_name='detail')
    op.drop_index('stock_pershare_code_id', table_name='per_share')
    op.drop_index('stock_pricehistory_code_id', table_name='price_history')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index('stock_pricehistory_code_id', 'price_history', ['code_id'], unique=False)
    op.create_index('stock_pershare_code_id', 'per_share', ['code_id'], unique=False)
    op.create_index('stock_detail_code_like', 'detail', ['code'], unique=False)
    op.create_index('stock_balsheet_code_id', 'bal_sheet', ['code_id'], unique=False)
    ### end Alembic commands ###
