# SOA-Linux

Running [Story of Alicia](https://storyofalicia.com/) and [Alicia Reborn](https://alicia-reborn.online/) on Linux.
> **NOTE**
> These guides document how I got the games working on my system through trial and error. Linux setups vary wildly - different distros, drivers, Wine versions, and GPUs can all change the outcome. If something doesn't work, you may need to troubleshoot differently than what's described here.

> **IMPORTANT**
> ***Read the instructions carefully and follow each step in order.*** Skipping steps (especially winetricks dependencies) will result in a black screen or crashes. These guides use full paths everywhere.
>
> This repo and it's guides is still under development. There will be spelling mistakes and things missing.
> 
> **Having trouble?** Check [Known Issues](docs/known-issues.md) first, then [open an issue](../../issues) with your distro, GPU, Wine version, and what went wrong.


## Guides

### Story of Alicia
- **[Official Launcher Setup](docs/official-launcher.md)** - Recommended. Uses the Electron-based launcher with Discord login.
- **[Old Launcher Setup](docs/old-launcher.md)** - For the legacy launcher with `alicia-launcher-bridge.exe` and a URL translation script.

### Alicia Reborn
- **[Alicia Reborn Setup](docs/alicia-reborn.md)** - Fan-run server with its own launcher and email/password login. Not tested well enough to recommend.

### Reference
- **[Known Issues](docs/known-issues.md)** - Issues I encountered, DXVK problems, and workarounds.
- **[Protocol Client](docs/protocol-client.md)** - A Python tool that connects to the game server and retrieves your player info without launching the game.

## Quick Start

1. Install Wine and DXVK (see your distro's packages)
2. Pick a launcher guide based on your GPU:
    - **NVIDIA GPU** - use the [Old Launcher](docs/old-launcher.md) with Proton. The official launcher's WebView2 doesn't work under Proton, but NVIDIA's Wine/DXVK support is better through Proton.
    - **AMD GPU (modern, RDNA+)** — the [Official Launcher](docs/official-launcher.md) with regular Wine should work. If you hit issues, fall back to the [Old Launcher](docs/old-launcher.md) with Proton.
    - **AMD iGPU / Intel** - same as above, try official first, old launcher as fallback.
3. Log in via Discord, race horses

## Tested On

- CachyOS (Arch-based), KDE Plasma/Wayland
- AMD Radeon 890M iGPU + AMD RX 7700 XT eGPU
- Wine 10.x / proton-cachyos

Contributions and issue reports welcome.