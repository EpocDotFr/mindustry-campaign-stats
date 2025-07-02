from mindustry_campaign_stats.constants import ItemsId
from mindustry_campaign_stats.stats import Stats, SectorStats, TotalsStats
from tabulate import tabulate
from typing import List
import humanize
import json


def to_table(computed_stats: Stats) -> str:
    date = computed_stats.date.astimezone().strftime('%c')

    table_headers = ['Sector', 'Stat']

    table_headers.extend([
        item_id.replace('-', '\n').title() for item_id in ItemsId.get(computed_stats.planet)
    ])

    def row_data(sector: SectorStats) -> List:
        stat_labels_cell = [
            'Available',
            f'Storage ({humanize.metric(sector.storage.capacity, precision=1)})',
            'Production (/s)'
        ]

        if sector.imports:
            stat_labels_cell.append('Imports (/s)')

        if sector.exports:
            stat_labels_cell.append('Exports (/s)')

        ret = [
            sector.name,
            '\n'.join(stat_labels_cell)
        ]

        for item_id in ItemsId.get(computed_stats.planet):
            stat_values_cell = [
                '✓' if item_id in sector.availability else '✕',
                humanize.metric(sector.storage.items.get(item_id, 0), precision=1),
                humanize.metric(sector.production.get(item_id, 0), precision=2)
            ]

            if item_id in sector.imports:
                stat_values_cell.append(humanize.metric(sector.imports.get(item_id, 0), precision=2))


            if item_id in sector.exports:
                stat_values_cell.append(humanize.metric(sector.exports.get(item_id, 0), precision=2))

            ret.append(
                '\n'.join(stat_values_cell)
            )

        return ret

    def totals_row_data(totals: TotalsStats) -> List:
        ret = [
            'Totals',
            f'Storage ({humanize.metric(computed_stats.totals.storage.capacity, precision=1)})\nProduction (/s)',
        ]

        ret.extend([
            '\n'.join([
                humanize.metric(totals.storage.items.get(item_id, 0), precision=1),
                humanize.metric(totals.production.get(item_id, 0), precision=2)
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


def to_json(computed_stats: Stats, pretty: bool) -> str:
    return json.dumps(
        computed_stats.to_dict(),
        indent=2 if pretty else None,
        separators=None if pretty else (',', ':')
    ) + '\n'


__all__ = ['to_table', 'to_json']
