# CLAUDE.md

This file provides **mandatory instructions** to Claude Code (claude.ai/code) when working with code in this repository.

---

## 🌐 ECOSYSTEM DOCUMENTATION HUB

**This repository (ldt-data) is the central documentation hub for the entire LatterDay Tools ecosystem.**

Before making changes to ANY LDT repository, you MUST read:

1. **[docs/ECOSYSTEM.md](docs/ECOSYSTEM.md)** - Overview of all 8 repositories and their relationships
2. **[docs/ROADMAP.md](docs/ROADMAP.md)** - Development phases, priorities, and next steps

### Quick Links
| Document | Purpose |
|----------|---------|
| [ECOSYSTEM.md](docs/ECOSYSTEM.md) | All repos, architecture diagram, data flow |
| [ROADMAP.md](docs/ROADMAP.md) | Phases, priorities, what to work on next |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute to any LDT project |
| [MAINTENANCE_SCHEDULE.md](MAINTENANCE_SCHEDULE.md) | Update schedules for all tools |

### All LDT Repositories
- **ldt-data** (this repo) - Central data & documentation hub
- **ldt-web** - Landing page (latterdaytools.io)
- **ldt-prophet** - Apostle succession calculator
- **ldt-temples** - Temple construction tracker
- **ldt-conference** - Conference analytics web UI
- **conference-analysis** - Python NLP toolkit
- **ldt-ui** - Shared UI components
- **bishop-toolkit** - Bishop admin automation

---

## ⚠️ MANDATORY PRACTICES

**READ FIRST**: Before starting any work, read `.claude/BEST_PRACTICES.md` for comprehensive development guidelines.

**You MUST:**
1. ✅ Create feature branches for all non-trivial work (NEVER commit directly to main)
2. ✅ Create GitHub issues before starting features
3. ✅ Use plan mode for features requiring 3+ file changes
4. ✅ Follow conventional commit format
5. ✅ Write tests for new features
6. ✅ Update documentation for user-facing changes
7. ✅ NEVER commit raw conference talk data (use .gitignore)

**Branch naming**: `<type>/<issue-number>-<brief-description>`
**Commit format**: `<type>(<scope>): <subject>` (see BEST_PRACTICES.md)

---

## Project Overview

**ldt-data** is the **central data repository** for the LatterDay Tools ecosystem. Similar to `rankview-data`, this repo serves as a **shared database** that all LDT projects read from, eliminating duplicate data scraping and ensuring consistency.

**Architecture Pattern**: Database-centric
- All LDT components share data from this repository
- Single source of truth for conference talks, gospel data, and metadata
- Other repos READ from here, this repo WRITES data

**Primary Data**: General Conference talks (1971-present)
- Raw talk text and metadata
- NLP embeddings (semantic search)
- Citation graphs
- Topic models
- Speaker metadata

---

## Key Commands

### Initial Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Data Management

```bash
# Scrape latest conference talks (updates data/raw/)
python scripts/scrape_latest.py

# Generate embeddings (updates data/embeddings/)
python scripts/generate_embeddings.py

# Extract citations (updates data/citations/)
python scripts/extract_citations.py

# Export for web (updates data/public/)
python scripts/export_public.py
```

### Testing

```bash
# Run all tests
pytest

# Test data integrity
pytest tests/test_data_integrity.py

# Test scraper
pytest tests/test_scraper.py
```

### Code Quality

```bash
# Format code
black src/ tests/ scripts/

# Lint
flake8 src/ tests/ scripts/

# Type check
mypy src/
```

---

## Architecture

### Database-Centric Design

This repository is the **single source of truth** for all LDT projects:

```
ldt-data/                    # Central database (THIS REPO)
    ├── data/
    │   ├── raw/talks/       # Conference talk text (gitignored)
    │   ├── embeddings/      # NLP embeddings (gitignored)
    │   ├── citations/       # Citation graphs (gitignored)
    │   ├── metadata/        # Talk metadata (version controlled)
    │   └── public/          # Exported data for web (version controlled)
    └── src/
        └── ldt_data/        # Data access utilities

                    ↓ READ FROM ↓

ldt-conference/              # Conference analysis tools
ldt-prophet/                 # Apostle succession calculator
ldt-web/                     # Public website
ldt-bishop/                  # Bishop tools
```

### Data Flow

```
Web Scraping → data/raw/
     ↓
Processing → data/embeddings/, data/citations/
     ↓
Export → data/public/
     ↓
Other LDT Projects READ from data/public/
```

### Key Components

1. **Scrapers** (`src/ldt_data/scrapers/`):
   - Church website scraper
   - LCR API wrapper
   - Metadata extraction

2. **Processors** (`src/ldt_data/processors/`):
   - NLP embedding generation
   - Citation extraction
   - Topic modeling
   - Data validation

3. **Exporters** (`src/ldt_data/exporters/`):
   - JSON exports for web
   - CSV exports for analysis
   - Lightweight summaries

4. **Utilities** (`src/ldt_data/utils/`):
   - Data loading helpers
   - Cache management
   - Version tracking

### Important Files

