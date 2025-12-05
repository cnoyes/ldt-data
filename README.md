# ldt-data

**Central data repository for the LatterDay Tools ecosystem**

---

## Overview

`ldt-data` is the **single source of truth** for all LatterDay Tools projects, following a database-centric architecture pattern (similar to `rankview-data`). All LDT components read from this shared repository, eliminating duplicate data scraping and ensuring consistency across the ecosystem.

## What's Stored Here

### Primary Data
- **General Conference Talks** (1971-present)
  - Raw talk text and metadata
  - NLP embeddings for semantic search
  - Citation graphs (scripture + talk references)
  - Speaker information
  - Topic models

### Future Data
- Temple information and schedules
- Leadership metadata
- Gospel topics indices

## Architecture Pattern

```
ldt-data/          ←  WRITES data (scraping, processing)
    ↓
    └─ data/public/    ←  Other projects READ from here
            ↓
    ┌───────┴──────┬──────────┬───────────┐
    ↓              ↓          ↓           ↓
ldt-conference  ldt-web  ldt-prophet  ldt-bishop
```

**Key Principle**: This repo manages data collection and processing. Other repos consume the data.

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/cnoyes/ldt-data.git
cd ldt-data

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Initial Data Setup

**✅ Current Status**: Conference talk data already populated (4,890 talks, 1971-2025)

```bash
# Generate metadata for version control
python scripts/generate_metadata.py

# Export public data for web consumption
python scripts/export_for_web.py
```

**Available data**:
- `data/raw/conference_talks.csv` - All talk text (48MB, gitignored)
- `data/embeddings/conference_talks_embeddings.pkl` - Semantic embeddings (7.2MB, gitignored)
- `data/metadata/conference_talks.csv` - Talk index without full text (868KB, version controlled)
- `data/public/*.json` - Exported stats for web apps (version controlled)

### Monthly Updates (After General Conference)

```bash
# Scrape only latest conference (1-2 min)
python scripts/scrape_latest.py

# Process new data
python scripts/generate_embeddings.py
python scripts/extract_citations.py
python scripts/export_public.py

# Commit metadata updates
git add data/metadata/ data/public/
git commit -m "feat(data): add October 2024 general conference"
git push
```

## Project Structure

```
ldt-data/
├── data/
│   ├── raw/              # Raw scraped data (gitignored)
│   │   └── talks/        # Conference talk text by date
│   ├── embeddings/       # NLP embeddings (gitignored)
│   ├── citations/        # Citation graphs (gitignored)
│   ├── metadata/         # Talk index, speakers (VERSION CONTROLLED)
│   └── public/           # Exported for web (VERSION CONTROLLED)
│
├── src/ldt_data/
│   ├── scrapers/         # Web scrapers
│   ├── processors/       # NLP, citations, validation
│   ├── exporters/        # JSON/CSV export utilities
│   └── utils/            # Data loading, caching
│
├── scripts/              # Automation scripts
│   ├── scrape_all.py
│   ├── scrape_latest.py
│   ├── generate_embeddings.py
│   ├── extract_citations.py
│   └── export_public.py
│
└── tests/                # Data integrity tests
    ├── test_scraper.py
    ├── test_data_integrity.py
    └── test_exporters.py
```

## Data Organization

### What Gets Committed (Small Files)
✅ `data/metadata/` - Talk index, speaker info, schema (~MB)
✅ `data/public/` - Exported summaries for web (~MB)
✅ All source code and scripts

### What's Gitignored (Large Files)
❌ `data/raw/` - Raw talk text (regenerate via scraping)
❌ `data/embeddings/` - NLP embeddings (regenerate as needed)
❌ `data/citations/` - Citation graphs (derived data)

## Usage from Other Projects

### Reading Data (Other LDT Projects)

```python
# In ldt-conference, ldt-web, etc.
import json
from pathlib import Path

# Point to sibling ldt-data repo
data_dir = Path(__file__).parent.parent.parent / "ldt-data" / "data" / "public"

# Load talk summaries
talks = json.loads((data_dir / "talks_summary.json").read_text())

# Load latest conference
latest = json.loads((data_dir / "latest_conference.json").read_text())
```

### Using the Data Access Library

```python
from ldt_data import load_talks, load_metadata, search_talks

# Load all talks
talks = load_talks()

# Semantic search
results = search_talks("faith and doubt")

# Get speaker metadata
speakers = load_metadata("speakers")
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Test data integrity
pytest tests/test_data_integrity.py

# Test with coverage
pytest --cov=src/ldt_data
```

### Code Quality

```bash
# Format code
black src/ tests/ scripts/

# Lint
flake8 src/ tests/ scripts/

# Type checking
mypy src/
```

## Projects Using This Data

1. **ldt-conference** - Conference talk analysis, trends, topics
2. **ldt-web** - Public website at latterdaytools.io
3. **ldt-prophet** - Apostle succession probability calculator
4. **lds-flyer-generator** - Talk summary PDF generation
5. **talk-citations** - Citation network analysis
6. **gospel-topics** - Topic modeling over time

## Data Schema

### talks.json
```json
{
  "talks": [
    {
      "id": "2024-10-nelson-opening",
      "title": "Opening Remarks",
      "speaker": "Russell M. Nelson",
      "date": "2024-10-05",
      "session": "Saturday Morning",
      "url": "https://...",
      "conference": "2024-10"
    }
  ]
}
```

### speakers.json
```json
{
  "speakers": [
    {
      "name": "Russell M. Nelson",
      "role": "President",
      "ordained": "1984-04-07",
      "first_talk": "1984-10"
    }
  ]
}
```

## Performance

- **First scrape**: 30-60 minutes (all conferences since 1971)
- **Incremental update**: 1-2 minutes (latest conference only)
- **Embedding generation**: 5-10 minutes (cached after first run)
- **Semantic search**: Nearly instant (using cached embeddings)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

MIT

---

**Part of the LatterDay Tools ecosystem** | [latterdaytools.io](https://latterdaytools.io)
