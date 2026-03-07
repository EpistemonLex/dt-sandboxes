#!/bin/bash
set -e
echo "--- Scanning for Compliance Violations (# noqa, type: ignore) ---"
VIOLATIONS=$(grep -rE --include="*.py" "noqa|type:\s*ignore" src tests | grep -v "scripts/check_compliance.sh" | grep -v "tests/test_architecture.py" || true)
if [ -n "$VIOLATIONS" ]; then
    echo "❌ Compliance Violation: Prohibited suppression found!"
    echo "$VIOLATIONS"
    exit 1
fi
echo "✅ No suppression comments found."
