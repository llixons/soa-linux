# Old Launcher Setup (Bridge Method)

If you have the legacy launcher with `alicia-launcher-bridge.exe`, you need a script to translate the new `soa://` URL format to the old one.

## Prerequisites

- **Wine** or **Proton** (proton works here, unlike the official launcher)
- **DXVK**
- **Python 3**


## Setup

>Replace YOUR_USER always with your own username on Linux. Eg. `/home/YOUR_USER/` becomes `/home/lio` if your username is lio
>
> Adjust `WINE_PATH` if using Proton (e.g. `/usr/share/steam/compatibilitytools.d/proton-cachyos/files/bin/wine` instead of `wine`).


### 1. Create a Wine prefix

```bash
export WINEPREFIX=/home/YOUR_USER/Games/story-of-alicia
mkdir -p "$WINEPREFIX"
WINEPREFIX=/home/YOUR_USER/Games/story-of-alicia wineboot -u
```

A fresh Wine prefix is missing runtime libraries the launcher needs. Install them:
This can take a few minutes.

```bash
WINEPREFIX=/home/YOUR_USER/Games/story-of-alicia winetricks -q vcrun2010 vcrun2012 vcrun2013 vcrun2019 
```

> Note: Follow the installer's default installer path and settings.

### 2. Install the Bridge

The bridge installs by default into `/home/YOUR_USER/Games/story-of-alicia-old/drive_c/users/YOUR_USER/AppData/Roaming/Story of Alicia/`

Download the bridge from [Proton Drive](https://drive.proton.me/urls/37WM215Q1R#NlzxAZSg7VFC
) and install it with Wine:

```bash
WINEPREFIX=/home/YOUR_USER/Games/story-of-alicia wine /path/to/Story\ of\ Alicia\ setup.exe
```


### 1. Create the translation script

The old bridge expects `soa://4?username=DISCORD_ID&token=TOKEN`, but the website now redirects to `https://storyofalicia.com/launcher/handoff/?token=XXX&user=YYY&username=ZZZ`. This script translates between them.

Create the file `~/.local/bin/translate_url.py`:
```bash
mkdir -p ~/.local/bin
touch ~/.local/bin/translate_url.py
```

Copy the contents of `translate_url.py` in this repo and past it into a newly created file here: `~/.local/bin/translate_url.py`:

```bash
chmod +x ~/.local/bin/translate_url.py
```
> Remember to edit `translate_url.py` so it matches your own paths. DO NOT RUN IT AS-IS!

### 2. Register the protocol handler

Create `~/.local/share/applications/soa-handler.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=SOA Protocol Handler
Exec=/home/YOUR_USER/.local/bin/translate_url.py %u
MimeType=x-scheme-handler/soa;
NoDisplay=true
```

```bash
xdg-mime default soa-handler.desktop x-scheme-handler/soa
update-desktop-database ~/.local/share/applications/
```

> Note: You don't need to install DXVK unless you want to show fps or system performance during gameplay.

### Install DXVK

```bash
sudo pacman -S wine proton dxvk
WINEPREFIX=/home/YOUR_USER/Games/story-of-alicia-old setup_dxvk install
```

### 3. Launch

Open the Discord OAuth link in your browser:

```
https://discord.com/oauth2/authorize?client_id=1272602862043795586&response_type=code&redirect_uri=https%3A%2F%2Fauthentication.storyofalicia.com%2F&scope=identify
```

Authorize → redirect fires → bridge translates → game launches.