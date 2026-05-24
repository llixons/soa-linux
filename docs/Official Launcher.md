# Official Launcher Setup

The official SOA launcher is an Electron app with WebView2. It handles Discord login and game updates.

## Prerequisites

- **Wine** - must be regular Wine, **not** Proton (WebView2 COM objects don't work under Proton)
- **DXVK** - for Vulkan-based rendering
- **winetricks** - for installing Windows runtime dependencies

### Install packages

Arch/CachyOS:

```bash
sudo pacman -S python wine dxvk winetricks
```

## Setup

### 1. Create a Wine prefix and install dependencies

>Replace YOUR_USER always with your own username on Linux. Eg. `/home/YOUR_USER/` becomes `/home/lio` if your username is lio

```bash
export WINEPREFIX=/home/YOUR_USER/Games/story-of-alicia
mkdir -p "$WINEPREFIX"
WINEPREFIX=/home/YOUR_USER/Games/story-of-alicia wineboot -u
```

A fresh Wine prefix is missing runtime libraries the launcher needs. Install them:
This can take a few minutes.

```bash
WINEPREFIX=/home/YOUR_USER/Games/story-of-alicia winetricks -q vcrun2010 vcrun2012 vcrun2013 vcrun2019 corefonts dotnet48
```

Without these, the launcher window will be black. If winetricks hangs with a "waiting for wine processes" warning, kill the wineserver first:

```bash
WINEPREFIX=/home/YOUR_USER/Games/story-of-alicia wineserver -k
```

Then retry.

> Note: Follow the installer's default installer path and settings.

### 2. Install the Launcher

The launcher installs by default into `/home/YOUR_USER/Games/story-of-alicia/drive_c/users/YOUR_USER/AppData/Local/Story of Alicia Launcher/`

Download the launcher from [storyofalicia's website](https://storyofalicia.com) and install it with Wine:

```bash
WINEPREFIX=/home/YOUR_USER/Games/story-of-alicia wine /path/to/Story\ of\ Alicia\ setup.exe
```

The launcher will install the WebView2 runtime automatically during setup.

> Note: You don't need to install DXVK unless you want to show fps or system performance during gameplay.

### 3. Install DXVK into the prefix

```bash
WINEPREFIX=/home/YOUR_USER/Games/story-of-alicia setup_dxvk install
```

### 4. Register the soa:// protocol handler

The launcher redirects through Discord OAuth and produces a `soa://` URL that needs to reach the launcher. Create a desktop entry to handle it.

Create `~/.local/share/applications/soa-handler.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=SOA Protocol Handler
Exec=env WINEPREFIX=/home/YOUR_USER/Games/story-of-alicia wine "/home/YOUR_USER/Games/story-of-alicia/drive_c/users/<your_username>/AppData/Local/Story of Alicia Launcher/story-of-alicia-launcher.exe" %u
MimeType=x-scheme-handler/soa;
NoDisplay=true
```

Register it:

```bash
xdg-mime default soa-handler.desktop x-scheme-handler/soa
update-desktop-database ~/.local/share/applications/
```

### 5. Launch

Open the launcher with Wine, click Play, authorize with Discord. The browser redirects to `soa://`, the protocol handler catches it and passes the URL to the launcher, which starts the game.

#### Environment Variables


| Variable | Value | Description                            |
|----------|-------|----------------------------------------|
| `DRI_PRIME` | `1` | Use discrete/external GPU (AMD/Intel)  |
| `__NV_PRIME_RENDER_OFFLOAD` | `1` | Use discrete GPU (NVIDIA)              |
| `__GLX_VENDOR_LIBRARY_NAME` | `nvidia` | Required alongside the above for NVIDIA |
| `__VK_LAYER_NV_optimus` | `NVIDIA_only` | Force Vulkan through NVIDIA GPU        |
| `DXVK_HUD` | `fps` | Show FPS counter in-game               |
| `WINEPREFIX` | Full path to prefix | Path to wine prefix |                   |

> Note: I recommend running the launcher first without any environment variables set.

#### Example with environment variables
```bash
WinePREFIX=/home/YOUR_USER/Games/story-of-alicia DXVK_HUD=1 wine "/home/YOUR_USER/Games/story-of-alicia/drive_c/users/YOUR_USER/AppData/Local/Story of Alicia Launcher/story-of-alicia-launcher.exe"
```
#### Example without environment variables
```bash
# This commands open the launcher with no enviroment variables set.
WINEPREFIX=/home/YOUR_USER/Games/story-of-alicia wine "/home/YOUR_USER/Games/story-of-alicia/drive_c/users/YOUR_USER/AppData/Local/Story of Alicia Launcher/story-of-alicia-launcher.exe"
```

> Once you verified the game is running and isn't crashing, create a desktop shortcut to the launcher:
```ini
[Desktop Entry]
Name=Story Of Alicia
Type=Application
Exec=WINEPREFIX="/home/YOUR_USER/Games/story-of-alicia" wine "/home/YOUR_USER/Games/story-of-alicia/drive_c/users/YOUR_USER/AppData/Local/Story of Alicia Launcher/story-of-alicia-launcher.exe"
Icon=wine
Terminal=false
Categories=Game;
StartupNotify=true
```

You can name or place this file wherever you want.

I recommend putting it in `~/.local/share/applications/`.
then run `update-desktop-database ~/.local/share/applications/` to update the database to show the shortcut in the menubar.

## Auth Flow

For the curious, here's what happens when you click Play:

1. Browser opens Discord OAuth (`discord.com/oauth2/authorize`)
2. You authorize, Discord redirects to `authentication.storyofalicia.com/?code=XXX`
3. Auth server exchanges the code with Discord, creates a session token
4. Auth server redirects to `soa://` URL containing `token`, `user` (Discord ID), and `username`
5. Protocol handler catches the URL and passes it to the launcher
6. Launcher starts the game, which connects to the game server with your Discord ID + token