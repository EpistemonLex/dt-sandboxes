/**
 * Deepthought Ed-OS: Mathigon (Polypad) Harvester
 * 
 * Intercepts virtual manipulative state from Mathigon.
 */

(function() {
    const HARVESTER_ID = "dt-mathigon-harvester";

    window.initEdOSMathigonHarvester = function(polypad) {
        if (!polypad) polypad = window.polypad;
        if (!polypad) return;

        console.log(`[${HARVESTER_ID}] Hooking into Mathigon...`);

        if (window.EdOS) {
            window.EdOS.initErrorCatching("math");
        }

        // Monitor tile counts and positions
        polypad.on('change', () => {
            if (window.EdOS) {
                const tiles = polypad.getTiles();
                window.EdOS.sendTelemetry("math", "math_state_update", {
                    tile_count: tiles.length,
                    timestamp: new Date().toISOString()
                });
            }
        });

        if (window.EdOS) {
            window.EdOS.sendTelemetry("math", "engine_ready", {}, "success");
        }
    };

    if (window.EdOS) setTimeout(window.initEdOSMathigonHarvester, 2000);
})();
