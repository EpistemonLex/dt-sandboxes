/**
 * Deepthought Ed-OS: BeepBox (Chiptune Music) Harvester
 * 
 * Intercepts musical state from the URL hash in BeepBox.
 * The hash contains the entire song state in a compressed format.
 */

(function() {
    const HARVESTER_ID = "dt-beepbox-harvester";

    window.initEdOSBeepBoxHarvester = function() {
        console.log(`[${HARVESTER_ID}] Hooking into BeepBox...`);

        if (window.EdOS) {
            window.EdOS.initErrorCatching("beepbox");
        }

        /**
         * Broadcasts the current song state (hash).
         */
        function broadcastState() {
            if (window.EdOS) {
                const hash = window.location.hash;
                
                // Extract some basic info if possible (BeepBox hash usually starts with #6 or #8)
                // In the future, we can add a JS-based decoder for the BeepBox format here.
                
                window.EdOS.sendTelemetry("beepbox", "hash_update", {
                    hash: hash,
                    timestamp: new Date().toISOString()
                });
            }
        }

        // 1. Listen for hash changes (when user edits the song)
        window.addEventListener('hashchange', broadcastState, false);

        // 2. Poll for editor state if accessible
        setInterval(() => {
            // Some versions of BeepBox expose the doc or editor
            const doc = window.doc || (window.beepbox && window.beepbox.doc);
            if (doc && doc.song && window.EdOS) {
                window.EdOS.sendTelemetry("beepbox", "state_update", {
                    bpm: doc.song.tempo,
                    key: doc.song.key,
                    tracks_count: doc.song.channels.length,
                    active_pattern: [] // Future: Parse active pattern notes
                });
            }
        }, 10000);

        // Initial broadcast
        if (window.location.hash) {
            broadcastState();
        }

        if (window.EdOS) {
            window.EdOS.sendTelemetry("beepbox", "engine_ready", {}, "success");
        }
    };

    // Auto-init
    if (window.EdOS) {
        window.initEdOSBeepBoxHarvester();
    }
})();
