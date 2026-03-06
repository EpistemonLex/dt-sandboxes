from abc import ABC, abstractmethod
import asyncio
from typing import Generic, TypeVar
from dt_sandboxes.schemas import BaseTelemetry, SandboxType

T = TypeVar("T", bound=BaseTelemetry)

class BaseSandbox(ABC, Generic[T]):
    def __init__(self, sandbox_id: str, sandbox_type: SandboxType):
        self.sandbox_id = sandbox_id
        self.sandbox_type = sandbox_type
        self.is_running = False
        self._telemetry_queue: asyncio.Queue[BaseTelemetry] = asyncio.Queue()

    @abstractmethod
    async def start(self) -> None:
        """Start the sandbox environment."""
        self.is_running = True

    @abstractmethod
    async def stop(self) -> None:
        """Stop the sandbox environment."""
        self.is_running = False

    async def push_telemetry(self, event: BaseTelemetry) -> None:
        """Push a telemetry event to the internal queue."""
        await self._telemetry_queue.put(event)

    async def get_telemetry(self) -> BaseTelemetry:
        """Get the next telemetry event from the queue."""
        return await self._telemetry_queue.get()
