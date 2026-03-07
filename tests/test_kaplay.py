"""Tests for the Kaplay sandbox engine."""

import pytest
from dt_contracts.sandboxes.base import SandboxType

from dt_sandboxes.engines.kaplay.sandbox import KaplaySandbox


@pytest.mark.asyncio
async def test_kaplay_sandbox_initialization() -> None:
    """Ensure Kaplay sandbox initializes with correct type and harvester."""
    sb = KaplaySandbox(sandbox_id="test-k-1")
    assert sb.sandbox_type == SandboxType.KAPLAY
    assert sb.sandbox_id == "test-k-1"
    assert sb.harvester is not None

@pytest.mark.asyncio
async def test_kaplay_harvester_script_loading() -> None:
    """Ensure the Kaplay harvester script can be retrieved."""
    sb = KaplaySandbox(sandbox_id="test-k-1")
    js = sb.harvester.get_injection_js()
    assert "window.initEdOSHarvester" in js
    assert "kaplay" in js
