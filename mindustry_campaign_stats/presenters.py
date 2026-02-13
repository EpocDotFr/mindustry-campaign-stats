from mindustry_campaign_stats.constants import ItemIds, ItemColors
from mindustry_campaign_stats.stats import Stats
from math import log10, floor
from rich.table import Table
import json


def humanize_number(value, significant_digits=3, strip_trailing_zeros=True):
    powers = [10 ** x for x in (12, 9, 6, 3, 0, -3, -6, -9)]
    human_powers = ['T', 'B', 'M', 'k', '', 'm', 'µ', 'n']
    is_negative = False
    suffix = ''

    if not isinstance(value, float):
        value = float(value)
    if value < 0:
        is_negative = True
        value = abs(value)
    if value == 0:
        decimal_places = max(0, significant_digits - 1)
    elif .001 <= value < 1:
        decimal_places = max(0, significant_digits - int(floor(log10(value))) - 1)
    else:
        p = next((x for x in powers if value >= x), 10 ** -9)
        i = powers.index(p)
        value = value / p
        before = int(log10(value)) + 1
        decimal_places = max(0, significant_digits - before)
        suffix = ' ' + human_powers[i]

    return_value = ("%." + str(decimal_places) + "f") % value

    if is_negative:
        return_value = "-" + return_value
    if strip_trailing_zeros and '.' in return_value:
        return_value = return_value.rstrip('0').rstrip('.')

    return f'{return_value}{suffix}'


def to_table(computed_stats: Stats, compact: bool = False) -> Table:
    date = computed_stats.date.astimezone().strftime('%c')

    ret = Table(
        title=f'{date} - {computed_stats.planet.name}'
    )

    item_ids = computed_stats.totals.storage.items.keys()

    if not computed_stats.sectors: # Totals only mode
        # Header
        ret.add_column('Item')
        ret.add_column('Storage')
        ret.add_column('Raw production (/m)')
        ret.add_column('Net production (/m)')

        for item_id in item_ids:
            if compact and computed_stats.totals.storage.items.get(item_id, 0) == 0 and computed_stats.totals.rawProduction.get(item_id, 0) == 0:
                continue

            row = [
                item_id.replace('-', ' ').title(),
                humanize_number(computed_stats.totals.storage.items.get(item_id, 0)),
                humanize_number(computed_stats.totals.rawProduction.get(item_id, 0)),
                humanize_number(computed_stats.totals.netProduction.get(item_id, 0)),
            ]

            ret.add_row(
                *row,
                style=ItemColors.get(item_id),
                end_section=True
            )
    else: # Normal mode
        ret.show_footer = True

        # Header
        ret.add_column(
            'Sector',
            footer='Totals'
        )

        ret.add_column(
            'Stat',
            footer=f'Storage ({humanize_number(computed_stats.totals.storage.capacity)})\nRaw prod. (/m)\nNet prod. (/m)',
            no_wrap=True
        )

        sector_item_ids = []

        for item_id in item_ids:
            if compact and computed_stats.totals.storage.items.get(item_id, 0) == 0 and computed_stats.totals.rawProduction.get(item_id, 0) == 0:
                continue

            ret.add_column(
                item_id.replace('-', '\n').title(),
                footer='\n'.join([
                    humanize_number(computed_stats.totals.storage.items.get(item_id, 0)),
                    humanize_number(computed_stats.totals.rawProduction.get(item_id, 0)),
                    humanize_number(computed_stats.totals.netProduction.get(item_id, 0)),
                ]),
                style=ItemColors.get(item_id),
                header_style=ItemColors.get(item_id),
                footer_style=ItemColors.get(item_id),
                no_wrap=True
            )

            sector_item_ids.append(item_id)

        # Body
        for sector in sorted(computed_stats.sectors.values(), key=lambda sector: sector.name):
            if compact:
                items_unavailable_anywhere = len([
                    item_id for item_id in sector_item_ids if item_id not in sector.availability
                ]) == len(sector_item_ids)

                items_storage_empty = sum([
                    sector.storage.items.get(item_id, 0) for item_id in sector_item_ids
                ]) == 0

                no_raw_production = sum([
                    sector.rawProduction.get(item_id, 0) for item_id in sector_item_ids
                ]) == 0

                no_net_production = sum([
                    sector.netProduction.get(item_id, 0) for item_id in sector_item_ids
                ]) == 0

                if items_unavailable_anywhere and items_storage_empty and no_raw_production and no_net_production:
                    continue

            stat_labels_cell = [
                'Available',
                f'Storage ({humanize_number(sector.storage.capacity)})',
                'Raw prod. (/m)',
                'Net prod. (/m)',
            ]

            if sector.imports:
                stat_labels_cell.append('Imports (/m)')

            if sector.exports:
                stat_labels_cell.append('Exports (/m)')

            row = [
                str(sector.name).replace(' ', '\n'),
                '\n'.join(stat_labels_cell)
            ]

            for item_id in sector_item_ids:
                stat_values_cell = [
                    '[green]✓[/green]' if item_id in sector.availability else '[red]✕[/red]',
                    humanize_number(sector.storage.items.get(item_id, 0)),
                    humanize_number(sector.rawProduction.get(item_id, 0)),
                    humanize_number(sector.netProduction.get(item_id, 0)),
                ]

                if item_id in sector.imports:
                    stat_values_cell.append(humanize_number(sector.imports.get(item_id, 0)))

                if item_id in sector.exports:
                    stat_values_cell.append(humanize_number(sector.exports.get(item_id, 0)))

                row.append(
                    '\n'.join(stat_values_cell)
                )

            ret.add_row(
                *row,
                end_section=True
            )

    return ret


def to_json(computed_stats: Stats, pretty: bool) -> str:
    return json.dumps(
        computed_stats.to_dict(),
        indent=2 if pretty else None,
        separators=None if pretty else (',', ':')
    )
