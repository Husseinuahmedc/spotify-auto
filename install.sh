#!/bin/bash
echo "Setting up spotify-auto..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
echo "Setup complete. Please edit .env and config.json."
