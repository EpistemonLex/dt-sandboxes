from typing import Callable, Awaitable, Optional
from dt_sandboxes.engines.kaplay.schemas import (
    KaplayTelemetryEvent, 
    TelemetryKind, 
    KaplayCompilationErrorPayload
)

class KaplayTelemetryHook:
    def __init__(
        self, 
        sandbox_id: str, 
        broadcast_fn: Callable[[KaplayTelemetryEvent], Awaitable[None]]
    ):
        self.sandbox_id = sandbox_id
        self.broadcast_fn = broadcast_fn

    async def capture_js_error(
        self, 
        message: str, 
        line: Optional[int] = None, 
        column: Optional[int] = None, 
        stack: Optional[str] = None
    ) -> None:
        """Capture a JavaScript compilation error and broadcast it as telemetry."""
        
        # Create the payload from the provided error details
        payload_model = KaplayCompilationErrorPayload(
            message=message,
            line=line,
            column=column,
            stack=stack
        )
        
        # Build the full telemetry event
        event = KaplayTelemetryEvent(
            sandbox_id=self.sandbox_id,
            kind=TelemetryKind.COMPILATION_ERROR,
            payload=payload_model.model_dump()
        )
        
        # Broadcast the event
        await self.broadcast_fn(event)
