"""empty message

Revision ID: 46fc5966de63
Revises:
Create Date: 2023-06-16 15:07:46.045874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46fc5966de63'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_task_user_id', 'task', ['user_id'], ['id'])
        batch_op.drop_column('lead')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lead', sa.VARCHAR(length=30), nullable=False))
        batch_op.drop_constraint('fk_task_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')
    # ### end Alembic commands ###
