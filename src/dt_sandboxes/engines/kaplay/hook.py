"""Hook for capturing telemetry from the Kaplay engine."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from dt_contracts.sandboxes.base import SandboxTelemetry

from .harvester import KaplayHarvester


class KaplayTelemetryHook:
    """Hook for capturing and broadcasting telemetry from the Kaplay engine."""

    def __init__(
        self,
        sandbox_id: str,
        broadcast_fn: Callable[[SandboxTelemetry], Awaitable[None]],
    ) -> None:
        """Initialize the Kaplay telemetry hook.

        Args:
            sandbox_id: The unique identifier for the sandbox.
            broadcast_fn: A function to broadcast SandboxTelemetry events.

        """
        self.sandbox_id = sandbox_id
        self.broadcast_fn = broadcast_fn
        self.harvester = KaplayHarvester()

    def get_injection_script(self) -> str:
        """Return the JS script to be injected into the Kaplay environment."""
        return self.harvester.get_injection_js()

    async def handle_raw_telemetry(self, telemetry: SandboxTelemetry) -> None:
        """Process incoming raw telemetry and broadcast it."""
        # The hook's primary job is to ensure the telemetry is routed correctly
        # We can also perform validation here if needed
        await self.broadcast_fn(telemetry)
