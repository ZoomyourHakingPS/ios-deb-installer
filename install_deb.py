#!/usr/bin/env python3
"""
iOS DEB Installer
Install .deb packages on jailbroken iPhone via SSH tunnel.

Author: @kega_007 (GitHub: App4l)
License: MIT
Tested on: iPhone 6 Plus, iOS 12.5.8, unc0ver, 3uTools SSH tunnel
"""

import os
import sys
import subprocess

# ============ НАСТРОЙКИ ============
DEFAULT_PORT = "61505"
HOST = "root@127.0.0.1"
REMOTE_TMP = "/tmp"
SSH_KEY = os.path.expanduser(r"~\.ssh\iphone_key")

DISCLAIMER = """
================================================================================
  iOS DEB Installer — by @kega_007 (App4l)
================================================================================

  ALLOWED:
    - Install .deb on YOUR OWN jailbroken iPhone
    - Test tweaks YOU are developing
    - Learn iOS internals on YOUR device

  FORBIDDEN:
    - Installing on someone else's device without permission
    - Piracy (cracked .ipa, paid .deb without license)
    - DRM / signing bypass
    - Unauthorized access, spying, hacking
    - Any illegal activity

  Author does NOT support piracy, theft, or unauthorized access.
  Jailbreaking voids Apple warranty. Use at your own risk.
  You are responsible for complying with your local laws.

  By continuing, you agree to these terms.

================================================================================
"""


def run(cmd, silent=False):
    """Запускает команду, показывает вывод."""
    if not silent:
        print(f"\n>>> {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False, text=True, timeout=600)
    return result.returncode == 0


def main():
    print(DISCLAIMER)
    if input("Continue? (y/n) [y]: ").strip().lower() not in ("", "y"):
        return

    print("=" * 60)
    print(" iOS DEB Installer")
    print("=" * 60)

    # 1. Файл .deb
    deb_path = input("\nPath to .deb file: ").strip().strip('"').strip("'")
    if not os.path.isfile(deb_path):
        print(f"[ERROR] File not found: {deb_path}")
        input("Press ENTER to exit...")
        return

    if not deb_path.lower().endswith(".deb"):
        print("[WARN] File does not end with .deb")
        if input("Continue? (y/n) [n]: ").strip().lower() != "y":
            return

    # 2. Порт
    port = input(f"SSH tunnel port [{DEFAULT_PORT}]: ").strip() or DEFAULT_PORT

    deb_name = os.path.basename(deb_path)
    remote_deb = f"{REMOTE_TMP}/{deb_name}"

    # Общие SSH-опции
    ssh_opts = [
        "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-o", "IdentitiesOnly=yes",
        "-o", "ConnectTimeout=10",
    ]

    # 3. Заливка
    print(f"\n[1/4] Uploading {deb_name}...")
    scp_cmd = ["scp", "-P", port] + ssh_opts + [deb_path, f"{HOST}:{remote_deb}"]
    if not run(scp_cmd):
        print("[ERROR] Upload failed. Check tunnel and SSH key.")
        input("Press ENTER to exit...")
        return

    # 4. Установка
    print(f"\n[2/4] Installing {deb_name}...")
    ssh_install = ["ssh", "-p", port] + ssh_opts + [HOST, f"dpkg -i {remote_deb}"]
    if not run(ssh_install):
        print("[!] dpkg error. Trying to fix dependencies...")
        ssh_fix = ["ssh", "-p", port] + ssh_opts + [
            HOST,
            "apt-get -f install -y --allow-unauthenticated"
        ]
        run(ssh_fix)

    # 5. Чистка
    print(f"\n[3/4] Cleaning up...")
    ssh_clean = ["ssh", "-p", port] + ssh_opts + [HOST, f"rm -f {remote_deb}"]
    run(ssh_clean, silent=True)

    # 6. Respring
    print(f"\n[4/4] Respring...")
    ssh_respring = ["ssh", "-p", port] + ssh_opts + [HOST, "killall -9 SpringBoard"]
    run(ssh_respring, silent=True)

    print("\n" + "=" * 60)
    print(" DONE. Tweak installed. By @kega_007")
    print("=" * 60)
    input("\nPress ENTER to exit")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        input("Press ENTER to exit")
