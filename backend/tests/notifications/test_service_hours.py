"""La hora del área es hora local de la institución, no UTC.

`service_areas.start_hour` se configura pensando en el reloj de pared del hospital
(República Dominicana, UTC-4). El cálculo de plazos y el cron trabajan en UTC, así que
la conversión tiene que hacerse aquí, en un solo sitio. Antes se interpretaba como UTC:
un turno de 06:00 se anunciaba a las 06:00 pero el recordatorio T-12 salía a las 14:00
locales, y el médico podía presentarse a la hora equivocada.
"""

from datetime import UTC, date, datetime, timedelta
from types import SimpleNamespace

from backend.app.application.notifications.service_hours import (
    service_start_for,
    service_start_utc,
)

SANTO_DOMINGO_OFFSET = timedelta(hours=-4)


def _area(start_hour: int) -> SimpleNamespace:
    return SimpleNamespace(start_hour=start_hour)


def test_start_hour_is_local_time_converted_to_utc():
    """Pista a las 06:00 locales (UTC-4) empieza a las 10:00 UTC."""
    assignment = SimpleNamespace(service_date=date(2026, 5, 1), service_start_at=None)

    start = service_start_for(assignment, _area(6))

    assert start is not None
    assert start.utcoffset() == SANTO_DOMINGO_OFFSET
    assert start.hour == 6
    assert start.astimezone(UTC) == datetime(2026, 5, 1, 10, 0, tzinfo=UTC)


def test_stored_assignment_time_is_shown_in_local_time():
    """La copia guardada está en UTC: al mostrarla debe volver a hora local."""
    assignment = SimpleNamespace(
        service_date=date(2026, 5, 1),
        service_start_at=datetime(2026, 5, 1, 10, 0, tzinfo=UTC),
    )

    start = service_start_for(assignment, None)  # sin área: manda la copia

    assert start is not None
    assert start.utcoffset() == SANTO_DOMINGO_OFFSET
    assert start.hour == 6
    assert start.astimezone(UTC) == datetime(2026, 5, 1, 10, 0, tzinfo=UTC)


def test_service_start_utc_is_the_instant_stored_on_the_assignment():
    """Lo que se guarda en el turno es el instante UTC de la hora local.

    Sin esto, el turno de 06:00 queda guardado como 06:00 UTC (las 02:00 locales) y
    cualquier cálculo que use la copia —reportes, plazos— se desplaza cuatro horas.
    """
    assert service_start_utc(date(2026, 5, 1), 6) == datetime(
        2026, 5, 1, 10, 0, tzinfo=UTC
    )
    assert service_start_utc(date(2026, 12, 1), 6) == datetime(
        2026, 12, 1, 10, 0, tzinfo=UTC
    )
