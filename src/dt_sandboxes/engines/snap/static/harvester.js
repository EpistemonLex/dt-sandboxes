/**
 * Deepthought Ed-OS: Snap! Harvester
 * 
 * Extracts block-based logic and sprite state from Snap!.
 */

(function() {
    const HARVESTER_ID = "dt-snap-harvester";

    function broadcast(eventName, payload, level = "info") {
        if (window.backpack && window.backpack.sendTelemetry) {
            window.backpack.sendTelemetry({
                sandbox_type: "snap",
                event_name: eventName,
                level: level,
                payload: payload
            });
        }
    }

    /**
     * Serializes the current Snap! project state.
     */
    function extractState() {
        if (!window.world || !world.children[0]) return null;
        const ide = world.children[0];
        const stage = ide.stage;

        const sprites = stage.children.filter(c => c.name).map(s => ({
            name: s.name,
            x: s.x(),
            y: s.y(),
            direction: s.direction(),
            scripts_count: s.scripts ? s.scripts.children.length : 0
        }));

        return {
            project_name: ide.projectName || "Untitled",
            sprites: sprites,
            variables: ide.globalVariables.vars,
            is_running: !!ide.stage.isStepping
        };
    }

    // Set up polling
    setInterval(() => {
        const state = extractState();
        if (state) broadcast("state_update", state);
    }, 5000);

    broadcast("engine_ready", { version: "Snap! Offline" }, "success");
})();
