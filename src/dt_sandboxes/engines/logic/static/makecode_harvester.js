/**
 * Deepthought Ed-OS: MakeCode (Visual/Textual Logic) Harvester
 * 
 * Intercepts code blocks and TypeScript from the Microsoft MakeCode environment.
 */

(function() {
    const HARVESTER_ID = "dt-makecode-harvester";

    window.initEdOSMakeCodeHarvester = function() {
        console.log(`[${HARVESTER_ID}] Hooking into MakeCode...`);

        if (window.EdOS) {
            window.EdOS.initErrorCatching("logic");
        }

        // MakeCode usually communicates via postMessage if embedded,
        // or has a global 'pxt' object.
        window.addEventListener("message", (event) => {
            if (event.data && event.data.type === "pxt-event") {
                if (window.EdOS) {
                    window.EdOS.sendTelemetry("logic", "makecode_event", event.data);
                }
            }
        });

        if (window.EdOS) {
            window.EdOS.sendTelemetry("logic", "engine_ready", {}, "success");
        }
    };

    // Auto-init
    if (window.EdOS) {
        window.initEdOSMakeCodeHarvester();
    }
})();
