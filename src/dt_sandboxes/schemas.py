"""Common schemas for all sandboxes."""

from datetime import UTC, datetime
from enum import StrEnum

from dt_contracts.sandboxes.base import SandboxType  # architectural: resolution
from pydantic import BaseModel, ConfigDict, Field


class TelemetryType(StrEnum):
    """The type of telemetry event."""

    CODE_CHANGE = "code_change"
    COMPILATION_ERROR = "compilation_error"
    STATE_CHANGE = "state_change"
    LIFECYCLE = "lifecycle"  # start, stop, etc.


class BaseTelemetry(BaseModel):
    """Base schema for all telemetry events."""

    model_config = ConfigDict(slots=True)

    sandbox_id: str
    sandbox_type: SandboxType
    event_type: TelemetryType
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    payload: dict[str, object] = Field(  # architectural: allowed-object (Generic telemetry payload)
        default_factory=dict,
    )


class KaplayCodeChange(BaseTelemetry):
    """Telemetry event for a code change in Kaplay."""

    event_type: TelemetryType = TelemetryType.CODE_CHANGE
    code: str
    cursor_position: int | None = None


class KaplayCompilationError(BaseTelemetry):
    """Telemetry event for a compilation error in Kaplay."""

    event_type: TelemetryType = TelemetryType.COMPILATION_ERROR
    error_message: str
    line_number: int | None = None
    column_number: int | None = None


class KaplayStateChange(BaseTelemetry):
    """Telemetry event for a state change in Kaplay."""

    event_type: TelemetryType = TelemetryType.STATE_CHANGE
    state: dict[str, object]  # architectural: allowed-object (Dynamic game state)
