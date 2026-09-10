---
title: "Changelog"
description: "ArchBox version history — all releases with key changes, new models, and improvements."
---

# Changelog

The canonical changelog lives in [`CHANGELOG.md`](https://github.com/ArchBox-GARCH-Models/archbox/blob/main/CHANGELOG.md)
at the repository root and is included verbatim below, so this page can never
drift out of sync with the release notes.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
ArchBox adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Sections**: Added, Changed, Fixed, Deprecated, Removed, Security, Performance.

---

--8<-- "CHANGELOG.md"

---

## Versioning Policy

ArchBox uses [Semantic Versioning](https://semver.org/):

| Component | When incremented |
|---|---|
| **Major** (X.0.0) | Incompatible API changes |
| **Minor** (0.X.0) | New features, backward compatible |
| **Patch** (0.0.X) | Bug fixes, backward compatible |

!!! warning "Pre-1.0"
    ArchBox is alpha software (`Development Status :: 3 - Alpha`). Until 1.0.0,
    minor releases may contain breaking changes; those are always called out
    under a **BREAKING** heading in the changelog above.

---

## See Also

- [Contributing Guide](contributing.md) — How to contribute
- [Roadmap](roadmap.md) — Planned features
- [API Reference](../api/index.md) — Full API documentation
