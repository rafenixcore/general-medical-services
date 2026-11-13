"""Un aviso fallido no debe deshacer el trabajo de la ruta."""

import datetime
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from backend.app.application.notifications.providers import FakeProvider
from backend.app.application.notifications.service import NotificationService
from backend.app.infrastructure.db.models.calendars import CalendarModel
from backend.app.infrastructure.repositories.notifications import NotificationRepository


def test_queue_fallido_no_revierte_trabajo_previo(db_session) -> None:
    now = datetime.datetime.now(datetime.UTC)
    calendar = CalendarModel(
        id=str(uuid4()),
        year=2026,
        month=5,
        status="draft",
        generation_mode="manual",
        created_by="actor-001",
        approved_by=None,
        created_at=now,
        updated_at=now,
        approved_at=None,
    )
    db_session.add(calendar)
    db_session.flush()

    service = NotificationService(
        repo=NotificationRepository(db_session),
        provider=FakeProvider(),
    )

    with pytest.raises(IntegrityError):
        service.queue(
            notification_type="service_assignment_removed",
            idempotency_key=f"roto-{uuid4()}",
            recipient_doctor_id=None,
            recipient_phone=None,
            payload={"message": "x"},
            assignment_id=str(uuid4()),  # no existe: viola la FK
        )

    db_session.commit()

    assert db_session.get(CalendarModel, calendar.id) is not None
