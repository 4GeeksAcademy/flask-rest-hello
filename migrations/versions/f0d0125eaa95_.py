"""empty message

Revision ID: f0d0125eaa95
Revises: 2d547c56ece2
Create Date: 2025-01-27 19:43:39.490687

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f0d0125eaa95'
down_revision = '2d547c56ece2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('homeworld_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'planet', ['homeworld_id'], ['id'])
        batch_op.drop_column('homeworld')

    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.drop_column('residents')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('residents', postgresql.BYTEA(), autoincrement=False, nullable=True))

    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('homeworld', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('homeworld_id')

    # ### end Alembic commands ###
