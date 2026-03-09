"""Science sandbox implementation (Mol. Workbench, NetLogo)."""

from dt_contracts.sandboxes.base import SandboxType

from dt_sandboxes.base import BaseSandbox
from dt_sandboxes.schemas import BaseTelemetry

from .harvester import ScienceHarvester


class ScienceSandbox(BaseSandbox[BaseTelemetry]):
    """Sandbox environment for Science (Mol. Workbench, NetLogo)."""

    def __init__(self, sandbox_id: str, engine_type: SandboxType) -> None:
        """Initialize the science sandbox.

        Args:
            sandbox_id: Unique identifier for the sandbox.
            engine_type: The specific engine (MOLWORKBENCH or NETLOGO).

        """
        super().__init__(sandbox_id, engine_type)
        self.harvester = ScienceHarvester(engine_type)

    async def start(self) -> None:
        """Start the science environment."""
        self.is_running = True

    async def stop(self) -> None:
        """Stop the science environment."""
        self.is_running = False
