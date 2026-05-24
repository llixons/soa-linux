# Known Issues

> If your issue isn't listed here, [open an issue](../../issues) with your distro, GPU, Wine version, and what went wrong.

---

## Game Freezes

The game can freeze when entering race rooms. This bug exists on **both Windows and Linux** — it's a client bug, not a Wine issue. There is no workaround; it requires a game update to fix.

---

## Black Launcher Window

**Symptom:** The official launcher opens but shows a completely black window.

**Cause:** Missing Windows runtime libraries in the Wine prefix.

**Fix:** Install the required dependencies:

```bash
WINEPREFIX=/home/<your_user>/Games/story-of-alicia winetricks -q vcrun2010 vcrun2012 vcrun2013 vcrun2019 corefonts dotnet48
```

If winetricks hangs with "waiting for wine processes", kill the wineserver and retry:

```bash
WINEPREFIX=/home/<your_user>/Games/story-of-alicia wineserver -k
```

---

## DXVK Not Working / No FPS Counter

**Symptom:** `DXVK_HUD=fps` shows nothing in-game.

**Cause:** DXVK isn't installed in the prefix. Check:

```bash
file "/home/<your_user>/Games/story-of-alicia/drive_c/windows/system32/d3d11.dll"
```

If it says `PE32+ executable` — that's Wine's built-in DirectX, not DXVK.

**Fix:**

```bash
sudo pacman -S dxvk
WINEPREFIX=/home/<your_user>/Games/story-of-alicia setup_dxvk install
```

Then kill the wineserver so it picks up the new DLLs:

```bash
WINEPREFIX=/home/<your_user>/Games/story-of-alicia wineserver -k
```

---

## DXVK_HUD Set But Still Not Showing

**Symptom:** DXVK is installed, `DXVK_HUD=fps` is set, but no FPS counter appears.

**Cause:** The wineserver is a persistent daemon. If it started before `DXVK_HUD` was in the environment, child processes won't inherit it.

**Fix:** Kill the wineserver so it restarts with the correct environment:

```bash
WINEPREFIX=/home/<your_user>/Games/story-of-alicia wineserver -k
```

Then relaunch the game with `DXVK_HUD=fps` set.

---

## WebView2 / COM Errors (Official Launcher)

**Symptom:** Launcher crashes with COM or WebView2 errors.

**Cause:** Proton doesn't support the COM objects the Electron launcher needs.

**Fix:** Use regular Wine, not Proton, for the official launcher. The game itself can run under either.

---

## soa:// Protocol Handler Not Working

**Symptom:** Clicking Play in the launcher opens the browser but the game doesn't start after authorizing with Discord.

**Possible causes:**

1. **Handler not registered.** Check:
   ```bash
   grep -i soa ~/.config/mimeapps.list
   ```
   If empty, register it:
   ```bash
   xdg-mime default soa-handler.desktop x-scheme-handler/soa
   update-desktop-database ~/.local/share/applications/
   ```

2. **Wrong path in desktop file.** Paths must be full absolute paths, not `~`. Check your `soa-handler.desktop`:
   ```bash
   cat ~/.local/share/applications/soa-handler.desktop
   ```

3. **Wrong exe path.** Make sure the `Exec` line points to the correct launcher or bridge executable and the file actually exists at that path.

---

## Wine Prefix Not Initialized

**Symptom:** Winetricks fails, weird errors about missing directories, or Wine acts up.

**Cause:** The prefix was created with `mkdir` but never initialized by Wine.

**Fix:** Initialize it before installing anything:

```bash
WINEPREFIX=/home/<your_user>/Games/story-of-alicia wineboot -u
```

---

## Winetricks Hangs

**Symptom:** Winetricks shows "This will hang until all wine processes terminate" and freezes.

**Cause:** A stale wineserver or wine process is running in that prefix.

**Fix:**

```bash
WINEPREFIX=/home/<your_user>/Games/story-of-alicia wineserver -k
```

Then retry the winetricks command.

---