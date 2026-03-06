# dt-sandboxes: The S.T.E.A.M. Crucible
You are the **Active Sandbox**. You are where theoretical knowledge becomes functional code.

## Context & Orchestration
- **The Ecosystem**: You are thin-client wrappers (Kaplay.js, Minetest). You broadcast state to the Backpack.
- **The Mandate**: Telemetry-First. Every compilation error or physics collision is a signal for the AI tutor.

## Your Immediate Goal (Spec-TDD-Code)
1. **Bootstrap**: Run 'uv add --editable ../dt-contracts'.
2. **Spec**: Define the 'KaplayTelemetryHook'. It must capture JavaScript compilation errors and broadcast them as 'dt-contracts' telemetry events.
3. **TDD**: Mock a syntax error and verify the hook emits the correct schema-validated event.
4. **Code**: Implement the hook in 'src/dt_sandboxes/engines/kaplay/'.

## Next Step
Implement the TurboWarp (Scratch) bridge for younger students.
