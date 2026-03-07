/**
 * Deepthought Ed-OS: tldraw Harvester
 * 
 * Extracts vector shapes and spatial reasoning metadata from tldraw.
 */

(function() {
    const HARVESTER_ID = "dt-design-harvester";

    function broadcast(eventName, payload, level = "info") {
        if (window.backpack && window.backpack.sendTelemetry) {
            window.backpack.sendTelemetry({
                sandbox_type: "tldraw",
                event_name: eventName,
                level: level,
                payload: payload
            });
        }
    }

    /**
     * Extracts shapes from the tldraw app instance.
     */
    function extractState() {
        if (!window.app || !window.app.store) return null;

        const shapes = window.app.getShapeAndDescendantIds(window.app.currentPageId)
            .map(id => window.app.getShape(id))
            .filter(s => s)
            .map(s => ({
                id: s.id,
                type: s.type,
                bounds_x: s.x,
                bounds_y: s.y,
                text: s.props ? s.props.text : null
            }));

        return {
            shapes: shapes,
            active_tool: window.app.activeToolId,
            camera_zoom: window.app.camera.z
        };
    }

    // Set up polling
    setInterval(() => {
        const state = extractState();
        if (state) broadcast("state_update", state);
    }, 5000);

    broadcast("engine_ready", { version: "tldraw Offline" }, "success");
})();
