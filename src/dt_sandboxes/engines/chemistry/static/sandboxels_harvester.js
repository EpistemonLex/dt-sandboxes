/**
 * Deepthought Ed-OS: Sandboxels (Emergent Physics) Harvester
 * 
 * Intercepts cellular automata grid states and reactions from Sandboxels.
 */

(function() {
    const HARVESTER_ID = "dt-sandboxels-harvester";

    window.initEdOSSandboxelsHarvester = function() {
        console.log(`[${HARVESTER_ID}] Hooking into Sandboxels...`);

        if (window.EdOS) {
            window.EdOS.initErrorCatching("sandboxels");
        }

        // 1. Monkey-patch reactPixels to detect reactions
        if (typeof window.reactPixels === 'function') {
            const originalReactPixels = window.reactPixels;
            window.reactPixels = function(pixel1, pixel2) {
                const elem1 = pixel1.element;
                const elem2 = pixel2.element;
                const result = originalReactPixels(pixel1, pixel2);
                
                if (result && window.EdOS) {
                    window.EdOS.sendTelemetry("sandboxels", "reaction", {
                        element1: elem1,
                        element2: elem2,
                        result: pixel1.element, // Usually pixel1 or pixel2 changes
                        pos_x: pixel1.x,
                        pos_y: pixel1.y
                    });
                }
                return result;
            };
            console.log(`[${HARVESTER_ID}] Successfully patched reactPixels`);
        } else {
            console.warn(`[${HARVESTER_ID}] reactPixels not found globally. Reaction tracking might be degraded.`);
        }

        // 2. Efficient Polling using currentPixels
        setInterval(() => {
            if (window.EdOS) {
                const elementCounts = {};
                
                // If currentPixels exists, use it (O(N) where N is active pixels)
                // Otherwise fallback to grid scan (O(W*H))
                if (window.currentPixels && Array.isArray(window.currentPixels)) {
                    for (let i = 0; i < window.currentPixels.length; i++) {
                        const pixel = window.currentPixels[i];
                        if (pixel && pixel.element && !pixel.del) {
                            elementCounts[pixel.element] = (elementCounts[pixel.element] || 0) + 1;
                        }
                    }
                } else if (window.pixelMap) {
                    for (let x = 0; x < pixelMap.length; x++) {
                        if (!pixelMap[x]) continue;
                        for (let y = 0; y < pixelMap[x].length; y++) {
                            const pixel = pixelMap[x][y];
                            if (pixel && pixel.element) {
                                elementCounts[pixel.element] = (elementCounts[pixel.element] || 0) + 1;
                            }
                        }
                    }
                }

                window.EdOS.sendTelemetry("sandboxels", "state_update", {
                    element_counts: elementCounts,
                    active_reactions: [], // Reactions are sent via event-based telemetry now
                    timestamp: new Date().toISOString()
                });
            }
        }, 5000); // 5s scan

        if (window.EdOS) {
            window.EdOS.sendTelemetry("sandboxels", "engine_ready", { version: window.currentversion || "unknown" }, "success");
        }
    };

    // Auto-init if EdOS is ready, otherwise wait for manual call
    if (window.EdOS) {
        // We might need to wait for Sandboxels to finish loading its globals
        setTimeout(window.initEdOSSandboxelsHarvester, 2000);
    }
})();
