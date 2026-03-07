"""Tests for the Chemistry sandbox engine."""

import pytest
from dt_contracts.sandboxes.base import SandboxTelemetry, SandboxType
from dt_contracts.sandboxes.chemistry import ChemistryState

from dt_sandboxes.engines.chemistry.sandbox import ChemistrySandbox


@pytest.mark.asyncio
async def test_chemistry_sandbox_initialization() -> None:
    """Ensure Chemistry sandbox initializes correctly."""
    sb = ChemistrySandbox(sandbox_id="test-c-1")
    assert sb.sandbox_type == SandboxType.SANDBOXELS
    assert sb.harvester is not None

@pytest.mark.asyncio
async def test_chemistry_harvester_parsing() -> None:
    """Ensure the Chemistry harvester can parse state updates."""
    sb = ChemistrySandbox(sandbox_id="test-c-1")

    telemetry = SandboxTelemetry(
        sandbox_id="test-c-1",
        sandbox_type=SandboxType.SANDBOXELS,
        event_name="state_update",
        payload={
            "temperature_avg": 25.5,
            "active_elements": ["sand", "fire"],
            "element_counts": {"sand": 100, "fire": 5},
        },
    )

    result = sb.harvester.parse_telemetry(telemetry)
    assert isinstance(result, ChemistryState)
    assert result.temperature_avg == 25.5
    assert "sand" in result.active_elements
