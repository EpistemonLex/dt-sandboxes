"""Audio sandbox implementation (AudioMass)."""

from dt_contracts.sandboxes.base import SandboxType

from dt_sandboxes.base import BaseSandbox
from dt_sandboxes.schemas import BaseTelemetry

from .harvester import AudioHarvester


class AudioSandbox(BaseSandbox[BaseTelemetry]):
    """Sandbox environment for Audio Editing (AudioMass)."""

    def __init__(self, sandbox_id: str, engine_type: SandboxType = SandboxType.AUDIOMASS) -> None:
        """Initialize the audio sandbox.

        Args:
            sandbox_id: Unique identifier for the sandbox.
            engine_type: The specific engine (AUDIOMASS).

        """
        super().__init__(sandbox_id, engine_type)
        self.harvester = AudioHarvester(engine_type)

    async def start(self) -> None:
        """Start the audio environment."""
        self.is_running = True

    async def stop(self) -> None:
        """Stop the audio environment."""
        self.is_running = False
