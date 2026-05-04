import os
import json
import time
import argparse
import logging
import spotipy
from datetime import datetime
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

class SpotifyAuto:
    def __init__(self):
        load_dotenv()
        self.config = self._load_config()
        self.state_file = ".last_played"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback"),
            scope="user-modify-playback-state user-read-playback-state"
        ))

    def _load_config(self):
        with open('config.json', 'r') as f:
            return json.load(f)

    def get_target_playlist(self):
        hour = datetime.now().hour
        for period, settings in self.config.items():
            start, end = settings['start'], settings['end']
            if start > end:
                if hour >= start or hour < end:
                    return settings['playlist'], period
            else:
                if start <= hour < end:
                    return settings['playlist'], period
        return None, None

    def get_last_played(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return f.read().strip()
        return None

    def set_last_played(self, period):
        with open(self.state_file, 'w') as f:
            f.write(period)

    def play(self, force=False):
        playlist_uri, period = self.get_target_playlist()
        
        if not playlist_uri:
            logging.info("No scheduled playlist for this time.")
            return

        if not force and self.get_last_played() == period:
            logging.info(f"Already playing {period} playlist. Skipping to avoid loop.")
            return

        try:
            devices = self.sp.devices().get('devices', [])
            if not devices:
                logging.error("No active devices found. Please open Spotify.")
                return

            active_id = next((d['id'] for d in devices if d['is_active']), devices[0]['id'])
            self.sp.start_playback(device_id=active_id, context_uri=playlist_uri)
            logging.info(f"Playing {period} playlist: {playlist_uri}")
            self.set_last_played(period)
            
        except Exception as e:
            logging.error(f"Playback failed: {e}. Retrying in 30s...")
            time.sleep(30)
            self.play(force=force)

    def status(self):
        playlist, period = self.get_target_playlist()
        last = self.get_last_played()
        print(f"Current Period: {period if period else 'None'}")
        print(f"Last Played: {last if last else 'None'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spotify Automation CLI")
    parser.add_argument('command', choices=['run', 'once', 'status'])
    args = parser.parse_args()

    bot = SpotifyAuto()

    if args.command == 'run':
        logging.info("Starting scheduler loop...")
        while True:
            bot.play()
            time.sleep(300)
    elif args.command == 'once':
        bot.play(force=True)
    elif args.command == 'status':
        bot.status()
