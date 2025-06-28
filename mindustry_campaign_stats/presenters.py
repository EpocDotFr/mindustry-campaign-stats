from mindustry_campaign_stats.stats import Stats
from tabulate import tabulate
import humanize
import json


def table(computed_stats: Stats) -> str:
    date = computed_stats.date.astimezone().strftime('%c')

    table_data = [
        [
            sector.name,
            f'Available\nStorage (max. {humanize.metric(sector.storage.capacity)})\nProduction (/m)'
        ] for sector in computed_stats.sectors.values()
    ]

    table_data.append([
        'Totals',
        f'Storage (max. {humanize.metric(computed_stats.totals.storage.capacity)})\nProduction (/m)',
    ])

    table = tabulate(
        table_data,
        ['Sector', 'Stat'],
        'rounded_grid'
    )

    return f'{date} - {computed_stats.planet.name}\n{table}\n'


def jsonl(computed_stats: Stats) -> str:
    return json.dumps(
        computed_stats.to_json(),
        indent=None,
        separators=(',', ':')
    ) + '\n'


__all__ = ['table', 'jsonl']
