# Protocol Client

# This is still not fully working yet. 

`alicia_client.py` is a Python tool that connects to Alicia game servers and retrieves your player information without launching the game. It implements the Alicia command protocol from scratch.

## What It Shows

- Player name, UID, level, carrots, role
- Server notice (including online player count)
- Horse stats (agility, rush, endurance, etc.), grade, condition, mastery
- Equipment items
- Guild membership
- Pet info
- Training progression
- Management skills

## Usage

```bash
python3 alicia_client.py [--skip-tests]
```

You'll be asked to choose a server:

1. **Story of Alicia** — authenticate via Discord OAuth, paste the redirect URL
2. **Alicia Reborn** — authenticate with email + password (partially supported, auth flow not fully decoded yet)

### SOA Example

```
$ python3 alicia_client.py --skip-tests

  ╔═══════════════════════════════════════════════╗
  ║         Alicia Online — Protocol Client       ║
  ╚═══════════════════════════════════════════════╝

── Select Server ──────────────────────────────────

  1. Story of Alicia  (Discord login)
  2. Alicia Reborn    (Email + Password)

  Choice [1/2]: 1

  1. Open in browser:
     https://discord.com/oauth2/authorize?client_id=...

  2. Copy the redirect URL after authorizing.

  Paste URL: https://storyofalicia.com/launcher/handoff/?token=...&user=...&username=...

── Connecting to 5.75.155.237:10030 ──

  ✓ LOGIN SUCCESSFUL

  ── Profile ─────────────────────────────────────
    Name:          YourName
    UID:           1234
    Level:         31
    Carrots:       50,513
    ...
```

## How It Works

The protocol was reverse-engineered from the open-source [alicia-server](https://github.com/Story-Of-Alicia/alicia-server) codebase:

- **MessageMagic** — 4-byte header with bit-shuffled command ID and length
- **XOR encryption** — rolling 4-byte key (initial `0x00000000`, control `0xA20191CB`, multiplier `0x20080825`)
- **Null-terminated strings** encoded in EUC-KR (Korean game originally)
- **Login packet** — version constants (50, 281), loginId (Discord ID), memberNo, authKey (session token)
- **LoginOK response** — sent unencrypted, contains full player profile

The tool sends exactly one login packet, reads the response, and disconnects. It does not interact with gameplay, other players, or any game systems.

## Dependencies

Python 3.10+ (standard library only, no pip packages needed).

## Security & Fair Use

This tool is for **personal and educational use**. It:

- Only reads your own account data (requires your credentials)
- Cannot access other players' information
- Does not automate gameplay or provide any competitive advantage
- Does not bypass any server-side protections
- Sends the same login packet the game client sends
- Tokens are single-use and expire in 10 minutes

Do not use this tool for automation, scraping, or any activity that violates the game's terms of service.

## Alicia Reborn Status

The Reborn login flow is partially decoded:

- **Server:** `92.255.105.157:10030`
- **Protocol:** identical to SOA (same magic, XOR, packet format)
- **loginId:** email address
- **memberNo:** user ID from JWT token (`user_id` field)
- **authKey:** 64-char hex string — source unknown (not SHA-256 of password, not derived from JWT). Likely comes from a second API call the launcher makes. This needs further investigation.

## Credits

- Protocol: [Story-Of-Alicia/alicia-server](https://github.com/Story-Of-Alicia/alicia-server) (GPL-2.0)
- Auth flow: [Story-Of-Alicia/authentication-server](https://github.com/Story-Of-Alicia/authentication-server)