"""Design sandbox implementation."""

from dt_contracts.sandboxes.base import SandboxType

from dt_sandboxes.base import BaseSandbox
from dt_sandboxes.schemas import BaseTelemetry

from .harvester import DesignHarvester


class DesignSandbox(BaseSandbox[BaseTelemetry]):
    """Sandbox environment for tldraw."""

    def __init__(self, sandbox_id: str) -> None:
        """Initialize the design sandbox.

        Args:
            sandbox_id: Unique identifier for the sandbox.

        """
        super().__init__(sandbox_id, SandboxType.TLDRAW)
        self.harvester = DesignHarvester()

    async def start(self) -> None:
        """Start the design environment."""
        self.is_running = True

    async def stop(self) -> None:
        """Stop the design environment."""
        self.is_running = False
