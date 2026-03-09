"""Integration tests for standardized harvesters using the Crucible."""

import pytest
from dt_sandboxes.engines.kaplay.harvester import KaplayHarvester
from dt_sandboxes.engines.music.harvester import MusicHarvester
from dt_sandboxes.engines.cad.harvester import CADHarvester
from dt_sandboxes.engines.snap.harvester import SnapHarvester
from .harness import CrucibleHarness

# Standardized HTML shim for testing JS injection
def get_shim_html(injection_js: str, trigger_js: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <body>
        <script>
            // The harness provides window.pywebview.api.sendTelemetry
            {injection_js}
            
            // Wait for bridge to be ready then trigger
            setTimeout(() => {{
                {trigger_js}
            }}, 100);
        </script>
    </body>
    </html>
    """

@pytest.mark.skip(reason="Requires GUI environment for pywebview")
def test_kaplay_standardized_telemetry():
    """Verify Kaplay harvester uses the unified bridge."""
    harvester = KaplayHarvester()
    injection = harvester.get_injection_js()
    
    # Simulate a Kaplay instance and state update
    trigger = """
        const mockK = {
            get: () => [],
            getGravity: () => 9.8,
            getFPS: () => 60,
            frameCount: () => 60,
            onUpdate: (cb) => { window.triggerUpdate = cb; },
            onCollide: () => {},
            isGameOver: () => false,
            score: () => 10
        };
        window.initEdOSHarvester(mockK);
        window.triggerUpdate(); // Manually trigger the update loop
    """
    
    harness = CrucibleHarness(get_shim_html(injection, trigger))
    harness.run(timeout=2)
    
    # Verify we received state update via standardized bridge
    events = [t.event_name for t in harness.telemetry_received]
    assert "engine_ready" in events
    assert "state_update" in events
    
    state_event = next(t for t in harness.telemetry_received if t.event_name == "state_update")
    assert state_event.payload["gravity"] == 9.8

@pytest.mark.skip(reason="Requires GUI environment for pywebview")
def test_strudel_standardized_telemetry():
    """Verify Strudel harvester uses the unified bridge."""
    harvester = MusicHarvester()
    injection = harvester.get_injection_js()
    
    trigger = """
        const mockStrudel = {
            evaluate: (code) => { console.log("Eval:", code); },
            scheduler: { bpm: 120, cycle: 1, cps: 0.5 }
        };
        window.initEdOSStrudelHarvester(mockStrudel);
        mockStrudel.evaluate("s('bd cp')");
    """
    
    harness = CrucibleHarness(get_shim_html(injection, trigger))
    harness.run(timeout=2)
    
    events = [t.event_name for t in harness.telemetry_received]
    assert "engine_ready" in events
    assert "code_evaluated" in events
    
    eval_event = next(t for t in harness.telemetry_received if t.event_name == "code_evaluated")
    assert eval_event.payload["code"] == "s('bd cp')"

import logging
logger = logging.getLogger("crucible.tests")

if __name__ == "__main__":
    # Note: These tests cannot run in a headless CLI environment easily
    logger.info("Crucible tests drafted. Run via pytest in a GUI-enabled session.")

