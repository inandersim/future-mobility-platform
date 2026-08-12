"""add identity security state

Revision ID: 0006_identity_security_hardening
Revises: 0005_devices
"""
from alembic import op
import sqlalchemy as sa

revision = "0006_identity_security_hardening"
down_revision = "0005_devices"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("failed_login_attempts", sa.Integer(), server_default="0", nullable=False))
    op.add_column("users", sa.Column("locked_until", sa.DateTime(timezone=True), nullable=True))
    op.add_column("users", sa.Column("password_changed_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.add_column("sessions", sa.Column("last_seen_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.add_column("sessions", sa.Column("replaced_by_session_id", sa.UUID(), nullable=True))
    op.create_index("ix_sessions_replaced_by_session_id", "sessions", ["replaced_by_session_id"])


def downgrade() -> None:
    op.drop_index("ix_sessions_replaced_by_session_id", table_name="sessions")
    op.drop_column("sessions", "replaced_by_session_id")
    op.drop_column("sessions", "last_seen_at")
    op.drop_column("users", "password_changed_at")
    op.drop_column("users", "locked_until")
    op.drop_column("users", "failed_login_attempts")
