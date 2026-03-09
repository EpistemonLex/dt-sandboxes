/**
 * Deepthought Ed-OS: Strudel (Music) Harvester
 * 
 * Intercepts music patterns and temporal events from the Strudel engine.
 */

(function() {
    const HARVESTER_ID = "dt-strudel-harvester";

    window.initEdOSStrudelHarvester = function(strudel) {
        console.log(`[${HARVESTER_ID}] Hooking into Strudel...`);

        if (window.EdOS) {
            window.EdOS.initErrorCatching("strudel");
        }

        // Hook into the evaluate event (when student runs code)
        const originalEvaluate = strudel.evaluate;
        strudel.evaluate = function(code) {
            if (window.EdOS) {
                window.EdOS.sendTelemetry("strudel", "code_evaluated", {
                    code: code,
                    timestamp: new Date().toISOString()
                });
            }
            return originalEvaluate.apply(this, arguments);
        };

        // Observe the scheduler for BPM and Cycle changes
        setInterval(() => {
            if (strudel.scheduler && window.EdOS) {
                const stats = {
                    bpm: strudel.scheduler.bpm,
                    cycle: strudel.scheduler.cycle,
                    cps: strudel.scheduler.cps
                };
                window.EdOS.sendTelemetry("strudel", "rhythm_stats", stats);
            }
        }, 5000); // Low frequency heartbeat

        if (window.EdOS) {
            window.EdOS.sendTelemetry("strudel", "engine_ready", {}, "success");
        }
    };
})();
