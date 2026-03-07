"""Tests for the Snap! sandbox engine."""

import pytest
from dt_contracts.sandboxes.base import SandboxTelemetry, SandboxType
from dt_contracts.sandboxes.snap import SnapState

from dt_sandboxes.engines.snap.sandbox import SnapSandbox


@pytest.mark.asyncio
async def test_snap_sandbox_initialization() -> None:
    """Ensure Snap! sandbox initializes correctly."""
    sb = SnapSandbox(sandbox_id="test-s-1")
    assert sb.sandbox_type == SandboxType.SNAP
    assert sb.harvester is not None

@pytest.mark.asyncio
async def test_snap_harvester_parsing() -> None:
    """Ensure the Snap! harvester can parse state updates."""
    sb = SnapSandbox(sandbox_id="test-s-1")

    telemetry = SandboxTelemetry(
        sandbox_id="test-s-1",
        sandbox_type=SandboxType.SNAP,
        event_name="state_update",
        payload={
            "project_name": "Test Project",
            "sprites": [{"name": "Sprite1", "x": 0, "y": 0, "direction": 90, "scripts_count": 1}],
            "variables": {"score": 10},
            "is_running": True,
        },
    )

    result = sb.harvester.parse_telemetry(telemetry)
    assert isinstance(result, SnapState)
    assert result.project_name == "Test Project"
    assert result.variables["score"] == 10
    assert result.sprites[0].name == "Sprite1"
