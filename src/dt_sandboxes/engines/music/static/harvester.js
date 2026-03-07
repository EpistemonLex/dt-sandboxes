/**
 * Deepthought Ed-OS: BeepBox Harvester
 * 
 * Monitors musical state changes in the BeepBox chiptune engine.
 */

(function() {
    const HARVESTER_ID = "dt-music-harvester";

    function broadcast(eventName, payload, level = "info") {
        if (window.backpack && window.backpack.sendTelemetry) {
            window.backpack.sendTelemetry({
                sandbox_type: "beepbox",
                event_name: eventName,
                level: level,
                payload: payload
            });
        }
    }

    /**
     * BeepBox encodes most of its state in the URL hash.
     * We monitor hash changes to detect state mutations.
     */
    window.addEventListener("hashchange", () => {
        // Example hash: #8n31s0k0l00e03t2cm0a7g0fj07i0r1o3210T1v1u...
        // We'll extract raw metadata if possible, but the URL itself is the 'source of truth'
        broadcast("state_update", {
            url_state: window.location.hash,
            timestamp: new Date().toISOString()
        });
    });

    // Initial broadcast
    setTimeout(() => {
        broadcast("engine_ready", { version: "BeepBox Offline" }, "success");
    }, 1000);
})();
