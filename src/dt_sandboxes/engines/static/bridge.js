/**
 * Deepthought Ed-OS: Unified Sandbox Bridge
 * 
 * Provides a standardized interface for all S.T.E.A.M. engines
 * to communicate with the Backpack daemon.
 */

window.EdOS = (function() {
    const BRIDGE_ID = "Ed-OS-Standard-Bridge";

    return {
        /**
         * Sends telemetry to the Backpack.
         * @param {string} engine - e.g., 'kaplay', 'strudel', 'tldraw'
         * @param {string} eventName - e.g., 'state_update', 'error'
         * @param {object} payload - The event data
         * @param {string} level - 'info', 'warning', 'error', 'success'
         */
        sendTelemetry: function(engine, eventName, payload, level = "info") {
            const data = {
                sandbox_type: engine,
                event_name: eventName,
                level: level,
                payload: payload,
                timestamp: new Date().toISOString()
            };

            // 1. Try pywebview bridge (Crucible Integration Harness)
            if (window.pywebview && window.pywebview.api) {
                if (window.pywebview.api.send_telemetry) {
                    window.pywebview.api.send_telemetry(data);
                } else if (window.pywebview.api.sendTelemetry) {
                    window.pywebview.api.sendTelemetry(data);
                }
            } 
            // 2. Try window.backpack (Backpack Daemon Bridge)
            else if (window.backpack && window.backpack.sendTelemetry) {
                window.backpack.sendTelemetry(data);
            }
            // 3. Fallback to console for debugging
            else {
                console.log(`[${BRIDGE_ID}] Telemetry (Disconnected):`, data);
            }
        },

        /**
         * Global error catcher for the sandbox.
         */
        initErrorCatching: function(engine) {
            window.onerror = (message, source, lineno, colno, error) => {
                this.sendTelemetry(engine, "runtime_error", {
                    message: message,
                    line: lineno,
                    column: colno,
                    stack: error ? error.stack : ""
                }, "error");
            };
            
            window.onunhandledrejection = (event) => {
                this.sendTelemetry(engine, "promise_rejection", {
                    reason: event.reason ? event.reason.toString() : "Unknown promise error"
                }, "error");
            };
        }
    };
})();
