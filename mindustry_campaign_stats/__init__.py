from mindustry_campaign_stats.__version__ import __version__
from mindustry_campaign_stats.constants import Planet
from mindustry_campaign_stats.settings import load
from mindustry_campaign_stats.stats import compute
from argparse import ArgumentParser
from tabulate import tabulate
from sys import stdout
import json


def cli() -> None:
    arg_parser = ArgumentParser(
        description='CLI tool to read Mindustry\'s campaign global stats.'
    )

    arg_parser.add_argument(
        'filename',
        help='The settings.bin file to load'
    )

    arg_parser.add_argument(
        'planet',
        help='Which campaign to retrieve stats for',
        type=Planet,
        choices=list(Planet)
    )

    arg_parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'parkitect-blueprint-reader {__version__}'
    )

    arg_parser.add_argument(
        '-j', '--json',
        help='Output JSON instead of table',
        action='store_true'
    )

    arg_parser.add_argument(
        '-r', '--refresh',
        help='Listen for file changes',
        action='store_true'
    )

    args = arg_parser.parse_args()

    with open(args.filename, 'rb') as fp:
        settings = load(fp)

    json.dump(
        compute(settings, args.planet),
        stdout,
        indent=None,
        separators=(',', ':')
    )


__all__ = ['load', 'compute']
