"""initial migration

Revision ID: c3cd81ec0423
Revises: 
Create Date: 2023-11-14 22:12:49.829794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3cd81ec0423'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('links', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.alter_column('long_url',
               existing_type=sa.TEXT(),
               type_=sa.String(length=500),
               existing_nullable=True)
        batch_op.alter_column('short_url',
               existing_type=sa.TEXT(),
               type_=sa.String(length=500),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('links', schema=None) as batch_op:
        batch_op.alter_column('short_url',
               existing_type=sa.String(length=500),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('long_url',
               existing_type=sa.String(length=500),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    # ### end Alembic commands ###