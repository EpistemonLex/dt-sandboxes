from dt_sandboxes.base import BaseSandbox
from dt_sandboxes.schemas import SandboxType, KaplayCodeChange, KaplayCompilationError, KaplayStateChange

class KaplaySandbox(BaseSandbox):
    def __init__(self, sandbox_id: str):
        super().__init__(sandbox_id, SandboxType.KAPLAY)

    async def start(self) -> None:
        """Initialize the Kaplay environment."""
        self.is_running = True
        # Future: Actually launch the browser sandbox or setup hooks.

    async def stop(self) -> None:
        """Shutdown the Kaplay environment."""
        self.is_running = False

    async def on_code_change(self, code: str, cursor_position: int = None) -> None:
        """Handle a code change event from the Kaplay client."""
        event = KaplayCodeChange(
            sandbox_id=self.sandbox_id,
            sandbox_type=self.sandbox_type,
            code=code,
            cursor_position=cursor_position
        )
        await self.push_telemetry(event)

    async def on_error(self, message: str, line: int = None, col: int = None) -> None:
        """Handle a compilation error event from the Kaplay client."""
        event = KaplayCompilationError(
            sandbox_id=self.sandbox_id,
            sandbox_type=self.sandbox_type,
            error_message=message,
            line_number=line,
            column_number=col
        )
        await self.push_telemetry(event)

    async def on_state_change(self, state: dict) -> None:
        """Handle a state change event from the Kaplay client."""
        event = KaplayStateChange(
            sandbox_id=self.sandbox_id,
            sandbox_type=self.sandbox_type,
            state=state
        )
        await self.push_telemetry(event)
