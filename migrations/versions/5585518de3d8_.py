"""empty message

Revision ID: 5585518de3d8
Revises: dbefb6e62384
Create Date: 2024-04-28 15:16:59.333217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5585518de3d8'
down_revision = 'dbefb6e62384'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_path', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.drop_column('image_path')

    # ### end Alembic commands ###
