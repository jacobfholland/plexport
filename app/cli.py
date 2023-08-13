import argparse
from dotenv import load_dotenv
from app.command import export
from app.log import setup_logging
from app.environment import install_missing_packages, set_environment


def cli_entry():
    initialization()
    parser = argparse.ArgumentParser(
        description='Plexport - A utility for exporting and matching Plex library items.')
    subparsers = parser.add_subparsers(title='Subcommands', dest='subcommand')
    export_parser = subparsers.add_parser(
        'export', help='Export Plex library items.')
    export_parser.set_defaults(func=export)
    init_parser = subparsers.add_parser(
        'init', help='Initialize environment variables')
    init_parser.set_defaults(func=set_environment)
    init_parser.add_argument('--plex-url', help='URL of the Plex server')
    init_parser.add_argument('--plex-token', help='Plex authentication token')
    init_parser.add_argument(
        '--export-dir', default='exports', help='Directory for export files')
    init_parser.add_argument('--log-dir', default='logs',
                             help='Directory for log files')
    init_parser.add_argument(
        '--log-level', default='info', help='Log level for the application')
    parser.set_defaults(func=export)
    args = parser.parse_args()
    args.func(args)


def initialization():
    install_missing_packages()
    load_dotenv("/home/jacob/code/plexport/.env")
    setup_logging()
