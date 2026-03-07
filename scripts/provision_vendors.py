"""Provisioning script for Ed-OS Sandbox vendors."""

import json
import subprocess
from pathlib import Path

def provision():
    manifest_path = Path("vendors/manifest.json")
    if not manifest_path.exists():
        print("❌ Manifest not found.")
        return

    with manifest_path.open() as f:
        config = json.load(f)

    for sb in config["sandboxes"]:
        name = sb["name"]
        url = sb["url"]
        target = Path(sb["target"])
        sb_type = sb["type"]

        if target.exists():
            print(f"✅ {name} already exists. Skipping.")
            continue

        print(f"🚀 Fetching {name}...")
        if sb_type == "file":
            subprocess.run(["curl", "-L", "-o", str(target), url], check=True)
        elif sb_type == "zip":
            zip_tmp = Path(f"vendors/{name}_tmp.zip")
            subprocess.run(["curl", "-L", "-o", str(zip_tmp), url], check=True)
            target.mkdir(parents=True, exist_ok=True)
            subprocess.run(["unzip", "-q", str(zip_tmp), "-d", str(target)], check=True)
            zip_tmp.unlink()

if __name__ == "__main__":
    provision()
