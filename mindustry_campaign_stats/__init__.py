from pprint import pprint

from mindustry_campaign_stats.__version__ import __version__
from mindustry_campaign_stats.settings import load
from argparse import ArgumentParser
from sys import stdout
from enum import Enum
import json


class Planets(Enum):
    Serpulo = 'serpulo'
    Erekir = 'erekir'

    def __str__(self):
        return self.value


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
        type=Planets,
        choices=list(Planets)
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

    with open(args.filename, 'rb') as fp:
        pprint(load(fp))
        # json.dump(
        #     load(fp),
        #     stdout,
        #     indent=2 if args.pretty else None,
        #     separators=None if args.pretty else (',', ':')
        # )


__all__ = ['load']
