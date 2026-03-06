from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field

class SandboxType(str, Enum):
    KAPLAY = "kaplay"
    MINETEST = "minetest"
    TURBOWARP = "turbowarp"
    SONICPI = "sonicpi"

class TelemetryType(str, Enum):
    CODE_CHANGE = "code_change"
    COMPILATION_ERROR = "compilation_error"
    STATE_CHANGE = "state_change"
    LIFECYCLE = "lifecycle"  # start, stop, etc.

class BaseTelemetry(BaseModel):
    model_config = ConfigDict(slots=True)

    sandbox_id: str
    sandbox_type: SandboxType
    event_type: TelemetryType
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: Dict[str, Any] = Field(default_factory=dict)

class KaplayCodeChange(BaseTelemetry):
    event_type: TelemetryType = TelemetryType.CODE_CHANGE
    code: str
    cursor_position: Optional[int] = None

class KaplayCompilationError(BaseTelemetry):
    event_type: TelemetryType = TelemetryType.COMPILATION_ERROR
    error_message: str
    line_number: Optional[int] = None
    column_number: Optional[int] = None

class KaplayStateChange(BaseTelemetry):
    event_type: TelemetryType = TelemetryType.STATE_CHANGE
    state: Dict[str, Any]  # e.g., current physics values, entities
