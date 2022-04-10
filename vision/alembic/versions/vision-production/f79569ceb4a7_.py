"""empty message

Revision ID: f79569ceb4a7
Revises: 17d7df7b7117
Create Date: 2022-03-24 22:25:03.826179

"""
import geoalchemy2  # noqa
from alembic import op
import sqlalchemy as sa  # noqa


# revision identifiers, used by Alembic.
revision = "f79569ceb4a7"
down_revision = "17d7df7b7117"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "introduction",
        "artwork_id",
        existing_type=sa.BIGINT(),
        nullable=True,
        schema="vision_sources",
    )
    op.alter_column(
        "series",
        "landmark_id",
        existing_type=sa.BIGINT(),
        nullable=True,
        schema="vision_sources",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "series",
        "landmark_id",
        existing_type=sa.BIGINT(),
        nullable=False,
        schema="vision_sources",
    )
    op.alter_column(
        "introduction",
        "artwork_id",
        existing_type=sa.BIGINT(),
        nullable=False,
        schema="vision_sources",
    )
    # ### end Alembic commands ###