"""Hora de inicio del servicio: una sola fuente de verdad para los avisos.

`calendar_assignments.service_start_at` es una copia que se congela al crear el turno
(en UTC). La hora que manda es la del área (`service_areas.start_hour`), que está en
hora **local** del hospital: el médico lee su reloj, no UTC.

Por eso toda lectura de la hora de inicio (texto del aviso y plazos de confirmación)
pasa por `service_start_for`, que devuelve un datetime **con zona local**:

- el texto se formatea tal cual (06:00 se lee "06:00 AM");
- restar 12/8/4 horas y comparar contra `datetime.now(UTC)` funciona igual, porque
  ambos lados están "aware" y Python compara instantes.
"""

from datetime import UTC, datetime

from backend.app.core.timezones import SERVICE_TIMEZONE


def local_service_start(service_date, hour: int) -> datetime:
    """Las 06:00 del hospital, con su zona local (la que lee el médico)."""
    return datetime(
        service_date.year,
        service_date.month,
        service_date.day,
        hour,
        0,
        0,
        tzinfo=SERVICE_TIMEZONE,
    )


def service_start_utc(service_date, hour: int) -> datetime:
    """Instante UTC que se guarda en `calendar_assignments.service_start_at`.

    La columna es `timestamptz`: se almacena el instante, no la hora de pared. Guardar
    06:00 como UTC desplazaría el turno cuatro horas.
    """
    return local_service_start(service_date, hour).astimezone(UTC)


def service_start_for(assignment, area=None) -> datetime | None:
    """Hora de inicio en hora local, para comunicarla y calcular plazos.

    Prioriza `area.start_hour`; solo si el área no está disponible (repositorios
    falsos, pruebas sin sesión) cae a la copia guardada en la asignación, que viene
    en UTC y se convierte a local. Una hora corrupta en la base no se usa: se ignora
    y manda la copia, en vez de reventar el envío.
    """
    service_date = getattr(assignment, "service_date", None)
    start_hour = getattr(area, "start_hour", None) if area is not None else None
    stored = getattr(assignment, "service_start_at", None)

    try:
        hour = int(start_hour) if start_hour is not None else None
    except (TypeError, ValueError):
        hour = None

    if hour is not None and 0 <= hour <= 23 and service_date is not None:
        return local_service_start(service_date, hour)

    if stored is not None:
        if getattr(stored, "tzinfo", None) is None:
            stored = stored.replace(tzinfo=UTC)
        return stored.astimezone(SERVICE_TIMEZONE)

    return None
