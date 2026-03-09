"""Music sandbox implementation (BeepBox, Strudel)."""

from dt_contracts.sandboxes.base import SandboxType

from dt_sandboxes.base import BaseSandbox
from dt_sandboxes.schemas import BaseTelemetry

from .beepbox_harvester import BeepBoxHarvester
from .harvester import MusicHarvester as StrudelHarvester


class MusicSandbox(BaseSandbox[BaseTelemetry]):
    """Sandbox environment for BeepBox or Strudel."""

    def __init__(self, sandbox_id: str, engine_type: SandboxType = SandboxType.BEEPBOX) -> None:
        """Initialize the music sandbox.

        Args:
            sandbox_id: Unique identifier for the sandbox.
            engine_type: The specific engine to use (BeepBox or Strudel).

        """
        super().__init__(sandbox_id, engine_type)
        if engine_type == SandboxType.BEEPBOX:
            self.harvester = BeepBoxHarvester()
        else:
            self.harvester = StrudelHarvester()

    async def start(self) -> None:
        """Start the music environment."""
        self.is_running = True

    async def stop(self) -> None:
        """Stop the music environment."""
        self.is_running = False
