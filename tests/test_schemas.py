"""Tests for the telemetry schemas."""

from __future__ import annotations

from datetime import datetime
from typing import cast

import pytest
from dt_contracts.sandboxes.base import SandboxType
from pydantic import ValidationError

from dt_sandboxes.schemas import (
    KaplayCodeChange,
    KaplayCompilationError,
    TelemetryType,
)


def test_kaplay_code_change_valid() -> None:
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

def test_kaplay_compilation_error_valid() -> None:
    """Test a valid KaplayCompilationError event."""
    error_line = 10
    error_column = 5
    event = KaplayCompilationError(
        sandbox_id="test-sandbox",
        sandbox_type=SandboxType.KAPLAY,
        error_message="ReferenceError: 'x' is not defined",
        line_number=error_line,
        column_number=error_column,
    )
    assert event.error_message == "ReferenceError: 'x' is not defined"
    assert event.line_number == error_line
    assert event.column_number == error_column

def test_kaplay_schema_invalid_type() -> None:
    """Test that validation fails for incorrect sandbox_type."""
    invalid_type: object = "invalid"  # architectural: allowed-object (Testing invalid input)
    with pytest.raises(ValidationError):
        KaplayCodeChange(
            sandbox_id="test-sandbox",
            sandbox_type=cast("SandboxType", invalid_type),  # architectural: allowed-object (Mypy cast for testing)
            code="print('hello')",
        )

def test_kaplay_schema_missing_required() -> None:
    """Test that validation fails for missing required fields."""
    # Use a dictionary that is missing required fields.
    # We use model_validate to trigger Pydantic runtime validation
    # without needing ** unpacking which is hard to type for negative tests.
    kwargs: dict[str, object] = {  # architectural: allowed-object (Dynamic test data)
        "sandbox_id": "test-sandbox",
        "sandbox_type": SandboxType.KAPLAY,
    }
    with pytest.raises(ValidationError):
        KaplayCodeChange.model_validate(kwargs)
