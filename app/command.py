import logging
import os
from app.export import Export
from app.plex import connect_plex


def export(args):
    plex = connect_plex()
    EXPORT_DIR = os.environ.get("EXPORT_DIR", "exports")
    if EXPORT_DIR == "exports":
        logging.warning(
            "No custom EXPORT_DIR set. Defaulting to exports directory.")
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)
    try:
        Export(plex, EXPORT_DIR).export(format="csv")
    except KeyboardInterrupt:
        logging.warning(
            "Ctrl + C User interrupt. Shutting down gracefully...")
