"""Base classes for sandboxes."""

import asyncio
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from dt_sandboxes.schemas import BaseTelemetry

if TYPE_CHECKING:
    from dt_contracts.sandboxes.base import SandboxType


class BaseSandbox[T: BaseTelemetry](ABC):
    """Abstract base class for all sandboxes.

    Args:
        T: Type of telemetry emitted by the sandbox.

    """

    def __init__(self, sandbox_id: str, sandbox_type: SandboxType) -> None:
        """Initialize the sandbox.

        Args:
            sandbox_id: Unique identifier for the sandbox.
            sandbox_type: Type of the sandbox.

        """
        self.sandbox_id = sandbox_id
        self.sandbox_type = sandbox_type
        self.is_running = False
        self._telemetry_queue: asyncio.Queue[T] = asyncio.Queue()

    @abstractmethod
    async def start(self) -> None:
        """Start the sandbox environment."""
        self.is_running = True

    @abstractmethod
    async def stop(self) -> None:
        """Stop the sandbox environment."""
        self.is_running = False

    async def push_telemetry(self, event: T) -> None:
        """Push a telemetry event to the internal queue.

        Args:
            event: The telemetry event to push.

        """
        await self._telemetry_queue.put(event)

    async def get_telemetry(self) -> T:
        """Get the next telemetry event from the queue.

        Returns:
            The next telemetry event.

        """
        return await self._telemetry_queue.get()
