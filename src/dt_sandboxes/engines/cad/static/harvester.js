/**
 * Deepthought Ed-OS: BlocksCAD (3D Modeling) Harvester
 * 
 * Extracts the Blockly XML workspace from the BlocksCAD environment.
 */

(function() {
    const HARVESTER_ID = "dt-cad-harvester";

    window.initEdOSCADHarvester = function(blocklyWorkspace) {
        console.log(`[${HARVESTER_ID}] Hooking into BlocksCAD...`);

        if (window.EdOS) {
            window.EdOS.initErrorCatching("cad");
        }

        // Listen for workspace changes
        blocklyWorkspace.addChangeListener((event) => {
            // We only care about events that change the actual logic/structure
            if (event.type === "move" || event.type === "create" || event.type === "delete" || event.type === "change") {
                if (window.EdOS) {
                    const xml = Blockly.Xml.workspaceToDom(blocklyWorkspace);
                    const xmlText = Blockly.Xml.domToText(xml);
                    
                    window.EdOS.sendTelemetry("cad", "workspace_update", {
                        xml: xmlText,
                        timestamp: new Date().toISOString()
                    });
                }
            }
        });

        if (window.EdOS) {
            window.EdOS.sendTelemetry("cad", "engine_ready", {}, "success");
        }
    };
})();
