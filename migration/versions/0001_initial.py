"""initial

Revision ID: 0001
Revises: 
Create Date: 2023-05-12 23:12:45.375331

"""
from alembic import op
import sqlalchemy as sa

from src.utils.consts import Roles


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'class_lessons',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('grade', sa.Integer(), nullable=False),
        sa.Column('letter', sa.String(length=1), nullable=False),
        sa.Column('image', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id')
    )
    op.create_table(
        'full_lessons',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('grade', sa.Integer(), nullable=False),
        sa.Column('image', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id')
    )
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
        sa.UniqueConstraint('role')
    )

    for role in Roles:
        op.execute(f'INSERT INTO roles (role) VALUES ("{role.value}")')

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=32), nullable=True),
        sa.Column('grade', sa.Integer(), nullable=True),
        sa.Column('letter', sa.String(length=1), nullable=True),
        sa.Column('lessons_notify', sa.Boolean(), nullable=False),
        sa.Column('news_notify', sa.Boolean(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('createad_time', sa.DateTime(), nullable=False),
        sa.Column('modified_time', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f('ix_users_user_id'), ['user_id'], unique=True
        )

    op.create_table(
        'menus',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('edit_by', sa.Integer(), nullable=True),
        sa.Column('breakfast', sa.String(), nullable=True),
        sa.Column('lunch', sa.String(), nullable=True),
        sa.Column('dinner', sa.String(), nullable=True),
        sa.Column('snack', sa.String(), nullable=True),
        sa.Column('supper', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['edit_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id')
    )
    with op.batch_alter_table('menus', schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f('ix_menus_date'), ['date'], unique=True
        )

    op.create_table(
        'users_to_roles',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_to_roles')
    with op.batch_alter_table('menus', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_menus_date'))

    op.drop_table('menus')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_user_id'))

    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('full_lessons')
    op.drop_table('class_lessons')
    # ### end Alembic commands ###
