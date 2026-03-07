"""Kaplay.js sandbox implementation."""

from dt_contracts.sandboxes.base import SandboxType

from dt_sandboxes.base import BaseSandbox
from dt_sandboxes.schemas import BaseTelemetry

from .harvester import KaplayHarvester


class KaplaySandbox(BaseSandbox[BaseTelemetry]):
    """Sandbox environment for Kaplay.js."""

    def __init__(self, sandbox_id: str) -> None:
        """Initialize the Kaplay sandbox.

        Args:
            sandbox_id: Unique identifier for the sandbox.

        """
        super().__init__(sandbox_id, SandboxType.KAPLAY)
        self.harvester = KaplayHarvester()

    async def start(self) -> None:
        """Start the Kaplay environment."""
        self.is_running = True

    async def stop(self) -> None:
        """Stop the Kaplay environment."""
        self.is_running = False
