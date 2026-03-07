"""Tests for the Music sandbox engine."""

import pytest
from dt_contracts.sandboxes.base import SandboxType

from dt_sandboxes.engines.music.sandbox import MusicSandbox


@pytest.mark.asyncio
async def test_music_sandbox_initialization() -> None:
    """Ensure Music sandbox initializes correctly."""
    sb = MusicSandbox(sandbox_id="test-m-1")
    assert sb.sandbox_type == SandboxType.BEEPBOX
    assert sb.harvester is not None

@pytest.mark.asyncio
async def test_music_harvester_script_loading() -> None:
    """Ensure the Music harvester script can be retrieved."""
    sb = MusicSandbox(sandbox_id="test-m-1")
    js = sb.harvester.get_injection_js()
    assert "dt-music-harvester" in js
    assert "hashchange" in js
