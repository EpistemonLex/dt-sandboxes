/**
 * Deepthought Ed-OS: tldraw (Design/Visual Thinking) Harvester
 * 
 * Intercepts canvas state and vector shapes from tldraw.
 */

(function() {
    const HARVESTER_ID = "dt-tldraw-harvester";

    window.initEdOSTldrawHarvester = function(editor) {
        if (!editor) {
            // Try to find editor globally if not provided
            editor = window.editor || (window.tldraw && window.tldraw.editor);
        }

        if (!editor) {
            console.warn(`[${HARVESTER_ID}] tldraw editor not found yet. Retrying in 1s...`);
            setTimeout(() => window.initEdOSTldrawHarvester(), 1000);
            return;
        }

        console.log(`[${HARVESTER_ID}] Successfully hooked into tldraw editor.`);

        if (window.EdOS) {
            window.EdOS.initErrorCatching("tldraw");
        }

        // tldraw uses a store-based reactive architecture.
        // We listen for changes to the shapes.
        editor.store.listen((entry) => {
            if (window.EdOS) {
                // Throttle: Only send summary of current shapes to avoid Bus congestion
                if (!window._tldraw_last_broadcast || (Date.now() - window._tldraw_last_broadcast > 3000)) {
                    const shapes = editor.getCurrentPageShapes();
                    
                    window.EdOS.sendTelemetry("tldraw", "state_update", {
                        active_tool: editor.getCurrentToolId(),
                        camera_zoom: editor.getZoomLevel(),
                        shapes: shapes.map(s => {
                            // Map tldraw shape to Ed-OS CanvasShape contract
                            return {
                                id: s.id,
                                type: s.type,
                                bounds_x: s.x,
                                bounds_y: s.y,
                                text: s.props.text || null
                            };
                        }),
                        timestamp: new Date().toISOString()
                    });
                    
                    window._tldraw_last_broadcast = Date.now();
                }
            }
        }, { scope: 'record', signals: true });

        if (window.EdOS) {
            window.EdOS.sendTelemetry("tldraw", "engine_ready", { version: editor.version || "v2+" }, "success");
        }
    };

    // Auto-init attempt
    if (window.EdOS) {
        // Many tldraw apps set window.editor on mount
        setTimeout(() => window.initEdOSTldrawHarvester(), 2000);
    }
})();