- `data/metadata/talks.json` - Master talk index (version controlled)
- `data/metadata/speakers.json` - Speaker metadata
- `data/public/` - Exported data for consumption by other projects
- `scripts/scrape_latest.py` - Incremental update script
- `scripts/export_public.py` - Export for web deployment

---

## Data Organization

### Directory Structure

```
data/
├── raw/                          # Raw scraped data (gitignored)
│   ├── talks/                    # Conference talk text
│   │   ├── 2024-10/              # By conference date
│   │   │   ├── nelson_opening.json
│   │   │   ├── oaks_saturday.json
│   │   │   └── ...
│   │   └── ...
│   └── lcr/                      # LCR data (private)
│
├── embeddings/                   # NLP embeddings (gitignored)
│   ├── talks_embeddings.pkl      # Sentence transformer embeddings
│   └── metadata.json             # Embedding configuration
│
├── citations/                    # Citation graphs (gitignored)
│   ├── scripture_citations.json
│   └── talk_citations.json
│
├── metadata/                     # Version controlled metadata
│   ├── talks.json                # Master talk index
│   ├── speakers.json             # Speaker information
│   ├── conferences.json          # Conference dates/themes
│   └── schema_version.json       # Data schema version
│
└── public/                       # Exported for web (version controlled)
    ├── talks_summary.json        # Lightweight talk index
    ├── latest_conference.json    # Most recent conference
    └── stats.json                # Overall statistics
```

### What Gets Committed

**YES - Version controlled**:
- `data/metadata/` - Talk index, speaker info, schema
- `data/public/` - Exported summaries for web
- All source code in `src/`
- Scripts in `scripts/`

**NO - Gitignored**:
- `data/raw/` - Raw talk text (too large, scraped on demand)
- `data/embeddings/` - Generated embeddings (regenerate as needed)
- `data/citations/` - Extracted citations (derived data)
- `.venv/` - Virtual environment

---

## Common Patterns

### Pattern 1: Adding New Conference Data

After each General Conference:

1. Run scraper: `python scripts/scrape_latest.py`
2. Verify data: `pytest tests/test_data_integrity.py`
3. Generate embeddings: `python scripts/generate_embeddings.py`
4. Extract citations: `python scripts/extract_citations.py`
5. Export public data: `python scripts/export_public.py`
6. Commit metadata updates: `git add data/metadata/ data/public/`

### Pattern 2: Reading Data from Other Projects

Other LDT projects should read from `data/public/`:

```python
# In ldt-conference, ldt-web, etc.
import json
from pathlib import Path

# Point to sibling ldt-data repo
data_dir = Path(__file__).parent.parent.parent / "ldt-data" / "data" / "public"
talks = json.loads((data_dir / "talks_summary.json").read_text())
```

### Pattern 3: Regenerating All Data

Start from scratch:

```bash
# Scrape all conferences (takes 30-60 min)
python scripts/scrape_all.py

# Process everything
python scripts/generate_embeddings.py
python scripts/extract_citations.py
python scripts/export_public.py
```

---

## Integration with Other LDT Projects

### Projects Using This Data

1. **ldt-conference** - Reads talks for NLP analysis
2. **ldt-web** - Displays latest conferences
3. **lds-flyer-generator** - Generates talk summaries
4. **talk-citations** - Citation network analysis
5. **gospel-topics** - Topic modeling

### Data Access Library

```python
# Utility library for consistent data access
from ldt_data import load_talks, load_metadata, search_talks

# Load all talks
talks = load_talks()

# Search semantically
results = search_talks("faith and doubt")

# Get metadata
speakers = load_metadata("speakers")
```

---

## Troubleshooting

### Common Issues

1. **Issue**: Scraper fails with 403/404 errors
   **Solution**: Church website structure may have changed. Check `src/ldt_data/scrapers/church_scraper.py` and update selectors.

2. **Issue**: Embeddings generation is slow
   **Solution**: Use GPU if available. Install `sentence-transformers[gpu]`. Cache embeddings in `data/embeddings/`.

3. **Issue**: Other projects can't find data
   **Solution**: Ensure `ldt-data` is in sibling directory to other LDT projects (all in `~/code/`).

4. **Issue**: Git repo size growing too large
   **Solution**: Verify `data/raw/` and `data/embeddings/` are gitignored. Only commit `data/metadata/` and `data/public/`.

---

## Development Workflow

### Multi-Repo Coordination

Since other LDT projects depend on this repo:

1. **Make breaking changes carefully** - Update schema version
2. **Test with dependent projects** - Verify ldt-conference, ldt-web still work
3. **Document schema changes** - Update `data/metadata/schema_version.json`
4. **Coordinate updates** - If schema changes, update dependent repos

### Updating Data

- **Incremental**: Run `scrape_latest.py` monthly after conferences
- **Full refresh**: Run `scrape_all.py` when schema changes
- **Always test**: Run pytest before committing metadata

---

**Last Updated**: 2025-12-05
**Project Type**: Python Data Repository
**Role**: Central database for LatterDay Tools ecosystem
**Pattern**: Database-centric (like rankview-data)
