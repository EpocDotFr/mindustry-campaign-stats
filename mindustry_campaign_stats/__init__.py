from mindustry_campaign_stats.__version__ import __version__
from mindustry_campaign_stats.presenters import jsonl, table
from mindustry_campaign_stats.constants import Planet
from mindustry_campaign_stats.settings import load
from mindustry_campaign_stats.stats import compute
from argparse import ArgumentParser
from sys import stdout
import locale


def cli() -> None:
    locale.setlocale(locale.LC_ALL, '')

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
        help='Output JSON instead of a table',
        action='store_true'
    )

    arg_parser.add_argument(
        '-r', '--refresh',
        help='Listen for file changes',
        action='store_true'
    )

    args = arg_parser.parse_args()

    with open(args.filename, 'rb') as fp:
        settings_parsed = load(fp)

    computed_stats = compute(settings_parsed, args.planet)

    stdout.write(
        jsonl(computed_stats) if args.json else table(computed_stats)
    )


__all__ = ['load', 'compute', 'jsonl', 'table']
