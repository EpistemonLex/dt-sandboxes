"""The Crucible: Offline Integration Harness for Ed-OS Sandboxes."""

import asyncio
import threading

import webview
from dt_contracts.sandboxes.base import SandboxTelemetry


class CrucibleHarness:
    """Headless browser harness for testing sandboxes offline."""

    def __init__(self, html_content: str) -> None:
        """Initialize the harness with HTML content."""
        self.html_content = html_content
        self.telemetry_received: list[SandboxTelemetry] = []
        self._window: object = None  # architectural: allowed-object (Webview Window)
        self._loop = asyncio.get_event_loop()

    def sendTelemetry(self, raw_telemetry: dict[str, object]) -> None:  # noqa: N802 # architectural: allowed-object (JS Bridge)
        """Ingest raw telemetry from JavaScript.

        Called from JavaScript via window.pywebview.api.sendTelemetry.
        """
        try:
            # Validate against dt-contracts immediately
            telemetry = SandboxTelemetry.model_validate(raw_telemetry)
            self.telemetry_received.append(telemetry)
        except Exception as e:  # architectural: Loop safety
            # Log error without crashing the webview loop
            print(f"[Crucible] Ingestion failed: {e}")  # noqa: T201 # architectural: Test logging

    def run(self, timeout: int = 5) -> None:
        """Run the harness and wait for telemetry."""
        window = webview.create_window(
            "Ed-OS Crucible",
            html=self.html_content,
            js_api=self,
        )
        self._window = window

        # Start webview in a way that allows us to close it programmatically
        def _close() -> None:
            if window:
                window.destroy()

        threading.Timer(timeout, _close).start()
        webview.start(debug=True)

    def execute_js(self, script: str) -> object:  # architectural: allowed-object (JS Return Value)
        """Execute JS in the running window."""
        if self._window and hasattr(self._window, "evaluate_js"):
            return self._window.evaluate_js(script)
        return None
