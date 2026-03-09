"""Electronics sandbox implementation (CircuitJS1, Q.js)."""

from dt_contracts.sandboxes.base import SandboxType

from dt_sandboxes.base import BaseSandbox
from dt_sandboxes.schemas import BaseTelemetry

from .harvester import ElectronicsHarvester


class ElectronicsSandbox(BaseSandbox[BaseTelemetry]):
    """Sandbox environment for Electronics (CircuitJS, Quantum)."""

    def __init__(self, sandbox_id: str, engine_type: SandboxType) -> None:
        """Initialize the electronics sandbox.

        Args:
            sandbox_id: Unique identifier for the sandbox.
            engine_type: The specific engine (CIRCUITJS or QJS).

        """
        super().__init__(sandbox_id, engine_type)
        self.harvester = ElectronicsHarvester(engine_type)

    async def start(self) -> None:
        """Start the electronics environment."""
        self.is_running = True

    async def stop(self) -> None:
        """Stop the electronics environment."""
        self.is_running = False
