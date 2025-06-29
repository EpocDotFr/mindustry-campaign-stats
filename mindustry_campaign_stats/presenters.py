from mindustry_campaign_stats.constants import ItemsId
from mindustry_campaign_stats.stats import Stats, SectorStats, TotalsStats
from tabulate import tabulate
from typing import List
import humanize
import json


def table(computed_stats: Stats) -> str:
    date = computed_stats.date.astimezone().strftime('%c')

    table_headers = ['Sector', 'Stat']

    table_headers.extend([
        item_id.replace('-', ' ').title() for item_id in ItemsId.get(computed_stats.planet)
    ])

    def row_data(sector: SectorStats) -> List:
        ret = [
            sector.name,
            f'Available\nStorage (max. {humanize.metric(sector.storage.capacity, precision=1)})\nProduction (/m)'
        ]

        ret.extend([
            '\n'.join([
                '✅' if item_id in sector.availability else '❌',
                humanize.metric(sector.storage.items.get(item_id, 0), precision=1),
                humanize.metric(sector.production.get(item_id, 0), precision=1)
            ]) for item_id in ItemsId.get(computed_stats.planet)
        ])

        return ret

    def totals_row_data(totals: TotalsStats) -> List:
        ret = [
            'Totals',
            f'Storage (max. {humanize.metric(computed_stats.totals.storage.capacity, precision=1)})\nProduction (/m)',
        ]

        ret.extend([
            '\n'.join([
                humanize.metric(totals.storage.items.get(item_id, 0), precision=1),
                humanize.metric(totals.production.get(item_id, 0), precision=1)
            ]) for item_id in ItemsId.get(computed_stats.planet)
        ])

        return ret

    table_data = [
        row_data(sector) for sector in computed_stats.sectors.values()
    ]

    table_data.append(
        totals_row_data(computed_stats.totals)
    )

    table_str = tabulate(
        table_data,
        table_headers,
        'rounded_grid'
    )

    return f'{date} - {computed_stats.planet.name}\n{table_str}\n'


def jsonl(computed_stats: Stats) -> str:
    return json.dumps(
        computed_stats.to_dict(),
        indent=None,
        separators=(',', ':')
    ) + '\n'


__all__ = ['table', 'jsonl']
