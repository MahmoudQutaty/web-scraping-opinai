"""Updated models with relationships

Revision ID: 435b5f5197af
Revises: bc2280de5907
Create Date: 2024-12-12 10:51:18.893977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '435b5f5197af'
down_revision = 'bc2280de5907'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('agents', schema=None) as batch_op:
        batch_op.alter_column('image_url',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.Text(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('agents', schema=None) as batch_op:
        batch_op.alter_column('image_url',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=200),
               existing_nullable=True)

    # ### end Alembic commands ###
