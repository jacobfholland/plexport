import logging
import os
from plexapi.server import PlexServer
from plexapi.exceptions import Unauthorized
from requests.exceptions import ConnectionError


def connect_plex():
    try:
        PLEX_URL = os.environ.get("PLEX_URL")
        PLEX_TOKEN = os.environ.get("PLEX_TOKEN")
        logging.info("Connecting to Plex server...")
        plex = PlexServer(PLEX_URL, PLEX_TOKEN, timeout=10)
        logging.info("Successfully connected to Plex server!")
    except Unauthorized as e:
        logging.error(f"Failed to connect to Plex server: 401 Unauthorized. Check your PLEX_URL and PLEX_TOKEN")
    except ConnectionError as e:
        logging.error(f"Failed to connect to Plex server: {e}")
    except Exception as e:
        logging.error(f"Failed to connect to Plex server: {e}")
    return plex