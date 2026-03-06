import pytest
import asyncio
from dt_sandboxes.kaplay import KaplaySandbox
from dt_sandboxes.schemas import SandboxType, TelemetryType, KaplayCodeChange

@pytest.mark.asyncio
async def test_kaplay_sandbox_lifecycle():
    """Test the basic lifecycle of the Kaplay sandbox."""
    sandbox = KaplaySandbox(sandbox_id="kaplay-test")
    assert sandbox.sandbox_id == "kaplay-test"
    assert sandbox.sandbox_type == SandboxType.KAPLAY
    assert not sandbox.is_running

    await sandbox.start()
    assert sandbox.is_running

    await sandbox.stop()
    assert not sandbox.is_running

@pytest.mark.asyncio
async def test_kaplay_sandbox_telemetry_push():
    """Test pushing telemetry to the Kaplay sandbox."""
    sandbox = KaplaySandbox(sandbox_id="kaplay-test")
    await sandbox.start()

    event = KaplayCodeChange(
        sandbox_id="kaplay-test",
        sandbox_type=SandboxType.KAPLAY,
        code="add([])"
    )

    await sandbox.push_telemetry(event)

    received = await sandbox.get_telemetry()
    assert received.event_type == TelemetryType.CODE_CHANGE
    assert received.code == "add([])"
