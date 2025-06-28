from mindustry_campaign_stats.stats import Stats
from tabulate import tabulate
from typing import Dict
import json


def table(computed_stats: Stats) -> str:
    date = computed_stats.date.astimezone().strftime('%c')

    ret = f'{date} - {computed_stats.planet.name}\n'

    return ret


def jsonl(computed_stats: Stats) -> str:
    return json.dumps(
        computed_stats.to_json(),
        indent=None,
        separators=(',', ':')
    ) + '\n'


__all__ = ['table', 'jsonl']
