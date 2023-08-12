import os
import csv
import sys
import logging
import subprocess
import pkg_resources

required_packages = {'plexapi', 'coloredlogs'}
installed_packages = {pkg.key for pkg in pkg_resources.working_set}
missing_packages = required_packages - installed_packages
if missing_packages:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', '-r', 'requirements.txt'])

import plexapi
from plexapi.server import PlexServer
import coloredlogs
coloredlogs.install()

class AutoFlushStreamHandler(logging.StreamHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()

# Check if an environment variable for the log directory is set
LOG_DIR = os.getenv("LOG_DIR", "logs")

# Ensure the directory exists or create it
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure the logger to write logs to a file in the specified directory
log_filename = os.path.join(LOG_DIR, 'plex_export.log')
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    handlers=[logging.FileHandler(log_filename, mode='w'), AutoFlushStreamHandler()])


EXPORT_DIR = os.getenv("EXPORT_DIR", "exports")

if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)

PLEX_URL = 'http://192.168.0.61:32400'  # Change this to your Plex server address
PLEX_TOKEN = "1JgQUWRbVkssP3PhdW_U"  # You can use a token if you prefer

try:
    logging.info("Connecting to Plex server...")
    plex = PlexServer(PLEX_URL, PLEX_TOKEN, timeout=10)
    logging.info("Successfully connected to Plex server!")
except Exception as e:
    logging.error(f"Failed to connect to Plex server: {e}")
    raise

def get_tmdb_id(movie):
    prefix = 'com.plexapp.agents.themoviedb://'
    if movie.guid and movie.guid.startswith(prefix):
        return movie.guid[len(prefix):].split('?')[0]
    return None

# Scan every movie type library section
for section in plex.library.sections():
    if section.type == 'movie':
        logging.info(f"Processing library section: {section.title}")
        movies = section.all()
        filename = os.path.join(EXPORT_DIR, f"{section.title}.csv")

        # Extract more movie attributes and write to CSV
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            headers = ['Name', 'Year', 'TMDb Link', 'Rating', 'Summary', 'Duration (mins)', 'Genres', 'Directors', 'Writers', 'Actors', 'Resolution', 'Codec', 'Container', 'Bitrate', 'Size (MB)', 'Audio Channels', 'Added At', 'Updated At']
            writer.writerow(headers)  # Write the header
            
            for movie in movies:
                if movie.guid is None or movie.guid.startswith("local://"):
                    logging.warning(f"Unmatched movie detected: {movie.title}")
                tmdb_id = get_tmdb_id(movie)
                tmdb_link = f"https://www.themoviedb.org/movie/{tmdb_id}" if tmdb_id else None
                duration_mins = round(movie.duration / 60000) if movie.duration else None  # Convert duration from milliseconds to minutes
                genres = ', '.join([genre.tag for genre in movie.genres]) if movie.genres else None
                directors = ', '.join([director.tag for director in movie.directors]) if movie.directors else None
                writers = ', '.join([writer.tag for writer in movie.writers]) if movie.writers else None
                actors = ', '.join([actor.tag for actor in movie.actors]) if movie.actors else None

                if movie.media:
                    media = movie.media[0]  # Assuming you're interested in the primary media source
                    resolution = media.videoResolution
                    codec = media.videoCodec
                    container = media.container
                    bitrate = media.bitrate
                    size_MB = media.size / (1024 * 1024) if hasattr(media, 'size') else None  # Convert bytes to megabytes only if size attribute exists
                    audio_channels = media.audioChannels if media.audioChannels else None
                else:
                    resolution, codec, container, bitrate, size_MB, audio_channels = [None] * 6
                    logging.warning(f"Movie {movie.title} has no size")

                added_at = movie.addedAt.strftime('%Y-%m-%d %H:%M:%S') if movie.addedAt else None
                updated_at = movie.updatedAt.strftime('%Y-%m-%d %H:%M:%S') if movie.updatedAt else None

                writer.writerow([movie.title, movie.year, tmdb_link, movie.rating, movie.summary, duration_mins, genres, directors, writers, actors, resolution, codec, container, bitrate, size_MB, audio_channels, added_at, updated_at])

                logging.info(f"Added movie: {movie.title} ({movie.year}) to {filename}")

logging.info("Export completed!")
