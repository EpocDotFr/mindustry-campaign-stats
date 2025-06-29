from enum import StrEnum


class Planet(StrEnum):
    Serpulo = 'serpulo'
    Erekir = 'erekir'


SectorsName = {
    Planet.Serpulo: {
        1: 'Atolls',
        3: 'Testing Grounds',
        15: 'Ground Zero',
        18: 'The Craters',
        20: 'Stained Mountains',
        21: 'Fungal Pass',
        23: 'Tar Fields',
        39: 'Weathered Channels',
        47: 'Sea Port',
        50: 'Frontier',
        54: 'Cruxscape',
        64: 'Facility 32M',
        81: 'Biomass Synthesis Facility',
        86: 'Frozen Forest',
        93: 'Planetary Launch Terminal',
        101: 'Salt Flats',
        108: 'Coastline',
        123: 'Desolate Rift',
        130: 'Nuclear Production Complex',
        134: 'Overgrowth',
        165: 'Extraction Outpost',
        210: 'Infested Canyons',
        213: 'Ruinous Shores',
        216: 'Naval Fortress',
        221: 'Tainted Woods',
        227: 'Impact 0078',
        246: 'Windswept Islands',
        260: 'Mycelia Bastion',
        264: 'Geothermal Stronghold',
    },
}

ItemsId = {
    Planet.Serpulo: [
        'blast-compound',
        'coal',
        'copper',
        'graphite',
        'lead',
        'metaglass',
        'phase-fabric',
        'plastanium',
        'pyratite',
        'scrap',
        'sand',
        'thorium',
        'titanium',
        'silicon',
        'spore-pod',
        'surge-alloy',
    ],
    Planet.Erekir: [
        'beryllium',
        'carbide',
        'dormant-cyst',
        'fissile-matter',
        'graphite',
        'oxide',
        'phase-fabric',
        'thorium',
        'tungsten',
        'silicon',
        'surge-alloy',
    ]
}