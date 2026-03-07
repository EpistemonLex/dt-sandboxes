"""Schemas for Kaplay engine telemetry."""

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class TelemetryKind(StrEnum):
    """The kind of telemetry event emitted by the Kaplay engine."""

    COMPILATION_ERROR = "compilation_error"
    STATE_CHANGE = "state_change"
    CODE_CHANGE = "code_change"


class KaplayTelemetryEvent(BaseModel):
    """A telemetry event emitted by the Kaplay engine."""

    model_config = ConfigDict(slots=True)

    sandbox_id: str
    kind: TelemetryKind
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    payload: dict[str, object]  # architectural: allowed-object (Generic telemetry payload)


class KaplayCompilationErrorPayload(BaseModel):
    """Payload for a compilation error event."""

    model_config = ConfigDict(slots=True)

    message: str
    line: int | None = None
    column: int | None = None
    stack: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
