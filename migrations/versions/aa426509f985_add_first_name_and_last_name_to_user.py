"""Add first_name and last_name to user

Revision ID: aa426509f985
Revises: 
Create Date: 2024-04-26 14:34:40.536760

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'aa426509f985'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('last_name', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('date_created', sa.DateTime(timezone=True), nullable=True))
        batch_op.alter_column('username',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=200),
               type_=sa.Text(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=200),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.drop_column('date_created')
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')

    op.create_table('message',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('subject', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('message', mysql.TEXT(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
