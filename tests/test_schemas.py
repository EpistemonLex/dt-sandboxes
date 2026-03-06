from datetime import datetime
import pytest
from pydantic import ValidationError
from dt_sandboxes.schemas import KaplayCodeChange, SandboxType, TelemetryType, KaplayCompilationError

def test_kaplay_code_change_valid():
    """Test a valid KaplayCodeChange event."""
    event = KaplayCodeChange(
        sandbox_id="test-sandbox",
        sandbox_type=SandboxType.KAPLAY,
        code="add([rect(40, 40), pos(20, 20), color(0, 0, 255)])",
    )
    assert event.sandbox_id == "test-sandbox"
    assert event.sandbox_type == SandboxType.KAPLAY
    assert event.event_type == TelemetryType.CODE_CHANGE
    assert isinstance(event.timestamp, datetime)
    assert "add([" in event.code

def test_kaplay_compilation_error_valid():
    """Test a valid KaplayCompilationError event."""
    event = KaplayCompilationError(
        sandbox_id="test-sandbox",
        sandbox_type=SandboxType.KAPLAY,
        error_message="ReferenceError: 'x' is not defined",
        line_number=10,
        column_number=5
    )
    assert event.error_message == "ReferenceError: 'x' is not defined"
    assert event.line_number == 10
    assert event.column_number == 5

def test_kaplay_schema_invalid_type():
    """Test that validation fails for incorrect sandbox_type."""
    with pytest.raises(ValidationError):
        KaplayCodeChange(
            sandbox_id="test-sandbox",
            sandbox_type="invalid",  # type: ignore
            code="print('hello')",
        )

def test_kaplay_schema_missing_required():
    """Test that validation fails for missing required fields."""
    with pytest.raises(ValidationError):
        KaplayCodeChange(
            sandbox_id="test-sandbox",
            sandbox_type=SandboxType.KAPLAY,
            # code is missing
        )
