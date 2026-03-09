"""Headless verification script for ALL dt-sandboxes harvesters."""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path("dt-sandboxes/src")))

from dt_sandboxes.engines.kaplay.harvester import KaplayHarvester
from dt_sandboxes.engines.music.harvester import MusicHarvester, BeepBoxHarvester
from dt_sandboxes.engines.cad.harvester import CADHarvester, OpenJSCADHarvester
from dt_sandboxes.engines.snap.harvester import SnapHarvester
from dt_sandboxes.engines.chemistry.phet_harvester import PhetHarvester
from dt_sandboxes.engines.chemistry.sandboxels_harvester import SandboxelsHarvester
from dt_sandboxes.engines.design.tldraw_harvester import TldrawHarvester
from dt_sandboxes.engines.notebook.starboard_harvester import StarboardHarvester

def verify_engine(name: str, harvester_class):
    print(f"🔍 Verifying {name} Harvester...")
    h = harvester_class()
    js = h.get_injection_js()
    
    # 1. Verify Bridge Presence
    if "window.EdOS =" not in js:
        print(f"❌ {name}: Standard bridge missing from injection!")
        return False
    
    # 2. Verify Error Catching
    if "initErrorCatching" not in js:
        print(f"❌ {name}: Error catching hook missing!")
        return False
        
    print(f"✅ {name}: Bridge and Hooks verified.")
    return True

if __name__ == "__main__":
    engines = [
        ("Kaplay", KaplayHarvester),
        ("Music (Strudel)", MusicHarvester),
        ("Music (BeepBox)", BeepBoxHarvester),
        ("CAD (BlocksCAD)", CADHarvester),
        ("CAD (OpenJSCAD)", OpenJSCADHarvester),
        ("Snap!", SnapHarvester),
        ("PhET", PhetHarvester),
        ("Sandboxels", SandboxelsHarvester),
        ("tldraw", TldrawHarvester),
        ("Starboard", StarboardHarvester),
    ]
    
    results = [verify_engine(n, c) for n, c in engines]
    
    if all(results):
        print("\n🏆 ALL Harvesters pass architectural compliance.")
    else:
        print("\n⚠️ Some harvesters failed verification.")
        sys.exit(1)
