"""empty message

Revision ID: 26365fce7735
Revises: e731b2aa2436
Create Date: 2022-04-04 22:39:11.401783

"""
import geoalchemy2  # noqa
from alembic import op
import sqlalchemy as sa  # noqa


# revision identifiers, used by Alembic.
revision = "26365fce7735"
down_revision = "e731b2aa2436"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "activity",
        sa.Column("start_time", sa.DateTime(), nullable=True),
        schema="vision_sources",
    )
    op.add_column(
        "activity",
        sa.Column("end_time", sa.DateTime(), nullable=True),
        schema="vision_sources",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("activity", "end_time", schema="vision_sources")
    op.drop_column("activity", "start_time", schema="vision_sources")
    # ### end Alembic commands ###
