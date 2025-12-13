# LatterDay Tools Ecosystem

This document provides a comprehensive overview of the LatterDay Tools ecosystem - a collection of data science projects for analyzing and visualizing data related to The Church of Jesus Christ of Latter-day Saints.

**Central Hub**: This repository (ldt-data) serves as the documentation and data hub for the entire ecosystem.

---

## Repository Overview

| Repository | Purpose | Tech Stack | Status | URL |
|------------|---------|------------|--------|-----|
| **ldt-data** | Central data & docs hub | Python | Active | - |
| **ldt-web** | Landing page/marketing | Next.js | Production | latterdaytools.io |
| **ldt-prophet** | Apostle succession calculator | R + Next.js | Production | prophet.latterdaytools.io |
| **ldt-temples** | Temple construction tracker | R + Next.js | Production | temples.latterdaytools.io |
| **ldt-conference** | Conference analytics web UI | Next.js | In Development | conference.latterdaytools.io |
| **conference-analysis** | NLP analysis toolkit | Python | Functional | CLI/Jupyter |
| **ldt-ui** | Shared UI components | Next.js | Active | npm package |
| **bishop-toolkit** | Bishop admin automation | Python | Production | CLI |

---

## Repository Details

### ldt-data (This Repo)
**Purpose**: Central data repository and documentation hub for the LDT ecosystem.

**Contains**:
- 4,890 General Conference talks (1971-2025)
- Ecosystem documentation and roadmap
- Data export scripts for web apps
- Shared data schemas

**Key Files**:
- `data/metadata/conference_talks.csv` - Talk index
- `data/public/*.json` - Web-ready exports
- `docs/` - Ecosystem documentation

---

### ldt-web
**Purpose**: Main landing page and marketing hub for LatterDay Tools.

**Features**:
- Project showcase with links to all tools
- About section and disclaimers
- Responsive design

**Tech**: Next.js 14, TypeScript, Tailwind CSS

---

### ldt-prophet
**Purpose**: Calculate apostle succession probabilities using Monte Carlo simulation.

**Features**:
- Monte Carlo simulation (100,000 runs)
- CDC mortality data + Weibull distribution fitting
- Interactive charts showing probabilities
- Daily automated updates via GitHub Actions

**Tech**: R Shiny (backend), Next.js (frontend), Recharts

**Data Flow**:
```
raw_data/apostles.csv → R simulation → derived_data/*.rds → JSON export → Next.js UI
```

---

### ldt-temples
**Purpose**: Visualize 150+ years of temple construction (1877-2025).

**Features**:
- Interactive Mapbox map with 382 temples
- Timeline animation (play through history)
- Status color-coding (Dedicated, Under Construction, etc.)
- Video/GIF exports of growth animation

**Tech**: R (data pipeline), Next.js + Mapbox GL (frontend)

**Data Flow**:
```
churchofjesuschristtemples.org → R scraping → RDS files → JSON → Mapbox visualization
```

---

### ldt-conference
**Purpose**: Web interface for General Conference talk analytics.

**Current Features**:
- Basic statistics dashboard
- Top speakers ranking
- Decade distribution
- Recent talks with links

**Planned Features** (see ROADMAP.md):
- Semantic search using embeddings
- Topic modeling visualization
- Trend analysis charts

**Tech**: Next.js 14, TypeScript, Tailwind CSS

**Data Source**: Consumes JSON from ldt-data/data/public/

---

### conference-analysis
**Purpose**: Python NLP toolkit for deep analysis of conference talks.

**Features**:
- Web scraping from churchofjesuschrist.org
- Sentence embeddings (sentence-transformers)
- Temporal word/phrase frequency analysis
- Trend discovery (increasing/decreasing terms)
- Topic clustering
- Interactive Plotly visualizations

**Tech**: Python, sentence-transformers, pandas, plotly

**Relationship to ldt-conference**: This is the analysis engine; ldt-conference is the web UI. Future work will connect them.

---

### ldt-ui
**Purpose**: Shared React component library for consistent UI across LDT apps.

**Components**:
- **UI**: Button, Card, Badge, Loading
- **Layout**: SiteHeader, SiteFooter, AppLayout

**Usage**:
```typescript
import { Button, AppLayout } from 'ldt-ui'
```

**Tech**: Next.js, React 18, TypeScript, Tailwind CSS

---

### bishop-toolkit
**Purpose**: Automation tools for LDS bishop administrative tasks.

**Tools**:
1. **Agenda Management** (Production)
   - Create/update bishopric meeting agendas
   - Google Docs integration
   - Prayer assignments, ward needs tracking

