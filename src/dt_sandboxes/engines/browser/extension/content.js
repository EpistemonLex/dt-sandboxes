// Deepthought Ed-OS: Pedagogical Nanny - Content Script
// Observes the current page and reports to the background script.

(function() {
    const payload = {
        type: "PAGE_VISIT",
        title: document.title,
        url: window.location.href,
        timestamp: new Date().toISOString()
    };

    // Send to background service worker
    chrome.runtime.sendMessage(payload);
    
    console.log("[Ed-OS] Digital Curiosity observed:", document.title);
})();
