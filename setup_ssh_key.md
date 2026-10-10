# SSH Key Setup

## Why?

Without SSH key you need to enter password **4 times per install**.
With key — **zero times**.

## Steps

### 1. Generate key on PC

**Windows (PowerShell):**
```powershell
ssh-keygen -t ed25519 -f "$env:USERPROFILE\.ssh\iphone_key"
```
Press **Enter twice** (empty passphrase).

**macOS / Linux:**
```bash
ssh-keygen -t ed25519 -f ~/.ssh/iphone_key
```

### 2. Find your port

Open **3uTools** → **Toolbox** → **SSH Tunnel**.
Look at the port (e.g. `61505`).

### 3. Copy public key to iPhone

**Windows:**
```powershell
type "$env:USERPROFILE\.ssh\iphone_key.pub" | ssh -p 61505 root@127.0.0.1 "mkdir -p /var/root/.ssh && cat >> /var/root/.ssh/authorized_keys && chmod 600 /var/root/.ssh/authorized_keys && chmod 700 /var/root/.ssh && echo KEY_OK"
```

**macOS / Linux:**
```bash
cat ~/.ssh/iphone_key.pub | ssh -p 61505 root@127.0.0.1 "mkdir -p /var/root/.ssh && cat >> /var/root/.ssh/authorized_keys && chmod 600 /var/root/.ssh/authorized_keys && chmod 700 /var/root/.ssh && echo KEY_OK"
```

Default root password: **`alpine`**.

You should see: `KEY_OK`

### 4. Verify

```powershell
ssh -i "$env:USERPROFILE\.ssh\iphone_key" -p 61505 root@127.0.0.1 "echo KEY_WORKS"
```

Should print `KEY_WORKS` **without password prompt**.

### 5. Done

Now `install_deb.py` works without passwords.

## Troubleshooting

| Error | Solution |
|---|---|
| `UNIX authentication refused` | Password not set — reset via NewTerm: `su root` → `passwd` |
| `Permission denied` | Wrong password — try `alpine`, `root`, or reset |
| `KEY_OK` not shown | Check `/var/root/.ssh/` permissions on iPhone |
