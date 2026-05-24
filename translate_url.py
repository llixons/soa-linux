#!/usr/bin/env python3
"""
SOA URL Translator
Translates the new soa:// handoff URL format to the old bridge format.

Configure the paths below before first use.
"""

import os
import sys
import subprocess
import shutil
from urllib.parse import urlparse, parse_qs

# ── Configuration ───────────────────────────────────────────
# Edit these paths to match your setup.

WINEPREFIX = "/home/YOUR_USER/Games/story-of-alicia"

BRIDGE_PATH = os.path.join(
    WINEPREFIX,
    "drive_c/users/YOUR_USER/AppData/Roaming/Story of Alicia",
    "alicia-launcher-bridge.exe",
)

# Path to wine binary. Examples:
#   /usr/bin/wine
#   /usr/share/steam/compatibilitytools.d/proton-cachyos/files/bin/wine
WINE_PATH = "/usr/bin/wine"

# Optional environment variables for GPU and DXVK.
# Comment out or remove any that don't apply to your setup.
EXTRA_ENV = {
    #"DRI_PRIME": "1",          # AMD/Intel: use discrete GPU
    "DXVK_HUD": "fps",        # Show FPS counter
    # NVIDIA users — uncomment these and comment out DRI_PRIME:
    # "__NV_PRIME_RENDER_OFFLOAD": "1",
    # "__GLX_VENDOR_LIBRARY_NAME": "nvidia",
    # "__VK_LAYER_NV_optimus": "NVIDIA_only",
}

# ── Script ──────────────────────────────────────────────────

def die(msg: str):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    # Check args
    if len(sys.argv) < 2:
        die("No URL provided. This script is meant to be called by the soa:// protocol handler.")

    incoming_url = sys.argv[1]

    # Validate URL
    parsed = urlparse(incoming_url)
    if parsed.scheme not in ("soa", "https", "http"):
        die(f"Unexpected URL scheme: {parsed.scheme}")

    # Parse parameters — handle both direct soa:// and handoff URLs
    query = parse_qs(parsed.query)
    user = query.get("user", [""])[0]
    token = query.get("token", [""])[0]

    if not user:
        die(f"Missing 'user' parameter in URL.\nReceived: {incoming_url}")
    if not token:
        die(f"Missing 'token' parameter in URL.\nReceived: {incoming_url}")

    # Check configuration
    if "YOUR_USER" in WINEPREFIX or "YOUR_USER" in WINE_PATH:
        die("You haven't configured this script yet. Edit the paths at the top of the file.")

    if not os.path.isdir(WINEPREFIX):
        die(f"Wine prefix not found: {WINEPREFIX}")

    bridge_full = os.path.join(WINEPREFIX, BRIDGE_PATH) if not os.path.isabs(BRIDGE_PATH) else BRIDGE_PATH
    if not os.path.isfile(bridge_full):
        die(f"Bridge executable not found: {bridge_full}")

    wine = shutil.which(WINE_PATH) or WINE_PATH
    if not os.path.isfile(wine):
        die(f"Wine not found: {WINE_PATH}")

    # Build translated URL
    translated_url = f"soa://4?username={user}&token={token}"

    # Build environment
    env = {
        **os.environ,
        "WINEPREFIX": WINEPREFIX,
        **EXTRA_ENV,
    }

    # Launch
    print(f"Launching bridge with translated URL...")
    try:
        subprocess.Popen([wine, bridge_full, translated_url], env=env)
    except PermissionError:
        die(f"Permission denied running: {wine}\nTry: chmod +x {wine}")
    except FileNotFoundError:
        die(f"Could not execute: {wine}")
    except Exception as e:
        die(f"Failed to launch bridge: {e}")


if __name__ == "__main__":
    main()