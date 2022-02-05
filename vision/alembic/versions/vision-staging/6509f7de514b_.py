"""empty message

Revision ID: 6509f7de514b
Revises: ce284bd6f84f
Create Date: 2022-02-05 01:41:20.280307

"""
import geoalchemy2  # noqa
from alembic import op
import sqlalchemy as sa  # noqa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "6509f7de514b"
down_revision = "ce284bd6f84f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column(
            "inserted_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("user_email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column(
            "language",
            sa.Enum("cn", "en", "fr", name="language"),
            server_default="en",
            nullable=False,
        ),
        sa.Column(
            "date_joined",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "is_superuser",
            sa.Boolean(),
            server_default="FALSE",
            nullable=False,
        ),
        sa.Column(
            "role",
            sa.Enum("admin", "editor", "visitor", name="userrole"),
            server_default="visitor",
            nullable=False,
        ),
        sa.Column(
            "extras", postgresql.JSON(astext_type=sa.Text()), nullable=True
        ),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("user_email"),
        sa.UniqueConstraint("user_id"),
        schema="vision_sources",
    )
    op.drop_column("introduction", "lang", schema="vision_sources")
    op.add_column(
        "series",
        sa.Column(
            "language",
            sa.Enum("cn", "en", "fr", name="language"),
            server_default="en",
            nullable=False,
        ),
        schema="vision_sources",
    )
    op.drop_column("series", "lang", schema="vision_sources")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "series",
        sa.Column("lang", sa.VARCHAR(), autoincrement=False, nullable=False),
        schema="vision_sources",
    )
    op.drop_column("series", "language", schema="vision_sources")
    op.add_column(
        "introduction",
        sa.Column("lang", sa.VARCHAR(), autoincrement=False, nullable=False),
        schema="vision_sources",
    )
    op.drop_table("user", schema="vision_sources")
    # ### end Alembic commands ###