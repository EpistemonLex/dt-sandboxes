// Deepthought Ed-OS: Pedagogical Nanny - Background Service Worker
// Relays curiosity telemetry from the content script to the local Backpack daemon.

const BACKPACK_URL = "http://localhost:8000/telemetry/browser";

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("[Ed-OS] Relaying curiosity:", message.title);

    fetch(BACKPACK_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            sandbox_type: "browser",
            event_name: "curiosity_harvested",
            payload: message,
            level: "info",
            timestamp: new Date().toISOString()
        })
    }).catch(err => {
        console.warn("[Ed-OS] Failed to broadcast to Backpack:", err);
    });

    return true;
});
