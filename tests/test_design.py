"""Tests for the Design sandbox engine."""

import pytest
from dt_contracts.sandboxes.base import SandboxTelemetry, SandboxType
from dt_contracts.sandboxes.design import DesignState

from dt_sandboxes.engines.design.sandbox import DesignSandbox


@pytest.mark.asyncio
async def test_design_sandbox_initialization() -> None:
    """Ensure Design sandbox initializes correctly."""
    sb = DesignSandbox(sandbox_id="test-d-1")
    assert sb.sandbox_type == SandboxType.TLDRAW
    assert sb.harvester is not None

@pytest.mark.asyncio
async def test_design_harvester_parsing() -> None:
    """Ensure the Design harvester can parse state updates."""
    sb = DesignSandbox(sandbox_id="test-d-1")

    telemetry = SandboxTelemetry(
        sandbox_id="test-d-1",
        sandbox_type=SandboxType.TLDRAW,
        event_name="state_update",
        payload={
            "shapes": [{"id": "s1", "type": "box", "bounds_x": 10, "bounds_y": 20}],
            "active_tool": "select",
            "camera_zoom": 1.0,
        },
    )

    result = sb.harvester.parse_telemetry(telemetry)
    assert isinstance(result, DesignState)
    assert result.active_tool == "select"
    assert len(result.shapes) == 1
