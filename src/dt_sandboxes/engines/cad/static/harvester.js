/**
 * Deepthought Ed-OS: BlocksCAD / OpenJSCAD Harvester
 * 
 * Monitors 3D geometric state and script changes in CAD engines.
 */

(function() {
    const HARVESTER_ID = "dt-cad-harvester";

    function broadcast(eventName, payload, level = "info") {
        if (window.backpack && window.backpack.sendTelemetry) {
            window.backpack.sendTelemetry({
                sandbox_type: "cad",
                event_name: eventName,
                level: level,
                payload: payload
            });
        }
    }

    /**
     * For OpenJSCAD, we monitor the script text.
     */
    function extractJSCADState() {
        if (typeof gProcessor === 'undefined') return null;
        return {
            script: gProcessor.currentScript,
            objects_count: gProcessor.objects ? gProcessor.objects.length : 0
        };
    }

    // Set up polling for geometry changes
    setInterval(() => {
        const state = extractJSCADState();
        if (state) broadcast("state_update", state);
    }, 5000);

    broadcast("engine_ready", { version: "CAD Offline" }, "success");
})();
