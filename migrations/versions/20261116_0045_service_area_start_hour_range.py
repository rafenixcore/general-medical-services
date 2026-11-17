"""Rango válido para service_areas.start_hour

La hora de inicio del área es la que usan los avisos y los plazos de confirmación.
Un valor fuera de 0..23 (por ejemplo, 25) desplazaría el turno a un día distinto y el
médico recibiría una hora imposible. La API ya lo valida; esta restricción lo impide
también a nivel de base.

Solo DDL: no toca ninguna fila.

Revision ID: 20261116_0045
Revises: 20261113_0044
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20261116_0045"
down_revision: str | None = "20261113_0044"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_CONSTRAINT = "ck_service_areas_start_hour_range"


def upgrade() -> None:
    op.execute(
        f"""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint WHERE conname = '{_CONSTRAINT}'
            ) THEN
                ALTER TABLE service_areas
                ADD CONSTRAINT {_CONSTRAINT}
                CHECK (start_hour >= 0 AND start_hour <= 23);
            END IF;
        END
        $$;
        """
    )


def downgrade() -> None:
    op.execute(f"ALTER TABLE service_areas DROP CONSTRAINT IF EXISTS {_CONSTRAINT};")
