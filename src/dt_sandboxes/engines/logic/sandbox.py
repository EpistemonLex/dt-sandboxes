"""Logic/CS sandbox implementation (MakeCode)."""

from dt_contracts.sandboxes.base import SandboxType

from dt_sandboxes.base import BaseSandbox
from dt_sandboxes.schemas import BaseTelemetry

from .harvester import LogicHarvester


class LogicSandbox(BaseSandbox[BaseTelemetry]):
    """Sandbox environment for Logic (MakeCode)."""

    def __init__(self, sandbox_id: str, engine_type: SandboxType = SandboxType.MAKECODE) -> None:
        """Initialize the logic sandbox.

        Args:
            sandbox_id: Unique identifier for the sandbox.
            engine_type: The specific engine (MAKECODE).

        """
        super().__init__(sandbox_id, engine_type)
        self.harvester = LogicHarvester(engine_type)

    async def start(self) -> None:
        """Start the logic environment."""
        self.is_running = True

    async def stop(self) -> None:
        """Stop the logic environment."""
        self.is_running = False
