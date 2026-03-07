/**
 * Deepthought Ed-OS: Kaplay.js Harvester
 * 
 * Injected into the sandbox to extract state and broadcast telemetry.
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
     * Broadcasts a SandboxTelemetry event to the Backpack bridge.
     */
    function broadcast(eventName, payload, level = "info") {
        if (window.backpack && window.backpack.sendTelemetry) {
            window.backpack.sendTelemetry({
                sandbox_type: "kaplay",
                event_name: eventName,
                level: level,
                payload: payload
            });
        } else {
            console.warn(`[${HARVESTER_ID}] Backpack bridge not found. Telemetry dropped:`, eventName);
        }
    }

    /**
     * Hooks into the Kaplay instance.
     */
    window.initEdOSHarvester = function(k) {
        console.log(`[${HARVESTER_ID}] Hooking into Kaplay instance...`);

        // 1. Hook into the game loop for state tracking
        k.onUpdate(() => {
            // Throttle: Only send if something significant changed or every N frames
            if (k.getFPS() > 0 && k.frameCount() % 60 === 0) {
                const state = extractState(k);
                const hash = JSON.stringify(state);
                if (hash !== lastStateHash) {
                    broadcast("state_update", state);
                    lastStateHash = hash;
                }
            }
        });

        // 2. Hook into collisions
        k.onCollide((obj1, obj2) => {
            broadcast("collision", {
                obj1_tags: obj1.tags,
                obj2_tags: obj2.tags,
                pos: obj1.pos
            });
        });

        // 3. Global Error Handling
        window.onerror = function(message, source, lineno, colno, error) {
            broadcast("compilation_error", {
                message: message,
                line: lineno,
                column: colno,
                stack: error ? error.stack : ""
            }, "error");
        };

        broadcast("engine_ready", { version: "Ed-OS 1.0" }, "success");
    };
})();
