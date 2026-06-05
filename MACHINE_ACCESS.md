# Machine Access — M1 / M2 / M1B (UNIVERSAL, cross-project)

**Scope:** Canonical reference for SSH access to the user's compute nodes **M1**, **M2**
(and **M1B**). Access is **NOT specific to the Farey project** — any project or session may
read this file to connect to M1/M2 for compute. It physically lives in the `Farey NOW` repo
but is a shared infra reference. (Supersedes the blank template `m1-m2-handoff.md`.)

_Last updated: 2026-06-05. M1 & M2 RE-VERIFIED CONTROL_OK from M3 (passwordless). See STATUS._

> **2026-06-05 re-verification + two durable gotchas:**
> 1. **Wi-Fi client isolation can silently block M3↔node even on the same `192.168.1.x`.**
>    Symptom: node self-reports its IP + Remote Login ON, but from M3 `ping` = 100% loss and
>    `arp -n <ip>` = **(incomplete)** while *another* node on the same /24 pings fine. Cause = node
>    joined a different SSID / guest net / mesh-leg with station isolation. NOT a key/sleep problem —
>    no paste on the node fixes it. Fix is router-side: put the node on the **same un-isolated SSID**
>    as M3 (or wire it). Same root cause also kills mDNS (`*.local`) across the boundary.
> 2. **mDNS `*.local` did NOT resolve from M3** even when the node was reachable by IP (resolver
>    quirk). Once on the same network, **connect by IP** (`new@192.168.1.22`, `alicia@192.168.1.92`);
>    treat `.local` as best-effort, not the primary handle.
> 3. **Never-sleep is now enforced by a root LaunchDaemon** `com.farey.keepawake`
>    (`/Library/LaunchDaemons/com.farey.keepawake.plist`, runs `caffeinate -dimsu`, RunAtLoad+KeepAlive)
>    **+ `sudo pmset -a sleep 0 … disablesleep 1`**. Loads at boot, no login needed. If a node sleeps
>    again, re-check the daemon is `loaded` and `pmset -g | grep disablesleep` = 1.

## Topology (current)
- **M3** = primary workstation / Claude-Code host = `Saaars-MacBook-Pro.local`, currently `192.168.1.134`.
- **M1 / M2 / M1B** = remote Mac compute nodes, reached by SSH **from M3** over the LAN.
- Wi-Fi network: **"happyface starlink"**, subnet `192.168.1.0/24` (Starlink default).
- ⚠️ All nodes are **Wi-Fi laptops on DHCP** → their IPs **DRIFT** across reboots / network
  changes, and they sleep. **Re-discover** (see below) instead of trusting a hardcoded IP.

