from datetime import datetime, timezone
from enum import StrEnum
from typing import Any, Dict, Optional
from pydantic import Field, ConfigDict
from dt_contracts.base import DeepthoughtBaseModel

class TelemetryKind(StrEnum):
    COMPILATION_ERROR = "compilation_error"
    STATE_CHANGE = "state_change"
    CODE_CHANGE = "code_change"

class KaplayTelemetryEvent(DeepthoughtBaseModel):
    model_config = ConfigDict(slots=True)

    sandbox_id: str
    kind: TelemetryKind
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: Dict[str, Any]

class KaplayCompilationErrorPayload(DeepthoughtBaseModel):
    model_config = ConfigDict(slots=True)

    message: str
    line: Optional[int] = None
    column: Optional[int] = None
    stack: Optional[str] = None
