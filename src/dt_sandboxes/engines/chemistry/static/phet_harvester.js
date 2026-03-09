/**
 * Deepthought Ed-OS: PhET Interactive Simulations Harvester
 * 
 * Injected into PhET simulations to observe model variables.
 * Uses the internal simulation model tree to extract granular state.
 */

(function() {
    const HARVESTER_ID = "dt-phet-harvester";

    window.initEdOSPhetHarvester = function() {
        console.log(`[${HARVESTER_ID}] Attempting to hook into PhET...`);

        if (window.EdOS) {
            window.EdOS.initErrorCatching("phet");
        }

        // 1. Detection Loop: Wait for PhET to initialize
        const pollInterval = setInterval(() => {
            if (window.phet && window.phet.joist && window.phet.joist.sim) {
                console.log(`[${HARVESTER_ID}] PhET Sim detected:`, window.phet.joist.sim.name);
                clearInterval(pollInterval);
                setupObservation(window.phet.joist.sim);
            }
        }, 1000);

        function setupObservation(sim) {
            // 2. High-Fidelity State Extraction
            setInterval(() => {
                if (window.EdOS) {
                    const variables = [];
                    
                    /**
                     * Recursively extract numerical/boolean properties from the model.
                     */
                    function extractModel(obj, path = "") {
                        if (!obj || typeof obj !== 'object') return;
                        
                        for (let key in obj) {
                            if (key.startsWith("_")) continue; // Skip internal/private
                            
                            const prop = obj[key];
                            const currentPath = path ? `${path}.${key}` : key;

                            // 1. Check if it's a PhET Property (ax-core or similar)
                            // PhET properties usually have a .value and are often observable
                            if (prop && prop.value !== undefined && (typeof prop.value !== 'function')) {
                                variables.push({
                                    name: currentPath,
                                    value: prop.value,
                                    units: prop.units || null
                                });
                            }
                            // 2. Direct values
                            else if (typeof prop === 'number' || typeof prop === 'boolean' || typeof prop === 'string') {
                                if (currentPath.length < 50) { // Limit depth/noise
                                    variables.push({
                                        name: currentPath,
                                        value: prop,
                                        units: null
                                    });
                                }
                            }
                            // 3. Nested objects (limited recursion)
                            else if (typeof prop === 'object' && path.split(".").length < 3) {
                                extractModel(prop, currentPath);
                            }
                        }
                    }

                    if (sim.model) {
                        extractModel(sim.model);
                    }

                    window.EdOS.sendTelemetry("phet", "phet_state_update", {
                        sim_id: sim.name || "unknown",
                        variables: variables,
                        timestamp: new Date().toISOString()
                    });
                }
            }, 5000); // 5s polling for low overhead
        }

        if (window.EdOS) {
            window.EdOS.sendTelemetry("phet", "engine_ready", {}, "success");
        }
    };

    // Auto-init
    if (window.EdOS) {
        window.initEdOSPhetHarvester();
    }
})();
