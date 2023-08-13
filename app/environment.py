import subprocess
import sys
import pkg_resources
import os


def install_missing_packages():
    required_packages = {'plexapi', 'coloredlogs'}
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    missing_packages = required_packages - installed_packages
    if missing_packages:
        python = sys.executable
        subprocess.check_call(
            [python, '-m', 'pip', 'install', '--user', '-r', 'requirements.txt'])


def set_environment(args):
    if args.plex_url:
        os.environ['PLEX_URL'] = args.plex_url
    elif os.environ.get("PLEX_URL"):
        os.environ['PLEX_URL'] = os.environ.get("PLEX_URL")
    else:
        os.environ['PLEX_URL'] = "None"

    if args.plex_token:
        os.environ['PLEX_TOKEN'] = args.plex_token
    elif os.environ.get("PLEX_TOKEN"):
        os.environ['PLEX_TOKEN'] = os.environ.get("PLEX_TOKEN")
    else:
        os.environ['PLEX_TOKEN'] = "None"

    if args.export_dir:
        os.environ['EXPORT_DIR'] = args.export_dir
    elif os.environ.get("EXPORT_DIR"):
        os.environ['EXPORT_DIR'] = os.environ.get("EXPORT_DIR")
    else:
        os.environ['EXPORT_DIR'] = "logs"

    if args.log_dir:
        os.environ['LOG_DIR'] = args.log_dir
    elif os.environ.get("LOG_DIR"):
        os.environ['LOG_DIR'] = os.environ.get("LOG_DIR")
    else:
        os.environ['LOG_DIR'] = "logs"

    if args.log_level:
        os.environ['LOG_LEVEL'] = args.log_level
    elif os.environ.get("LOG_LEVEL"):
        os.environ['LOG_LEVEL'] = os.environ.get("LOG_LEVEL")
    else:
        os.environ['LOG_LEVEL'] = "info"

    with open('.env', 'w') as f:
        f.write(f"PLEX_URL={os.environ.get('PLEX_URL')}\n")
        f.write(f"PLEX_TOKEN={os.environ.get('PLEX_TOKEN')}\n")
        f.write(f"EXPORT_DIR={os.environ.get('EXPORT_DIR')}\n")
        f.write(f"LOG_DIR={os.environ.get('LOG_DIR')}\n")
        f.write(f"LOG_LEVEL={os.environ.get('LOG_LEVEL')}\n")
