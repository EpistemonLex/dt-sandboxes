"""Offline Integration Test for Kaplay.js Harvester."""

import threading
import time

import pytest

from dt_sandboxes.engines.kaplay.harvester import KaplayHarvester

from .harness import CrucibleHarness

# A minimal HTML shim that looks like a Kaplay environment to the harvester
KAPLAY_SHIM_HTML = """
<!DOCTYPE html>
<html>
<body>
    <h1>Kaplay Shim</h1>
    <script>
        // 1. Mock the Backpack Bridge (usually provided by daemon)
        window.backpack = {
            sendTelemetry: function(data) {
                // Route to pywebview API (supporting both cases)
                if (window.pywebview && window.pywebview.api) {
                    if (window.pywebview.api.send_telemetry) {
                        window.pywebview.api.send_telemetry(data);
                    } else if (window.pywebview.api.sendTelemetry) {
                        window.pywebview.api.sendTelemetry(data);
                    }
                }
            }
        };

        // 2. Mock Kaplay Engine (k)
        const mockK = {
            get: (selector) => [{ id: 1, tags: ["player"], pos: { x: 10, y: 20 }, paused: false }],
            getGravity: () => 9.8,
            getFPS: () => 60,
            frameCount: () => 60,
            onUpdate: (fn) => { window.triggerUpdate = fn; },
            onCollide: (fn) => { window.triggerCollision = fn; },
            score: () => 100,
            isGameOver: () => false
        };

        // 3. Signal readiness
        console.log("Kaplay Shim Ready");
    </script>
    <script id="harvester-script"></script>
</body>
</html>
"""


@pytest.mark.skip(reason="Requires GUI environment/display for pywebview")
def test_kaplay_harvester_extraction() -> None:
    """Verify that the JS Harvester extracts state from the shim."""
    harvester = KaplayHarvester()
    js_code = harvester.get_injection_js()

    # Prepare the test page with the harvester injected
    html = KAPLAY_SHIM_HTML.replace(
        '<script id="harvester-script"></script>',
        f"<script>{js_code}</script>",
    )

    harness = CrucibleHarness(html)

    # Define the simulation sequence
    def simulate_events() -> None:
        # Give webview a moment to start
        time.sleep(1)

        # Initialize harvester
        harness.execute_js("window.initEdOSHarvester(mockK)")

        # Trigger a fake update
        harness.execute_js("window.triggerUpdate()")

        # Trigger a fake collision
        harness.execute_js("window.triggerCollision({tags: ['enemy']}, {tags: ['player']})")

        # Wait a bit then destroy
        time.sleep(1)

    threading.Thread(target=simulate_events).start()

    # Run the harness (blocks until destroyed)
    harness.run(timeout=5)

    # Assertions
    telemetry = harness.telemetry_received
    assert any(t.event_name == "engine_ready" for t in telemetry)
    assert any(t.event_name == "state_update" for t in telemetry)

    # Verify specific data mapping
    state_update = next(t for t in telemetry if t.event_name == "state_update")
    assert state_update.payload["gravity"] == 9.8
    objects = state_update.payload["objects"]
    assert isinstance(objects, list)
    assert len(objects) == 1
