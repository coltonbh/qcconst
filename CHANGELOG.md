# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]

## [0.1.2] - 2025-04-01

### Changed

- GitHub workflows now trigger on `pull_request` and only pushes to `master`.
- Version update in `release.py` now happens with `re` package rather than `poetry`.
- Added `write` permission to `create-release.yaml` GitHub action.

## [0.1.1] - 2025-03-24

### Added

- `constants.HARTREE_TO_EV` and `constants.EV_TO_HARTREE`.

## [0.1.0] - 2025-03-21

### Added

- Core physical constants, periodic table, and solvent properties.
- Common API for showing available constants and solvents.

[unreleased]: https://github.com/coltonbh/qcconst/compare/0.1.2...HEAD
[0.1.2]: https://github.com/coltonbh/qcconst/releases/tag/0.1.2
[0.1.1]: https://github.com/coltonbh/qcconst/releases/tag/0.1.1
[0.1.0]: https://github.com/coltonbh/qcconst/releases/tag/0.1.0
