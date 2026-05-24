# Alicia Reborn Setup

> **Note:** Alicia Reborn has not been extensively tested on Linux. This guide documents what worked on one system (CachyOS, AMD GPU, proton-cachyos). Your mileage may vary.

[Alicia Reborn](https://alicia-reborn.online/) is a fan-run server. It uses the same game client as Story of Alicia but has its own launcher (PyInstaller-bundled Python app) and account system (email/password instead of Discord).

- **Website:** [alicia-reborn.online](https://alicia-reborn.online/)
- **Discord:** [discord.gg/aliciareborn](https://discord.gg/aliciareborn)
- **Server:** `92.255.105.157:10030`

## Prerequisites

- **Wine** or **Proton** (proton-cachyos confirmed working)
- **DXVK**

>Replace YOUR_USER always with your own username on Linux. Eg. `/home/YOUR_USER/` becomes `/home/lio` if your username is lio
>
> Adjust `WINE_PATH` if using Proton (e.g. `/usr/share/steam/compatibilitytools.d/proton-cachyos/files/bin/wine` instead of `wine`).


## Setup

### 1. Create a Wine prefix

```bash
export WINEPREFIX=/home/YOUR_USER/Games/alicia-reborn
mkdir -p "$WINEPREFIX"
WINEPREFIX=/home/YOUR_USER/Games/story-of-alicia wineboot -u
```

> Note: Follow the installer's default installer path and settings.
> 
### 2. Install the game

The launcher installs by default into `/home/YOUR_USER/Games/alicia-reborn/drive_c/Games/AliciaReborn/`

Download the Alicia Reborn launcher/installer from their website. Install it with Wine:

```bash
WINEPREFIX=/home/YOUR_USER/Games/alicia-reborn wine AliciaRebornSetup.exe
```
> Note: You don't need to install DXVK unless you want to show fps or system performance during gameplay.


### 3. Install DXVK

```bash
sudo pacman -S dxvk  # Arch/CachyOS
WINEPREFIX=~/Games/alicia-reborn setup_dxvk install
```

### 4. Launch

```bash
WINEPREFIX=~/Games/alicia-reborn DXVK_HUD=fps wine "/path/to/AliciaLauncher.exe"
```

The launcher handles login (email/password) and game updates. After logging in, click Play and the game should start.

## Differences from SOA

- **Login:** email + password instead of Discord OAuth
- **Same client engine:** same game binary, same protocol, same bugs (including gamefreeze)

## What's Not Tested

- Game updates through their launcher on Linux
- Stability over long play sessions
- All maps and game modes
- The launcher's Cloudflare Turnstile captcha behavior under Wine

If you run into issues not covered here, check the [Alicia Reborn Discord](https://discord.gg/aliciareborn) — the devs may have Linux-specific advice.