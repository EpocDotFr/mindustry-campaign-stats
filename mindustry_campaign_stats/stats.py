from mindustry_campaign_stats.constants import Planet
from datetime import datetime, timezone
from typing import Dict, List
import re


class StatsBuilder:
	settings: Dict
	planet: Planet

	sectors_info: Dict

	def __init__(self, settings: Dict, planet: Planet):
		self.settings = settings
		self.planet = planet

		self.sectors_info = self.get_sectors_info()

	def build_sectors(self) -> Dict:
		return {
			sector_id: {
				'availability': sector_info.get('resources', []),
				'storage': {
					'capacity': sector_info.get('storageCapacity', 0),
					'items': sector_info.get('items', {})
				},
				'production': {
					item_name: item_info.get('mean', 0.0) for item_name, item_info in sector_info.get('rawProduction', {}).items() if item_info.get('mean', 0.0) != 0
				},
				# 'imports': {
				# 	'copper': {
				# 		58: 500,
				# 		41: 200,
				# 	}
				# },
				# 'exports': {
				# 	'copper': {
				# 		58: 500,
				# 		41: 200,
				# 	}
				# },
			} for sector_id, sector_info in self.sectors_info.items()
		}

	def build_totals(self) -> Dict:
		return {
			'storage': {
				'capacity': sum([sector_info.get('storageCapacity', 0) for sector_info in self.sectors_info.values()]),
				'items': {
					'copper': 1520,
					'titanium': 2000,
				}
			},
			'production': {
				'copper': 5000,
				'titanium': 5000,
			}
		}

	def get_sectors_info(self) -> Dict:
		sector_name_regex = re.compile(fr'{self.planet.value}-s-(?P<number>\d+)-info')

		sectors_info = {}

		for key, value in self.settings.items():
			sector_name_match = sector_name_regex.match(key)

			if not sector_name_match:
				continue

			sector_number = int(sector_name_match.groupdict()['number'])

			sectors_info[sector_number] = value

		return sectors_info

	def get_items_available(self, sector_info: Dict) -> List:
		return sector_info.get('resources', [])


def compute(settings: Dict, planet: Planet) -> Dict:
	builder = StatsBuilder(settings, planet)

	return {
		'date': datetime.now(timezone.utc).isoformat(timespec='seconds'),
		'planet': builder.planet.value,
		'sectors': builder.build_sectors(),
		'totals': builder.build_totals(),
	}


__all__ = ['compute']
