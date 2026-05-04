# spotify-auto 🎵

## Problem

Manual playlist switching wastes time. Human interrupts flow.
`spotify-auto` automates playback using time-based rules via Spotify API.

---

## Features

* Time-based playlist switching
* Cross-midnight scheduling (e.g. 18 → 5)
* Stateful control (no repeat triggering)
* Works as background service (Linux `systemd`)
* Android automation support (Tasker)
* Environment-based secrets handling

---

## Architecture

* **Scheduler** → checks current hour
* **State Machine** → avoids duplicate playback
* **Spotify Client** → sends playback command
* **Runtime Layer** → loop / systemd / Tasker

---

## Demo

![Demo](https://via.placeholder.com/600x300?text=Spotify+Auto+Demo)

---

## Setup

### 1. Clone

```bash
git clone git@github.com:Husseinuahmedc/spotify-auto.git
cd spotify-auto
```

---

### 2. Install

```bash
chmod +x install.sh
./install.sh
```

---

### 3. Environment

Create `.env`:

```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

Get credentials from Spotify Developer Dashboard.

---

### 4. Config

Edit `config.json`:

```json
{
  "morning": {
    "start": 6,
    "end": 8,
    "playlist": "spotify:playlist:XXXX"
  },
  "night": {
    "start": 18,
    "end": 5,
    "playlist": "spotify:playlist:YYYY"
  }
}
```

---

## Usage

Run once:

```bash
python main.py once
```

Run loop:

```bash
python main.py run
```

Check status:

```bash
python main.py status
```

---

## Linux (systemd)

Create service:

```bash
sudo nano /etc/systemd/system/spotify-auto.service
```

```ini
[Unit]
Description=Spotify Auto Scheduler
After=network.target

[Service]
WorkingDirectory=/path/to/spotify-auto
ExecStart=/path/to/spotify-auto/venv/bin/python main.py run
Restart=always
RestartSec=10
User=yourusername

[Install]
WantedBy=multi-user.target
```

Enable:

```bash
sudo systemctl daemon-reload
sudo systemctl enable spotify-auto
sudo systemctl start spotify-auto
```

---

## Android (Tasker)

Method A:

* Time trigger
* Open playlist via intent

```
Action: android.intent.action.VIEW
Data: spotify:playlist:XXXX
```

Method B:

* Use Termux
* Run Python script

---

## Design

* Uses `datetime.hour`
* Cross-midnight: OR logic
* Select active device or fallback
* Skip if same period already played

---

## Limits

* Needs active Spotify device
* Needs internet
* Mobile background unreliable

---

## Future

* Location triggers
* Calendar sync
* GUI
* Multi-user
* Smart recommendations

---

## License

MIT

---

## Summary

Time → evaluate → select playlist → play → store state.
Loop every 5 minutes.
