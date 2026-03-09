/**
 * Deepthought Ed-OS: Kaplay.js Harvester (Unified)
 * 
 * Injected into the sandbox to extract state and broadcast telemetry.
 * Uses the EdOS standard bridge.
 */

(function() {
    const HARVESTER_ID = "dt-kaplay-harvester";
    let lastStateHash = "";

    /**
     * Extracts a simplified KaplayState for the AI Tutor.
     */
    function extractState(k) {
        const objects = k.get("*").map(obj => ({
            id: obj.id,
            tags: obj.tags || [],
            pos_x: obj.pos ? obj.pos.x : 0,
            pos_y: obj.pos ? obj.pos.y : 0,
            is_paused: !!obj.paused
        }));

        return {
            objects: objects,
            gravity: k.getGravity() || 0,
            is_game_over: k.isGameOver ? k.isGameOver() : false,
            score: k.score ? k.score() : 0
        };
    }

    /**
     * Hooks into the Kaplay instance.
     */
    window.initEdOSHarvester = function(k) {
        console.log(`[${HARVESTER_ID}] Hooking into Kaplay instance...`);

        // Initialize standard error catching
        if (window.EdOS) {
            window.EdOS.initErrorCatching("kaplay");
        }

        // 1. Hook into the game loop for state tracking
        k.onUpdate(() => {
            if (k.getFPS() > 0 && k.frameCount() % 60 === 0) {
                const state = extractState(k);
                const hash = JSON.stringify(state);
                if (hash !== lastStateHash) {
                    if (window.EdOS) {
                        window.EdOS.sendTelemetry("kaplay", "state_update", state);
                    }
                    lastStateHash = hash;
                }
            }
        });

        // 2. Hook into collisions
        k.onCollide((obj1, obj2) => {
            if (window.EdOS) {
                window.EdOS.sendTelemetry("kaplay", "collision", {
                    obj1_tags: obj1.tags,
                    obj2_tags: obj2.tags,
                    pos: obj1.pos
                });
            }
        });

        if (window.EdOS) {
            window.EdOS.sendTelemetry("kaplay", "engine_ready", { version: "Ed-OS 1.0" }, "success");
        }
    };
})();
