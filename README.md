# spotify-auto
> Automates Spotify playlist tasks using Python and Bash scripts.

![Python](https://img.shields.io/badge/python-3.10+-blue) ![Shell](https://img.shields.io/badge/shell-bash-green) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

## What it does
Automates repetitive Spotify playlist operations via the Spotify API.
Uses Bash scripts for Linux environment setup and task scheduling.
Reduces manual playlist management to a single command.

## Tech Stack
- Python, Shell/Bash, Spotify Web API

## Quick Start
```bash
git clone https://github.com/Husseinuahmedc/spotify-auto
cd spotify-auto
pip install -r requirements.txt
bash run.sh
```

## Structure
```
spotify-auto/
├── main.py
├── install.sh
├── requirements.txt
└── README.md
```

## Notes
Requires Spotify Developer credentials. Set CLIENT_ID and CLIENT_SECRET in .env file.
