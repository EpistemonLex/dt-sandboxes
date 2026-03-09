"""Math sandbox implementation (Mathigon, GeoGebra)."""

from dt_contracts.sandboxes.base import SandboxType

from dt_sandboxes.base import BaseSandbox
from dt_sandboxes.schemas import BaseTelemetry

from .harvester import MathHarvester


class MathSandbox(BaseSandbox[BaseTelemetry]):
    """Sandbox environment for Math (Mathigon, GeoGebra)."""

    def __init__(self, sandbox_id: str, engine_type: SandboxType) -> None:
        """Initialize the math sandbox.

        Args:
            sandbox_id: Unique identifier for the sandbox.
            engine_type: The specific engine (MATHIGON or GEOGEBRA).

        """
        super().__init__(sandbox_id, engine_type)
        self.harvester = MathHarvester(engine_type)

    async def start(self) -> None:
        """Start the math environment."""
        self.is_running = True

    async def stop(self) -> None:
        """Stop the math environment."""
        self.is_running = False
