"""Tests for the CAD sandbox engine."""

import pytest
from dt_contracts.sandboxes.base import SandboxType

from dt_sandboxes.engines.cad.sandbox import CADSandbox


@pytest.mark.asyncio
async def test_cad_sandbox_initialization() -> None:
    """Ensure CAD sandbox initializes correctly."""
    sb = CADSandbox(sandbox_id="test-cad-1")
    assert sb.sandbox_type == SandboxType.CAD
    assert sb.harvester is not None

@pytest.mark.asyncio
async def test_cad_harvester_script_loading() -> None:
    """Ensure the CAD harvester script can be retrieved."""
    sb = CADSandbox(sandbox_id="test-cad-1")
    js = sb.harvester.get_injection_js()
    assert "dt-cad-harvester" in js
    assert "gProcessor" in js
