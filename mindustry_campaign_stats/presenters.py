from mindustry_campaign_stats.constants import ItemsId
from mindustry_campaign_stats.stats import Stats
from tabulate import tabulate
import humanize
import json


def table(computed_stats: Stats) -> str:
    date = computed_stats.date.astimezone().strftime('%c')

    table_headers = ['Sector', 'Stat']

    table_headers.extend([
        item_id for item_id in ItemsId.get(computed_stats.planet)
    ])

    table_data = [
        [
            sector.name,
            f'Available\nStorage (max. {humanize.metric(sector.storage.capacity, precision=1)})\nProduction (/m)'
        ] for sector in computed_stats.sectors.values()
    ]

    table_data.append([
        'Totals',
        f'Storage (max. {humanize.metric(computed_stats.totals.storage.capacity, precision=1)})\nProduction (/m)',
    ])

    table = tabulate(
        table_data,
        table_headers,
        'rounded_grid'
    )

    return f'{date} - {computed_stats.planet.name}\n{table}\n'


def jsonl(computed_stats: Stats) -> str:
    return json.dumps(
        computed_stats.to_dict(),
        indent=None,
        separators=(',', ':')
    ) + '\n'


__all__ = ['table', 'jsonl']
