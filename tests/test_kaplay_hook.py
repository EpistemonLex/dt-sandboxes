"""Tests for the Kaplay telemetry hook."""

import pytest
from dt_contracts.sandboxes.base import SandboxTelemetry, SandboxType

from dt_sandboxes.engines.kaplay.hook import KaplayTelemetryHook


@pytest.mark.asyncio
async def test_kaplay_hook_broadcasts_telemetry() -> None:
    """Verify the hook emits the correct SandboxTelemetry event."""
    # Setup: a hook that we can monitor
    emitted_events = []

    async def broadcast_callback(event: SandboxTelemetry) -> None:
        emitted_events.append(event)

    hook = KaplayTelemetryHook(sandbox_id="test-kaplay-1", broadcast_fn=broadcast_callback)

    # Action: simulate a raw telemetry event from the harvester
    raw_event = SandboxTelemetry(
        sandbox_id="test-kaplay-1",
        sandbox_type=SandboxType.KAPLAY,
        event_name="state_update",
        payload={"gravity": 9.8, "objects": []},
    )

    await hook.handle_raw_telemetry(raw_event)

    # Validation: check the emitted event
    assert len(emitted_events) == 1
    event = emitted_events[0]

    assert isinstance(event, SandboxTelemetry)
    assert event.sandbox_id == "test-kaplay-1"
    assert event.event_name == "state_update"
    assert event.payload["gravity"] == 9.8
