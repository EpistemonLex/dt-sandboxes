/**
 * Deepthought Ed-OS: OpenJSCAD (Programmatic CAD) Harvester
 * 
 * Intercepts JavaScript geometric code from the OpenJSCAD environment.
 */

(function() {
    const HARVESTER_ID = "dt-openjscad-harvester";

    window.initEdOSOpenJSCADHarvester = function(editor) {
        if (!editor) {
            editor = window.editor || (window.gProcessor && window.gProcessor.editor);
        }

        if (!editor) {
            console.warn(`[${HARVESTER_ID}] OpenJSCAD editor not found yet. Retrying in 1s...`);
            setTimeout(() => window.initEdOSOpenJSCADHarvester(), 1000);
            return;
        }

        console.log(`[${HARVESTER_ID}] Successfully hooked into OpenJSCAD editor.`);

        if (window.EdOS) {
            window.EdOS.initErrorCatching("openjscad");
        }

        // OpenJSCAD typically uses CodeMirror or a similar editor.
        if (editor.on) {
            editor.on('change', () => {
                if (window.EdOS) {
                    // Throttle: Code updates can be rapid
                    if (!window._jscad_last_broadcast || (Date.now() - window._jscad_last_broadcast > 2000)) {
                        const code = editor.getValue();
                        window.EdOS.sendTelemetry("openjscad", "code_update", {
                            code: code,
                            timestamp: new Date().toISOString()
                        });
                        window._jscad_last_broadcast = Date.now();
                    }
                }
            });
        }

        if (window.EdOS) {
            window.EdOS.sendTelemetry("openjscad", "engine_ready", {}, "success");
        }
    };

    // Auto-init
    if (window.EdOS) {
        setTimeout(window.initEdOSOpenJSCADHarvester, 2000);
    }
})();
