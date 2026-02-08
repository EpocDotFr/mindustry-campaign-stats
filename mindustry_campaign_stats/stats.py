from mindustry_campaign_stats.constants import Planet, SectorNames, ItemIds
from typing import Dict, List, Union, Optional
from datetime import datetime, timezone
import dataclasses
import re


@dataclasses.dataclass
class StorageStats:
    capacity: int
    items: Dict[str, int]


@dataclasses.dataclass
class StorageAndProductionStatsMixin:
    storage: StorageStats
    rawProduction: Dict[str, float]  # Per minute
    netProduction: Dict[str, float]  # Per minute


@dataclasses.dataclass
class SectorStats(StorageAndProductionStatsMixin):
    name: str
    availability: List[str]
    imports: Dict[str, float]  # Per minute
    exports: Dict[str, float]  # Per minute


@dataclasses.dataclass
class TotalsStats(StorageAndProductionStatsMixin):
    pass


@dataclasses.dataclass
class Stats:
    date: datetime
    planet: Planet
    totals: TotalsStats
    sectors: Optional[Dict[int, SectorStats]] = None

    def to_dict(self) -> Dict:
        ret = dataclasses.asdict(self)

        ret['date'] = ret['date'].isoformat()
        ret['planet'] = ret['planet'].value

        if not ret['sectors']:
            del ret['sectors']

        return ret


class StatsBuilder:
    settings: Dict[str, Union[bool, float, int, bytes, str]]
    planet: Planet
    items: Optional[List[str]] = None
    sectors: Optional[List[str]] = None

    eligible_sectors: Dict[int, Dict]
    eligible_items: List[str]

    def __init__(
        self,
        settings: Dict[str, Union[bool, float, int, bytes, str]],
        planet: Planet,
        items: Optional[List[str]] = None,
        sectors: Optional[List[str]] = None
    ):
        self.settings = settings
        self.planet = planet
        self.items = items
        self.sectors = sectors

        self.eligible_sectors = self.get_eligible_sectors()
        self.eligible_items = self.get_eligible_items()

    def build_sectors(self) -> Dict:
        return {
            sector_id: SectorStats(
                name=SectorNames.get(self.planet).get(sector_id, str(sector_id)),
                availability=sector_info.get('resources', []),
                storage=StorageStats(
                    capacity=sector_info.get('storageCapacity', 0),
                    items=sector_info.get('items', {})
                ),
                rawProduction={
                    item_id: item_info.get('mean', 0) * 60 for item_id, item_info in
                    sector_info.get('rawProduction', {}).items()
                },
                netProduction={
                    item_id: item_info.get('mean', 0) * 60 for item_id, item_info in
                    sector_info.get('production', {}).items()
                },
                imports={
                    item_id: item_info.get('mean', 0) * 60 for item_id, item_info in
                    sector_info.get('imports', {}).items()
                },
                exports={
                    item_id: item_info.get('mean', 0) * 60 for item_id, item_info in
                    sector_info.get('export', {}).items()
                }
            ) for sector_id, sector_info in self.eligible_sectors.items()
        }

    def build_totals(self) -> TotalsStats:
        return TotalsStats(
            storage=StorageStats(
                capacity=sum([
                    sector_info.get('storageCapacity', 0) for sector_info in self.eligible_sectors.values()
                ]),
                items={
                    item_id: sum([
                        sector_info.get('items', {}).get(item_id, 0) for sector_info in self.eligible_sectors.values()
                    ]) for item_id in self.eligible_items
                }
            ),
            rawProduction={
                item_id: sum([
                    sector_info.get('rawProduction', {}).get(item_id, {}).get('mean', 0) * 60 for sector_info in
                    self.eligible_sectors.values() if sector_info.get('rawProduction', {}).get(item_id, {}).get('mean', 0)
                ]) for item_id in self.eligible_items
            },
            netProduction={
                item_id: sum([
                    sector_info.get('production', {}).get(item_id, {}).get('mean', 0) * 60 for sector_info in
                    self.eligible_sectors.values() if sector_info.get('production', {}).get(item_id, {}).get('mean', 0)
                ]) for item_id in self.eligible_items
            }
        )

    def get_eligible_sectors(self) -> Dict[int, Dict]:
        sector_name_regex = re.compile(fr'{self.planet.value}-s-(?P<number>\d+)-info')

        sectors_info = {}

        for key, value in self.settings.items():
            sector_name_match = sector_name_regex.match(key)

            if not sector_name_match:
                continue

            sector_number = int(sector_name_match.groupdict()['number'])

            if self.sectors:
                sector_name = SectorNames.get(self.planet).get(sector_number, str(sector_number)).lower()

                if not any([name for name in self.sectors if name.lower() in sector_name]):
                    continue

            sectors_info[sector_number] = value

        return sectors_info

    def get_eligible_items(self) -> List[str]:
        if not self.items:
            return ItemIds.get(self.planet)

        return [
            item_id for item_id in ItemIds.get(self.planet) if any([name for name in self.items if name.lower() in item_id.lower()])
        ]


def compute(
        settings: Dict[str, Union[bool, float, int, bytes, str]],
        planet: Planet,
        totals_only: bool = False,
        items: Optional[List[str]] = None,
        sectors: Optional[List[str]] = None
) -> Stats:
    builder = StatsBuilder(settings, planet, items, sectors)

    return Stats(
        date=datetime.now(timezone.utc),
        planet=planet,
        totals=builder.build_totals(),
        sectors=builder.build_sectors() if not totals_only else None
    )
