"""Chemistry sandbox implementation."""

from dt_contracts.sandboxes.base import SandboxType

from dt_sandboxes.base import BaseSandbox
from dt_sandboxes.schemas import BaseTelemetry

from .harvester import ChemistryHarvester


class ChemistrySandbox(BaseSandbox[BaseTelemetry]):
    """Sandbox environment for Sandboxels."""

    def __init__(self, sandbox_id: str) -> None:
        """Initialize the chemistry sandbox.

        Args:
            sandbox_id: Unique identifier for the sandbox.

        """
        super().__init__(sandbox_id, SandboxType.SANDBOXELS)
        self.harvester = ChemistryHarvester()

    async def start(self) -> None:
        """Start the chemistry environment."""
        self.is_running = True

    async def stop(self) -> None:
        """Stop the chemistry environment."""
        self.is_running = False
