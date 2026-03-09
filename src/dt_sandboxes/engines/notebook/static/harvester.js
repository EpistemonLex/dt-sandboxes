/**
 * Deepthought Ed-OS: Starboard Notebook Harvester
 * 
 * Intercepts cell content and execution from Starboard Notebooks.
 */

(function() {
    const HARVESTER_ID = "dt-starboard-harvester";

    window.initEdOSStarboardHarvester = function(runtime) {
        if (!runtime) {
            runtime = window.starboard || (window.starboard && window.starboard.runtime);
        }

        if (!runtime) {
            console.warn(`[${HARVESTER_ID}] Starboard runtime not found yet. Retrying in 1s...`);
            setTimeout(() => window.initEdOSStarboardHarvester(), 1000);
            return;
        }

        console.log(`[${HARVESTER_ID}] Successfully hooked into Starboard runtime.`);

        if (window.EdOS) {
            window.EdOS.initErrorCatching("starboard");
        }

        // Starboard uses a cell-based architecture.
        // We observe the notebook for changes.
        runtime.subscribe((event) => {
            if (window.EdOS) {
                // Throttle: Only broadcast significant changes or every N seconds
                if (!window._starboard_last_broadcast || (Date.now() - window._starboard_last_broadcast > 5000)) {
                    const cells = runtime.getCells().map(cell => ({
                        id: cell.id,
                        type: cell.cellType,
                        content: cell.textContent
                    }));

                    window.EdOS.sendTelemetry("starboard", "state_update", {
                        cell_count: cells.length,
                        cells: cells,
                        timestamp: new Date().toISOString()
                    });
                    
                    window._starboard_last_broadcast = Date.now();
                }
            }
        });

        if (window.EdOS) {
            window.EdOS.sendTelemetry("starboard", "engine_ready", {}, "success");
        }
    };

    // Auto-init
    if (window.EdOS) {
        setTimeout(window.initEdOSStarboardHarvester, 2000);
    }
})();
