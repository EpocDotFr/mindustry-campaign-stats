from mindustry_campaign_stats.__version__ import __version__
from argparse import ArgumentParser


def cli() -> None:
    arg_parser = ArgumentParser(
        description='CLI tool to read Mindustry\'s campaign global stats.'
    )

    arg_parser.add_argument(
        'planet',
        help='Which campaign to retrieve stats for',
        choices=['serpulo', 'erekir'],
        default='serpulo',
        nargs='?'
    )

    arg_parser.add_argument(
        'settings',
        help='The settings.bin file to load. Do not set to enable auto discovery',
        nargs='?'
    )

    arg_parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'parkitect-blueprint-reader {__version__}'
    )

    arg_parser.add_argument(
        '-j', '--json',
        help='Output JSON instead of tabular data',
        action='store_true'
    )

    arg_parser.add_argument(
        '-p', '--pretty',
        help='Pretty-print JSON output',
        action='store_true'
    )

    arg_parser.add_argument(
        '-r', '--refresh',
        help='Automatically refresh data on file change',
        action='store_true'
    )

    args = arg_parser.parse_args()
