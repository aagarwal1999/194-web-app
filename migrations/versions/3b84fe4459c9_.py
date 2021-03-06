"""empty message

Revision ID: 3b84fe4459c9
Revises: 0149ad5e844c
Create Date: 2021-05-08 13:32:44.910084

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3b84fe4459c9'
down_revision = '0149ad5e844c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dataset', sa.Column('avg_sentence_count', sa.Float(), nullable=True))
    op.drop_column('dataset', 'sentence_count')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dataset', sa.Column('sentence_count', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('dataset', 'avg_sentence_count')
    # ### end Alembic commands ###
