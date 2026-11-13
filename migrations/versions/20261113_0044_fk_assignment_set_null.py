"""FKs de asignación con ON DELETE SET NULL.

Revision ID: 20261113_0044
Revises: a2446a0123b3
"""

from alembic import op

revision = "20261113_0044"
down_revision = "a2446a0123b3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint(
        "fk_notification_events_assignment_id_calendar_assignments",
        "notification_events",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_notification_events_assignment_id_calendar_assignments",
        "notification_events",
        "calendar_assignments",
        ["assignment_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.drop_constraint(
        "fk_confirmation_requests_assignment_id_calendar_assignments",
        "confirmation_requests",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_confirmation_requests_assignment_id_calendar_assignments",
        "confirmation_requests",
        "calendar_assignments",
        ["assignment_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_notification_events_assignment_id_calendar_assignments",
        "notification_events",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_notification_events_assignment_id_calendar_assignments",
        "notification_events",
        "calendar_assignments",
        ["assignment_id"],
        ["id"],
    )
    op.drop_constraint(
        "fk_confirmation_requests_assignment_id_calendar_assignments",
        "confirmation_requests",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_confirmation_requests_assignment_id_calendar_assignments",
        "confirmation_requests",
        "calendar_assignments",
        ["assignment_id"],
        ["id"],
    )
