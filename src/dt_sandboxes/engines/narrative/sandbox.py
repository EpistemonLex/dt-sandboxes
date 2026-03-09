"""Narrative sandbox implementation (Ren'Py)."""

from dt_contracts.sandboxes.base import SandboxType

from dt_sandboxes.base import BaseSandbox
from dt_sandboxes.schemas import BaseTelemetry

from .harvester import NarrativeHarvester


class NarrativeSandbox(BaseSandbox[BaseTelemetry]):
    """Sandbox environment for Narrative (Ren'Py)."""

    def __init__(self, sandbox_id: str, engine_type: SandboxType = SandboxType.RENPY) -> None:
        """Initialize the narrative sandbox.

        Args:
            sandbox_id: Unique identifier for the sandbox.
            engine_type: The specific engine (RENPY).

        """
        super().__init__(sandbox_id, engine_type)
        self.harvester = NarrativeHarvester(engine_type)

    async def start(self) -> None:
        """Start the narrative environment."""
        self.is_running = True

    async def stop(self) -> None:
        """Stop the narrative environment."""
        self.is_running = False
