/**
 * Deepthought Ed-OS: GeoGebra Harvester
 * 
 * Intercepts mathematical equations and geometric constraints from GeoGebra.
 */

(function() {
    const HARVESTER_ID = "dt-geogebra-harvester";

    window.initEdOSGeoGebraHarvester = function(ggbApp) {
        if (!ggbApp) ggbApp = window.ggbApplet;
        if (!ggbApp) return;

        console.log(`[${HARVESTER_ID}] Hooking into GeoGebra...`);

        if (window.EdOS) {
            window.EdOS.initErrorCatching("math");
        }

        // Hook into GeoGebra's update listener
        ggbApp.registerUpdateListener((objName) => {
            if (window.EdOS) {
                const value = ggbApp.getValueString(objName);
                window.EdOS.sendTelemetry("math", "geogebra_update", {
                    object: objName,
                    value: value,
                    timestamp: new Date().toISOString()
                });
            }
        });

        if (window.EdOS) {
            window.EdOS.sendTelemetry("math", "engine_ready", {}, "success");
        }
    };

    if (window.EdOS) setTimeout(window.initEdOSGeoGebraHarvester, 2000);
})();
