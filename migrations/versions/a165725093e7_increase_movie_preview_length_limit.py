"""Increase movie preview length limit

Revision ID: a165725093e7
Revises: 638a188c9ee7
Create Date: 2021-11-19 05:07:24.982825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a165725093e7'
down_revision = '638a188c9ee7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('movie', 'preview',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=255),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('movie', 'preview',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
    # ### end Alembic commands ###