2. **Calling Tracker** (Demo Phase)
   - Mobile-friendly form for status updates
   - Google Sheets backend
   - Automated workflow tracking

**Tech**: Python, Google APIs (Docs, Sheets, Forms)

---

## Architecture Diagram

```
                    ┌─────────────────────────────────────┐
                    │           ldt-data                  │
                    │   (Central Data & Documentation)    │
                    │                                     │
                    │  - Conference talks (4,890)         │
                    │  - Ecosystem docs & roadmap         │
                    │  - JSON exports for web             │
                    └─────────────────┬───────────────────┘
                                      │
           ┌──────────────────────────┼──────────────────────────┐
           │                          │                          │
           ▼                          ▼                          ▼
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   ldt-conference    │    │     ldt-prophet     │    │    ldt-temples      │
│   (Conference UI)   │    │  (Prophet Calc)     │    │  (Temple Tracker)   │
│                     │    │                     │    │                     │
│  Consumes:          │    │  Self-contained:    │    │  Self-contained:    │
│  - talks_by_year    │    │  - apostles.csv     │    │  - Scrapes temples  │
│  - top_speakers     │    │  - CDC mortality    │    │  - Generates maps   │
│  - conference_stats │    │  - Monte Carlo      │    │  - Video exports    │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
           │
           │ (Future: will consume)
           ▼
┌─────────────────────┐
│ conference-analysis │
│   (NLP Engine)      │
│                     │
│  - Embeddings       │
│  - Trend analysis   │
│  - Topic modeling   │
└─────────────────────┘

┌─────────────────────┐    ┌─────────────────────┐
│       ldt-ui        │    │   bishop-toolkit    │
│ (Shared Components) │    │ (Admin Automation)  │
│                     │    │                     │
│  Used by:           │    │  Standalone tool    │
│  - ldt-web          │    │  - Google Docs      │
│  - ldt-conference   │    │  - Google Sheets    │
│  - ldt-temples      │    │  - Calling tracker  │
└─────────────────────┘    └─────────────────────┘

┌─────────────────────┐
│       ldt-web       │
│   (Landing Page)    │
│                     │
│  Links to all tools │
│  latterdaytools.io  │
└─────────────────────┘
```

---

## Data Flow Summary

### Conference Data
```
churchofjesuschrist.org
    ↓ (scraped by conference-analysis)
conference-analysis/data/raw/talks.csv
    ↓ (copied to ldt-data)
ldt-data/data/metadata/conference_talks.csv
    ↓ (exported to JSON)
ldt-data/data/public/*.json
    ↓ (consumed by)
ldt-conference/public/data/*.json
```

### Temple Data
```
churchofjesuschristtemples.org
    ↓ (scraped by ldt-temples R scripts)
ldt-temples/derived_data/*.rds
    ↓ (converted to JSON)
ldt-temples/temple-web/public/data/temples.json
```

### Apostle Data
```
ldt-prophet/raw_data/apostles.csv (manually maintained)
    ↓ (R simulation)
ldt-prophet/derived_data/*.rds
    ↓ (exported)
ldt-prophet/web/public/apostles.json
```

---

## Development Standards

All repositories follow these standards:

1. **CLAUDE.md** - AI assistant instructions (links to this central docs)
2. **Conventional Commits** - `type(scope): description`
3. **Feature Branches** - Never commit directly to main
4. **TypeScript/Type Hints** - Strong typing in all code
5. **Tailwind CSS** - Consistent styling across web apps

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

---

## Getting Started

### Clone All Repos
```bash
gh repo clone cnoyes/ldt-data
gh repo clone cnoyes/ldt-web
gh repo clone cnoyes/ldt-prophet
gh repo clone cnoyes/ldt-temples
gh repo clone cnoyes/ldt-conference
gh repo clone cnoyes/conference-analysis
gh repo clone cnoyes/ldt-ui
gh repo clone cnoyes/bishop-toolkit
```

### Quick Links
- **Live Site**: https://latterdaytools.io
- **Prophet Calculator**: https://prophet.latterdaytools.io
- **Temple Tracker**: https://temples.latterdaytools.io
- **GitHub**: https://github.com/cnoyes

---

## Related Documents

- [ROADMAP.md](./ROADMAP.md) - Development phases and priorities
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Technical architecture details
- [../CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute
- [../MAINTENANCE_SCHEDULE.md](../MAINTENANCE_SCHEDULE.md) - Update schedules
