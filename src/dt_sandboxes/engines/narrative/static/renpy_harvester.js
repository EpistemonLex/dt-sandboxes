/**
 * Deepthought Ed-OS: Ren'Py (Visual Novel) Harvester
 * 
 * Intercepts narrative state and Python variables from the Ren'Py Web runtime.
 */

(function() {
    const HARVESTER_ID = "dt-renpy-harvester";

    window.initEdOSRenPyHarvester = function() {
        console.log(`[${HARVESTER_ID}] Hooking into Ren'Py Web runtime...`);

        if (window.EdOS) {
            window.EdOS.initErrorCatching("renpy");
        }

        /**
         * Observes the Ren'Py store for changes.
         * Ren'Py Web exposes the Python environment via Emscripten.
         */
        setInterval(() => {
            if (window.renpy && window.EdOS) {
                try {
                    // Extract common narrative variables from the Ren'Py store
                    // Note: We use the Python bridge if available, otherwise we poll
                    const variables = {};
                    
                    // In RenPyWeb, renpy.get_variable is a common way to peek into the store
                    if (typeof renpy.get_variable === 'function') {
                         // We can poll specific tracked variables or the current label
                         variables.current_label = renpy.get_variable("last_label") || "start";
                    }

                    window.EdOS.sendTelemetry("renpy", "narrative_update", {
                        current_label: variables.current_label,
                        timestamp: new Date().toISOString()
                    });
                } catch (e) {
                    console.error(`[${HARVESTER_ID}] Failed to extract Ren'Py state:`, e);
                }
            }
        }, 5000);

        if (window.EdOS) {
            window.EdOS.sendTelemetry("renpy", "engine_ready", {}, "success");
        }
    };

    // Auto-init
    if (window.EdOS) {
        setTimeout(window.initEdOSRenPyHarvester, 5000); // Wait for WASM to load
    }
})();
