"""CAD sandbox implementation."""

from dt_contracts.sandboxes.base import SandboxType

from dt_sandboxes.base import BaseSandbox
from dt_sandboxes.schemas import BaseTelemetry

from .harvester import CADHarvester


class CADSandbox(BaseSandbox[BaseTelemetry]):
    """Sandbox environment for BlocksCAD and OpenJSCAD."""

    def __init__(self, sandbox_id: str) -> None:
        """Initialize the CAD sandbox.

        Args:
            sandbox_id: Unique identifier for the sandbox.

        """
        super().__init__(sandbox_id, SandboxType.CAD)
        self.harvester = CADHarvester()

    async def start(self) -> None:
        """Start the CAD environment."""
        self.is_running = True

    async def stop(self) -> None:
        """Stop the CAD environment."""
        self.is_running = False
