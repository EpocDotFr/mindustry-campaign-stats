# Mindustry Campaign Stats

Python API and CLI tool to read [Parkitect](https://www.themeparkitect.com/)'s blueprints metadata.

![Python versions](https://img.shields.io/pypi/pyversions/mindustry-campaign-stats.svg) ![Version](https://img.shields.io/pypi/v/mindustry-campaign-stats.svg) ![License](https://img.shields.io/pypi/l/mindustry-campaign-stats.svg)

[PyPI](https://pypi.org/project/mindustry-campaign-stats/) - [Documentation](https://github.com/EpocDotFr/mindustry-campaign-stats?tab=readme-ov-file#usage) - [Source code](https://github.com/EpocDotFr/mindustry-campaign-stats) - [Issue tracker](https://github.com/EpocDotFr/mindustry-campaign-stats/issues) - [Changelog](https://github.com/EpocDotFr/mindustry-campaign-stats/releases)

## Prerequisites

  - Python >= 3.10

## Installation

### From PyPi

```shell
pip install mindustry-campaign-stats
```

### Locally

After cloning/downloading the repo:

```shell
pip install .
```

## Usage

### API

> [!NOTE]
> TODO

### CLI

> [!NOTE]
> TODO

## References

  - [Settings.java](https://github.com/Anuken/Arc/blob/master/arc-core/src/arc/Settings.java)

## Development

### Getting source code and installing the package with dev dependencies

  1. Clone the repository
  2. From the root directory, run: `pip install -e ".[dev]"`

### Releasing the package

From the root directory, run `python setup.py upload`. This will build the package, create a git tag and publish on PyPI.

`__version__` in `mindustry_campaign_stats/__version__.py` must be updated beforehand. It should adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

An associated GitHub release must be created following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.
