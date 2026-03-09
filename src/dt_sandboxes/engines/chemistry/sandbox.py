"""Chemistry sandbox implementation (PhET, Sandboxels)."""

from dt_contracts.sandboxes.base import SandboxType

from dt_sandboxes.base import BaseSandbox
from dt_sandboxes.schemas import BaseTelemetry

from .phet_harvester import PhetHarvester
from .sandboxels_harvester import SandboxelsHarvester


class ChemistrySandbox(BaseSandbox[BaseTelemetry]):
    """Sandbox environment for Sandboxels or PhET."""

    def __init__(self, sandbox_id: str, engine_type: SandboxType = SandboxType.SANDBOXELS) -> None:
        """Initialize the chemistry sandbox.

        Args:
            sandbox_id: Unique identifier for the sandbox.
            engine_type: The specific engine to use (Sandboxels or PhET).

        """
        super().__init__(sandbox_id, engine_type)
        if engine_type == SandboxType.PHET:
            self.harvester = PhetHarvester()
        else:
            self.harvester = SandboxelsHarvester()

    async def start(self) -> None:
        """Start the chemistry environment."""
        self.is_running = True

    async def stop(self) -> None:
        """Stop the chemistry environment."""
        self.is_running = False
