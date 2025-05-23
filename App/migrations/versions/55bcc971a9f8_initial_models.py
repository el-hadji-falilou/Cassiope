"""Initial models

Revision ID: 55bcc971a9f8
Revises: 
Create Date: 2025-05-18 11:43:30.543961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55bcc971a9f8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('promotions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('key_master', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('crypto_materials',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cohort_id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=256), nullable=False),
    sa.Column('delta_in', sa.String(length=64), nullable=True),
    sa.Column('delta_out', sa.String(length=64), nullable=True),
    sa.Column('uploaded_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['cohort_id'], ['promotions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('pwd_hash', sa.String(length=128), nullable=False),
    sa.Column('role', sa.Enum('student', 'teacher', name='userrole'), nullable=False),
    sa.Column('cohort_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cohort_id'], ['promotions.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('crypto_materials')
    op.drop_table('promotions')
    # ### end Alembic commands ###
