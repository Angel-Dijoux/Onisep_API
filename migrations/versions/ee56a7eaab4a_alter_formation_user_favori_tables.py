"""Add UUID in formation table.

Revision ID: ee56a7eaab4a
Revises: 16c8bc08a922
Create Date: 2023-10-29 22:09:53.444244

"""
from alembic import op
from sqlalchemy.dialects import mysql

from src.models.helpers.UUIDType import UUIDType

# revision identifiers, used by Alembic.
revision = "ee56a7eaab4a"
down_revision = "16c8bc08a922"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_constraint("favori_formation_id_fk", "user_favori", type_="foreignkey")

    op.alter_column(
        "formation",
        "id",
        existing_type=mysql.VARCHAR(length=36),
        type_=UUIDType(),
        existing_nullable=False,
    )
    op.alter_column(
        "user_favori",
        "formation_id",
        existing_type=mysql.VARCHAR(length=36),
        type_=UUIDType(),
        existing_nullable=False,
    )

    op.create_foreign_key(
        "favori_formation_id_fk", "user_favori", "formation", ["formation_id"], ["id"]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("favori_formation_id_fk", "user_favori", type_="foreignkey")

    op.alter_column(
        "user_favori",
        "formation_id",
        existing_type=UUIDType(),
        type_=mysql.VARCHAR(length=36),
        existing_nullable=False,
    )
    op.alter_column(
        "formation",
        "id",
        existing_type=UUIDType(),
        type_=mysql.VARCHAR(length=36),
        existing_nullable=False,
    )

    op.create_foreign_key(
        "favori_formation_id_fk", "user_favori", "formation", ["formation_id"], ["id"]
    )
    # ### end Alembic commands ###