## Access method
- Auth = **SSH key** from M3's `~/.ssh/id_ed25519`. Public key (install this on each node):
  ```
  ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDcQldHpzWsEuiIuUUb+wNZOV75YNVdxwLbulPP9vWAF za@token-economy-20260508
  ```
  (The harness can't read the private key, but `ssh` can use it.)
- Connect: `ssh -i ~/.ssh/id_ed25519 -o StrictHostKeyChecking=accept-new <user>@<ip>`
- Usernames (historical — CONFIRM via report block; accounts may differ now):
  M1 = `new`, M2 = `saar`, M1B = `za`.

## Verified values — STATUS: M1 ✅ · M2 ✅ RE-VERIFIED CONTROL_OK 2026-06-05 (key passwordless, both up at .22/.92) · M1B offline
| node | IP | user | ssh | cores / RAM | macOS | toolchain | verified |
|---|---|---|---|---|---|---|---|
| M1  | `192.168.1.22` | `new` | `ssh -i ~/.ssh/id_ed25519 new@192.168.1.22` | M1 Max 10c / 32GB | 26.3.1 | cc, make, python3.9, mpmath1.3, numpy2.0 (no gp) | ✅ 2026-06-02 |
| M2 ("Alicia Pro") | `192.168.1.92` | `alicia` | `ssh -i ~/.ssh/id_ed25519 alicia@192.168.1.92` | M2 **Pro** 12c / 16GB | 26.4.1 | cc, make; ssh→py3.9+mpmath1.4; gui→py3.14+numpy2.4 (no gp) | ✅ 2026-06-02 |
| M1B | — | `za` | — | M1 Max 10c / 32GB | — | — | offline |

- **M1 ✅ verified 2026-06-02**: control test from M3 passed (`CONTROL_OK`, passwordless key auth).
  ComputerName "MacBook Pro" / `MacBook-Pro-2.local`; Wi-Fi MAC `c6:0f:26:67:d1:f0` (⚠ locally-
  administered / macOS *private* Wi-Fi address — rotates per-SSID; don't rely on it for long-term ID);
  74Gi free of 460Gi; Remote Login ON; **Farey repo absent** (scp sieve source before running). No PARI `gp`.
- **M2 ✅ verified 2026-06-02** = "Alicia Pro" (`Alicia-Pro.local`), user `alicia`, M2 **Pro** 12c / 16GB,
  macOS 26.4.1. Control test passed; `mpmath 1.4.1` installed. ⚠ PYTHON GOTCHA: over SSH (non-login)
  `python3` = CommandLineTools 3.9 (has mpmath 1.4.1); in the GUI Terminal `python3` = python.org 3.14.2
  (+ numpy 2.4.2). Use full paths if a specific interpreter is needed. Wi-Fi MAC `aa:92:1a:15:21:2d`
  (private/rotating). 81Gi free; Remote Login ON; Farey repo absent; no PARI gp. 16GB RAM (fine for the
  segmented sieve — memory is bounded by segment size, not by x). Confirmed by user as their M2.
- Old pre-Starlink IPs `192.168.1.218` (M1) / `192.168.1.187` (M2) / `192.168.1.64` (M1B) are **dead**.

## One-time setup — paste in Terminal ON each node (M1, then M2)
Installs M3's key (enables passwordless SSH from M3) and prints identity. No sudo; idempotent.
```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
K='ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDcQldHpzWsEuiIuUUb+wNZOV75YNVdxwLbulPP9vWAF za@token-economy-20260508'
grep -qF "$K" ~/.ssh/authorized_keys 2>/dev/null || printf '%s\n' "$K" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
nohup caffeinate -i -t 7200 >/dev/null 2>&1 &   # stay awake 2h for M3 to connect
IF=$(route -n get default 2>/dev/null | awk '/interface:/{print $2; exit}'); IF=${IF:-en0}
echo "===== M-NODE REPORT ====="
echo "ComputerName : $(scutil --get ComputerName 2>/dev/null)"
echo "LocalHost    : $(scutil --get LocalHostName 2>/dev/null).local"
echo "user         : $(whoami)"
echo "iface/IP/MAC : ${IF} / $(ipconfig getifaddr "$IF" 2>/dev/null) / $(ifconfig "$IF" 2>/dev/null | awk '/ether/{print $2}')"
echo "model/chip   : $(sysctl -n hw.model) / $(sysctl -n machdep.cpu.brand_string 2>/dev/null)"
echo "arch/cores   : $(uname -m) / $(sysctl -n hw.ncpu) cores / $(($(sysctl -n hw.memsize)/1073741824))GB RAM"
echo "macOS        : $(sw_vers -productVersion)"
echo "free disk    : $(df -h / | awk 'NR==2{print $4" of "$2}')"
echo "remote login : $(nc -z -G1 127.0.0.1 22 >/dev/null 2>&1 && echo ON || echo 'OFF -> System Settings > General > Sharing > Remote Login')"
echo "compiler     : cc=$(command -v cc||echo none) make=$(command -v make||echo none)"
echo "python3      : $(command -v python3||echo none) ($(python3 --version 2>&1))"
echo "mpmath/numpy : $(python3 -c 'import mpmath;print(mpmath.__version__)' 2>/dev/null||echo MISSING) / $(python3 -c 'import numpy;print(numpy.__version__)' 2>/dev/null||echo MISSING)"
echo "gp (PARI)    : $(command -v gp||echo none)"
echo "Farey repo   : $([ -d ~/'Documents/Farey NOW' ] && echo present || echo absent)"
echo "key install  : $(grep -qF "$K" ~/.ssh/authorized_keys && echo OK || echo FAILED)"
echo "===== END REPORT ====="
```

## Re-discovery (when IPs drift) — run on M3
```bash
SUB=$(ipconfig getifaddr en0 | sed 's/\.[0-9]*$//')          # M3's /24
for i in $(seq 1 254); do ping -c1 -t1 "$SUB.$i" >/dev/null 2>&1 & done; wait
for ip in $(arp -a | sed -n "s/.*(\($SUB\.[0-9]*\)).*/\1/p" | sort -u); do
  nc -z -G1 -w1 "$ip" 22 >/dev/null 2>&1 && echo "$ip ssh:22 open"; done
# identify a host: ssh -i ~/.ssh/id_ed25519 <user>@<ip> 'scutil --get ComputerName; sysctl -n hw.ncpu'
```
mDNS names (resolve regardless of IP, if the node is awake): `MacBookPro.local`, `zas-MacBook-Pro.local`.

## Operating notes
- **No remote wake**: WoL doesn't work over Wi-Fi; a sleeping node must be woken **physically**.
- **Long jobs**: Wi-Fi laptops idle-sleep → run under `caffeinate -s <cmd>` to keep awake mid-run.
- **Stability**: set a DHCP reservation on the Starlink router (or use the `.local` mDNS name)
  so the SSH target doesn't move.
- M1/M2 have **Ollama / EXO** roles historically; don't disrupt those when borrowing for compute.
