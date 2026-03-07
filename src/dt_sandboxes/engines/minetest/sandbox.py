"""Minetest sandbox implementation (Native)."""

from dt_contracts.sandboxes.base import SandboxType

from dt_sandboxes.base import BaseSandbox
from dt_sandboxes.schemas import BaseTelemetry

from .harvester import MinetestHarvester


class MinetestSandbox(BaseSandbox[BaseTelemetry]):
    """Native sandbox environment for Minetest."""

    def __init__(self, sandbox_id: str) -> None:
        """Initialize the minetest sandbox.

        Args:
            sandbox_id: Unique identifier for the sandbox.

        """
        super().__init__(sandbox_id, SandboxType.MINETEST)
        self.harvester = MinetestHarvester()

    async def start(self) -> None:
        """Start the minetest environment.

        Note: This involves launching the local binary with the harvester mod.
        """
        self.is_running = True

    async def stop(self) -> None:
        """Stop the minetest environment."""
        self.is_running = False
