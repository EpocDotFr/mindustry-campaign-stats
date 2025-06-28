from mindustry_campaign_stats.constants import Planet, SectorsName
from datetime import datetime, timezone
from typing import Dict, List, Union
import dataclasses
import re


@dataclasses.dataclass
class StorageStats:
	capacity: int
	items: Dict[str, int]


@dataclasses.dataclass
class HasStorageAndProductionStatsMixin:
	storage: StorageStats
	production: Dict[str, int]


@dataclasses.dataclass
class SectorStats(HasStorageAndProductionStatsMixin):
	name: str
	availability: List[str]


@dataclasses.dataclass
class TotalsStats(HasStorageAndProductionStatsMixin):
	pass


@dataclasses.dataclass
class Stats:
	date: datetime
	planet: Planet
	sectors: Dict[int, SectorStats]
	totals: TotalsStats

	def to_json(self) -> Dict:
		ret = dataclasses.asdict(self)

		ret['date'] = ret['date'].isoformat()
		ret['planet'] = ret['planet'].value

		return ret


class StatsBuilder:
	settings: Dict[str, Union[bool, float, int, bytes, str]]
	planet: Planet

	sectors_info: Dict[int, Dict]

	def __init__(self, settings: Dict[str, Union[bool, float, int, bytes, str]], planet: Planet):
		self.settings = settings
		self.planet = planet

		self.sectors_info = self.get_sectors_info()

	def build_sectors(self) -> Dict:
		return {
			sector_id: SectorStats(
				name=SectorsName.get(sector_id, sector_id),
				availability=sector_info.get('resources', []),
				storage=StorageStats(
					capacity=sector_info.get('storageCapacity', 0),
					items=sector_info.get('items', {})
				),
				production={
					item_name: item_info.get('mean', 0.0) for item_name, item_info in sector_info.get('rawProduction', {}).items() if item_info.get('mean', 0.0) != 0
				}
			) for sector_id, sector_info in self.sectors_info.items()
		}

	def build_totals(self) -> TotalsStats:
		return TotalsStats(
			storage=StorageStats(
				capacity=sum([sector_info.get('storageCapacity', 0) for sector_info in self.sectors_info.values()]),
				items={ # TODO
					'copper': 1520,
					'titanium': 2000,
				}
			),
			production={ # TODO
				'copper': 5000,
				'titanium': 5000,
			}
		)

	def get_sectors_info(self) -> Dict[int, Dict]:
		sector_name_regex = re.compile(fr'{self.planet.value}-s-(?P<number>\d+)-info')

		sectors_info = {}

		for key, value in self.settings.items():
			sector_name_match = sector_name_regex.match(key)

			if not sector_name_match:
				continue

			sector_number = int(sector_name_match.groupdict()['number'])

			sectors_info[sector_number] = value

		return sectors_info


def compute(settings: Dict[str, Union[bool, float, int, bytes, str]], planet: Planet) -> Stats:
	builder = StatsBuilder(settings, planet)

	return Stats(
		date=datetime.now(timezone.utc),
		planet=planet,
		sectors=builder.build_sectors(),
		totals=builder.build_totals()
	)


__all__ = ['compute', 'Stats']
