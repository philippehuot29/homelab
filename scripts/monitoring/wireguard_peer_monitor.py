#!/usr/bin/env python3
"""
wireguard_peer_monitor.py
Monitor WireGuard peer handshake times and alert via Telegram if a tunnel drops.

Stage 3 — WireGuard VPN Server
Host: M710q homelab (192.168.8.64)

Usage:
    python3 wireguard_peer_monitor.py

Cron (every 5 minutes):
    */5 * * * * /usr/bin/python3 /home/cyberphil/homelab/scripts/monitoring/wireguard_peer_monitor.py
"""

import subprocess
import time
import requests
from datetime import datetime

# --- Configuration ---
TELEGRAM_BOT_TOKEN = "REDACTED"
TELEGRAM_CHAT_ID = "REDACTED"

# Max seconds since last handshake before alerting
# WireGuard handshakes every ~180s — alert if > 300s (5 min)
HANDSHAKE_THRESHOLD_SECONDS = 300

PEERS = {
    "REDACTED_PUBLIC_KEY_LAPTOP": "Laptop",
    "REDACTED_PUBLIC_KEY_MOBILE": "Mobile",
}
# ---------------------


def send_telegram(message: str) -> None:
    """Send a Telegram notification."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except requests.RequestException as e:
        print(f"[ERROR] Telegram notification failed: {e}")


def get_wireguard_peers() -> dict:
    """
    Parse `wg show wg0 dump` output.
    Returns dict of {public_key: last_handshake_timestamp}
    """
    try:
        result = subprocess.run(
            ["wg", "show", "wg0", "dump"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] wg show failed: {e}")
        return {}

    peers = {}
    lines = result.stdout.strip().split("\n")

    # First line is interface — skip it
    for line in lines[1:]:
        parts = line.split("\t")
        if len(parts) >= 5:
            public_key = parts[0]
            last_handshake = int(parts[4])  # Unix timestamp
            peers[public_key] = last_handshake

    return peers


def check_peers() -> None:
    """Check all peers and alert if any tunnel has dropped."""
    now = int(time.time())
    peers = get_wireguard_peers()

    if not peers:
        send_telegram("⚠️ *WireGuard Monitor*\nCould not retrieve peer data from wg0.")
        return

    for public_key, last_handshake in peers.items():
        peer_name = PEERS.get(public_key, f"Unknown ({public_key[:8]}...)")

        if last_handshake == 0:
            # Never connected
            print(f"[INFO] {peer_name}: never connected")
            continue

        seconds_since = now - last_handshake
        last_seen = datetime.fromtimestamp(last_handshake).strftime("%Y-%m-%d %H:%M:%S")

        if seconds_since > HANDSHAKE_THRESHOLD_SECONDS:
            message = (
                f"🔴 *WireGuard Tunnel Down*\n"
                f"Peer: `{peer_name}`\n"
                f"Last handshake: `{last_seen}`\n"
                f"Silence: `{seconds_since}s` (threshold: {HANDSHAKE_THRESHOLD_SECONDS}s)"
            )
            print(f"[ALERT] {peer_name} tunnel down — last handshake {seconds_since}s ago")
            send_telegram(message)
        else:
            print(f"[OK] {peer_name} — last handshake {seconds_since}s ago ({last_seen})")


if __name__ == "__main__":
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking WireGuard peers...")
    check_peers()
