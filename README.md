# iOS DEB Installer

> Install `.deb` packages on jailbroken iPhone via SSH tunnel — without Cydia/Sileo, with automatic dependency resolution and Respring.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![iOS](https://img.shields.io/badge/iOS-12.5.8-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## Why?

- **BigBoss is dead in RU** — can't download tweaks via Sileo.
- **Cydia/Sileo** fails on iOS 12.5.8.
- **You have a `.deb`** — want to install it fast.
- **You're a tweak developer** — need quick deploy to device.

This tool does **one thing**: installs `.deb` on your iPhone via SSH.

## Features

- ✅ Install `.deb` via SSH tunnel (3uTools port).
- ✅ Auto-install dependencies (`apt-get -f install`).
- ✅ Auto Respring after install.
- ✅ SSH key authentication (no password prompts).
- ✅ Works on **Windows / macOS / Linux**.
- ✅ **Zero dependencies** — pure Python 3.8+.

## Requirements

- **Jailbroken iPhone** (tested on iOS 12.5.8, unc0ver).
- **3uTools** with **SSH Tunnel** open (green).
- **Python 3.8+**.
- **OpenSSH Client** (`ssh`, `scp` in PATH).
- **SSH key** configured (see [setup_ssh_key.md](setup_ssh_key.md)).

## Quick Start

### 1. Setup SSH key (once)

```bash
ssh-keygen -t ed25519 -f ~/.ssh/iphone_key
# Press Enter twice for empty passphrase
```

**Copy public key to iPhone:**

```powershell
# Windows
type "$env:USERPROFILE\.ssh\iphone_key.pub" | ssh -p 61505 root@127.0.0.1 "mkdir -p /var/root/.ssh && cat >> /var/root/.ssh/authorized_keys && chmod 600 /var/root/.ssh/authorized_keys && chmod 700 /var/root/.ssh"
```

```bash
# macOS / Linux
cat ~/.ssh/iphone_key.pub | ssh -p 61505 root@127.0.0.1 "mkdir -p /var/root/.ssh && cat >> /var/root/.ssh/authorized_keys && chmod 600 /var/root/.ssh/authorized_keys && chmod 700 /var/root/.ssh"
```

Default root password on jailbroken iOS: **`alpine`**.

### 2. Run installer

```bash
python install_deb.py
```

```
Path to .deb file: C:\Downloads\tweak.deb
SSH tunnel port [61505]: 61505

[1/4] Uploading tweak.deb...
[2/4] Installing tweak.deb...
[3/4] Cleaning up...
[4/4] Respring...
================================================================================
 DONE. Tweak installed. By @kega_007
================================================================================
```

### 3. Done

Tweak is installed. Check **Sileo → Installed**.

## How it works

```
[PC]                                    [iPhone]
  │                                        │
  │ 1. scp .deb → /tmp/                    │
  ├────────────────────────────────────────┤
  │                                        │
  │ 2. ssh: dpkg -i /tmp/tweak.deb         │
  ├────────────────────────────────────────┤
  │                                        │
  │ 3. ssh: apt-get -f install (if needed) │
  ├────────────────────────────────────────┤
  │                                        │
  │ 4. ssh: killall -9 SpringBoard         │
  ├────────────────────────────────────────┤
  │                                        │
  └──────────── Done ──────────────────────┘
```

## Configuration

Edit at the top of `install_deb.py`:

```python
DEFAULT_PORT = "61505"                                # 3uTools SSH tunnel port
HOST = "root@127.0.0.1"                               # SSH host
SSH_KEY = os.path.expanduser(r"~\.ssh\iphone_key")    # path to key
```

## Troubleshooting

| Error | Solution |
|---|---|
| `Connection refused` | Open 3uTools → SSH Tunnel (green) |
| `Permission denied` | Setup SSH key — see [setup_ssh_key.md](setup_ssh_key.md) |
| `dpkg: not found` | No jailbreak — install unc0ver/checkra1n |
| `dependency problems` | Script handles automatically |
| `is not a Debian format archive` | You're trying to install `.ipa` — use AppSync |

## Tested On

- iPhone 6 Plus (`iPhone7,1`)
- iOS 12.5.8
- unc0ver jailbreak
- 3uTools SSH tunnel (port 61505)
- Windows 10/11

## Roadmap

- [x] CLI installer
- [x] SSH key auth
- [x] Auto-dependency
- [ ] GUI (tkinter)
- [ ] Batch install (folder with `.deb`)
- [ ] Download `.deb` by URL
- [ ] `.exe` build
- [ ] macOS / Linux binaries

## Contributing

PRs welcome. Especially:
- Tested on other iOS versions
- GUI improvements
- New features

## License

MIT — see [LICENSE](LICENSE).

## Author

**@kega_007** (GitHub: [App4l](https://github.com/App4l))
- Steam: [AmethystUncoverLeminlemizNugget](https://steamcommunity.com/id/AmethystUncoverLeminlemizNugget/)

## ⚠️ Disclaimer

**Use only on YOUR OWN device. No piracy. No unauthorized access.**

- ✅ Install on your own jailbroken iPhone.
- ✅ Test tweaks you develop.
- ❌ No someone else's device without permission.
- ❌ No piracy / DRM bypass / unauthorized access.

Author is **not liable** for bricked devices, data loss, or legal issues.
Jailbreaking voids Apple warranty. **Use at your own risk.**

If you don't agree — **don't use this software.**
