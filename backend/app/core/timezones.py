"""Zona horaria de la institución.

`service_areas.start_hour` es la hora de pared del hospital, no UTC. Los plazos de
confirmación y el cron se calculan en UTC, así que la conversión se centraliza aquí
para que no haya dos criterios en distintos puntos del código.

República Dominicana usa UTC-4 todo el año: no aplica horario de verano.
"""

from zoneinfo import ZoneInfo

SERVICE_TIMEZONE_NAME = "America/Santo_Domingo"
SERVICE_TIMEZONE = ZoneInfo(SERVICE_TIMEZONE_NAME)
