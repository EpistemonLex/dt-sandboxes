/**
 * Deepthought Ed-OS: Snap! (Programming) Harvester
 * 
 * Injected into the Snap! environment to observe block-based code changes.
 */

(function() {
    const HARVESTER_ID = "dt-snap-harvester";

    window.initEdOSSnapHarvester = function(ide) {
        console.log(`[${HARVESTER_ID}] Hooking into Snap! IDE...`);

        if (window.EdOS) {
            window.EdOS.initErrorCatching("snap");
        }

        // Listen for project changes (blocks added, script moved, etc)
        const originalChanged = ide.changed;
        ide.changed = function() {
            if (window.EdOS) {
                // Throttle: Snap! ide.changed can be very frequent
                if (!this._last_broadcast || (Date.now() - this._last_broadcast > 2000)) {
                    const xml = ide.serializer.serialize(ide.project);
                    window.EdOS.sendTelemetry("snap", "state_update", {
                        xml: xml,
                        timestamp: new Date().toISOString()
                    });
                    this._last_broadcast = Date.now();
                }
            }
            return originalChanged.apply(this, arguments);
        };

        if (window.EdOS) {
            window.EdOS.sendTelemetry("snap", "engine_ready", {}, "success");
        }
    };
})();
