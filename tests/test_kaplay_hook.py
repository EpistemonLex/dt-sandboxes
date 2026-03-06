import pytest
import asyncio
from dt_sandboxes.engines.kaplay.hook import KaplayTelemetryHook
from dt_sandboxes.engines.kaplay.schemas import KaplayTelemetryEvent, TelemetryKind

@pytest.mark.asyncio
async def test_kaplay_hook_captures_syntax_error():
    """TDD: Mock a syntax error and verify the hook emits the correct event."""
    # Setup: a hook that we can monitor
    emitted_events = []
    
    async def broadcast_callback(event: KaplayTelemetryEvent):
        emitted_events.append(event)
        
    hook = KaplayTelemetryHook(sandbox_id="test-kaplay-1", broadcast_fn=broadcast_callback)
    
    # Action: simulate a JavaScript syntax error
    # e.g., "SyntaxError: Unexpected token ')' at line 5"
    await hook.capture_js_error(
        message="SyntaxError: Unexpected token ')'",
        line=5,
        column=12,
        stack="SyntaxError: Unexpected token ')'\n    at eval (<anonymous>)"
    )
    
    # Validation: check the emitted event
    assert len(emitted_events) == 1
    event = emitted_events[0]
    
    assert isinstance(event, KaplayTelemetryEvent)
    assert event.sandbox_id == "test-kaplay-1"
    assert event.kind == TelemetryKind.COMPILATION_ERROR
    assert event.payload["message"] == "SyntaxError: Unexpected token ')'"
    assert event.payload["line"] == 5
    assert event.payload["column"] == 12
