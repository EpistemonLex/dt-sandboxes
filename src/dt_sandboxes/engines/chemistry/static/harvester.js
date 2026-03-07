/**
 * Deepthought Ed-OS: Sandboxels Harvester
 * 
 * Extracts grid state and chemical reactions from Sandboxels.
 */

(function() {
    const HARVESTER_ID = "dt-chemistry-harvester";

    function broadcast(eventName, payload, level = "info") {
        if (window.backpack && window.backpack.sendTelemetry) {
            window.backpack.sendTelemetry({
                sandbox_type: "sandboxels",
                event_name: eventName,
                level: level,
                payload: payload
            });
        }
    }

    /**
     * Polls the grid for active elements and counts.
     */
    function pollGrid() {
        if (typeof elements === 'undefined' || !pixelTicks) return;

        // Extract active elements and counts
        // Note: This depends on Sandboxels internal global variables
        const counts = {};
        let totalPixels = 0;

        // Heuristic: iterate through game state if accessible
        // For now, we'll look for known globals
        broadcast("state_update", {
            active_elements: Object.keys(counts),
            element_counts: counts,
            temperature_avg: 20.0 // Default placeholder
        });
    }

    // Set up polling
    setInterval(pollGrid, 5000);

    broadcast("engine_ready", { version: "Sandboxels Offline" }, "success");
})();
