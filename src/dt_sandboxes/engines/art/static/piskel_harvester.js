/**
 * Deepthought Ed-OS: Piskel (Pixel Art) Harvester
 * 
 * Intercepts frame counts and export events from the Piskel editor.
 */

(function() {
    const HARVESTER_ID = "dt-piskel-harvester";

    window.initEdOSPiskelHarvester = function() {
        console.log(`[${HARVESTER_ID}] Hooking into Piskel...`);

        if (window.EdOS) {
            window.EdOS.initErrorCatching("art");
        }

        // Piskel uses a centralized 'pskl' object if running in-context.
        // We poll for frame changes and export actions.
        setInterval(() => {
            if (window.pskl && window.EdOS) {
                const piskel = pskl.app.piskelController.getPiskel();
                window.EdOS.sendTelemetry("art", "art_state_update", {
                    frame_count: piskel.getFrameCount(),
                    width: piskel.getWidth(),
                    height: piskel.getHeight(),
                    timestamp: new Date().toISOString()
                });
            }
        }, 10000);

        if (window.EdOS) {
            window.EdOS.sendTelemetry("art", "engine_ready", {}, "success");
        }
    };

    if (window.EdOS) setTimeout(window.initEdOSPiskelHarvester, 3000);
})();
