"""empty message

Revision ID: 1298e3a88f95
Revises: 3a6891149395
Create Date: 2022-05-24 00:14:49.231357

"""
import geoalchemy2  # noqa
from alembic import op
import sqlalchemy as sa  # noqa


# revision identifiers, used by Alembic.
revision = "1298e3a88f95"
down_revision = "3a6891149395"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(
        None, "geometry", ["geometry_id"], schema="vision_sources"
    )
    op.drop_column("geometry", "self_link", schema="vision_sources")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "geometry",
        sa.Column(
            "self_link", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
        schema="vision_sources",
    )
    op.drop_constraint(
        None, "geometry", schema="vision_sources", type_="unique"
    )
    # ### end Alembic commands ###