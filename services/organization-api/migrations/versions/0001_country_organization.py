"""create country sovereignty and organization domain

Revision ID: org_0001
Revises: None
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "org_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "countries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("iso2", sa.String(2), nullable=False, unique=True),
        sa.Column("iso3", sa.String(3), nullable=False, unique=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("default_locale", sa.String(20), nullable=False, server_default="en-US"),
        sa.Column("default_timezone", sa.String(80), nullable=False, server_default="UTC"),
        sa.Column("sovereign", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "organizations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("country_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("parent_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("legal_name", sa.String(300), nullable=False),
        sa.Column("display_name", sa.String(200), nullable=False),
        sa.Column("organization_type", sa.String(60), nullable=False),
        sa.Column("registration_number", sa.String(120), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["country_id"], ["countries.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["parent_id"], ["organizations.id"], ondelete="RESTRICT"),
        sa.UniqueConstraint("country_id", "registration_number", name="uq_org_country_registration"),
    )
    op.create_index("ix_organizations_country_id", "organizations", ["country_id"])
    op.create_index("ix_organizations_parent_id", "organizations", ["parent_id"])
    op.create_table(
        "organization_memberships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role", sa.String(100), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("organization_id", "user_id", name="uq_org_membership"),
    )
    op.create_index("ix_org_memberships_organization_id", "organization_memberships", ["organization_id"])
    op.create_index("ix_org_memberships_user_id", "organization_memberships", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_org_memberships_user_id", table_name="organization_memberships")
    op.drop_index("ix_org_memberships_organization_id", table_name="organization_memberships")
    op.drop_table("organization_memberships")
    op.drop_index("ix_organizations_parent_id", table_name="organizations")
    op.drop_index("ix_organizations_country_id", table_name="organizations")
    op.drop_table("organizations")
    op.drop_table("countries")
