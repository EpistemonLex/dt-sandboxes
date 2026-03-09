/**
 * Deepthought Ed-OS: NetLogo Web (Agent Modeling) Harvester
 * 
 * Intercepts agent (turtle/patch) counts and world variables from NetLogo Web.
 */

(function() {
    const HARVESTER_ID = "dt-netlogo-harvester";

    window.initEdOSNetLogoHarvester = function(world) {
        if (!world) world = window.world || (window.nlw && window.nlw.world);
        if (!world) return;

        console.log(`[${HARVESTER_ID}] Hooking into NetLogo Web...`);

        if (window.EdOS) {
            window.EdOS.initErrorCatching("science");
        }

        // Monitor turtle and patch counts
        setInterval(() => {
            if (world.turtles && window.EdOS) {
                window.EdOS.sendTelemetry("science", "agent_state_update", {
                    turtle_count: world.turtles().length,
                    patch_count: world.patches().length,
                    world_vars: {}, // Placeholder
                    timestamp: new Date().toISOString()
                });
            }
        }, 5000);

        if (window.EdOS) {
            window.EdOS.sendTelemetry("science", "engine_ready", {}, "success");
        }
    };

    if (window.EdOS) setTimeout(window.initEdOSNetLogoHarvester, 2000);
})();
