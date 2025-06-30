from mindustry_campaign_stats.presenters import to_json, to_table
from mindustry_campaign_stats.__version__ import __version__
from mindustry_campaign_stats.constants import Planet
from mindustry_campaign_stats.settings import load
from mindustry_campaign_stats.stats import compute
from argparse import ArgumentParser
from sys import stdout


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
        help='Output JSON instead of a table',
        action='store_true'
    )

    arg_parser.add_argument(
        '-p', '--pretty',
        help='Pretty-print JSON output',
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
        to_json(computed_stats, args.pretty) if args.json else to_table(computed_stats)
    )


__all__ = ['load', 'compute', 'jsonl', 'table']
