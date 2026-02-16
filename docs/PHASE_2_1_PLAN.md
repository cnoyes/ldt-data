# Phase 2.1: Connect conference-analysis NLP to ldt-conference

## Context

The ldt-conference web app currently shows a static stats dashboard (talks by decade, top speakers, recent talks) with a "Coming Soon" placeholder for NLP features. The conference-analysis Python repo has full NLP capabilities (embeddings, temporal analysis, trend discovery) but isn't connected to the web UI. This plan bridges them: pre-compute NLP results in Python, export as JSON, and build the web UI to display and search them.

## Architecture

```
conference-analysis (Python)     ldt-data (storage)       ldt-conference (Next.js)
  scrape talks                ->  metadata CSV          ->  static JSON (stats)
  generate OpenAI embeddings  ->  embeddings JSON       ->  API route (search)
  compute trends/clusters     ->  analysis JSON         ->  visualization components
```

- **Heavy NLP**: offline in Python scripts
- **Runtime**: only 1 OpenAI API call per search query (encode query -> cosine similarity against pre-computed embeddings)
- **Embedding model**: OpenAI `text-embedding-3-small` at 512 dimensions (~$0.22 one-time cost for all 4,890 talks)

## Prerequisites

Raw talk text doesn't exist locally (gitignored). Before any NLP work:
```bash
cd conference-analysis
pip install -r requirements.txt
python -m conference_analysis.scraper  # ~30-60 min first time
```

---

## Step 1: Create embedding export script

- [ ] **Repo**: `conference-analysis`
- [ ] **New file**: `scripts/export_embeddings_openai.py`

Script that:
1. Reads scraped talks from `data/raw/talks.csv`
2. Calls OpenAI `text-embedding-3-small` (512 dims) to embed each talk (title + first 8000 chars of text)
3. Batches requests (100 at a time) with rate limiting
4. Exports to `../ldt-data/data/embeddings/`:
   - `talk_embeddings.json` (~20 MB) -- model info + flat array of embeddings
   - `talk_metadata.json` -- parallel array of {title, speaker, date, conference, href}

- [ ] **Also modify**: `requirements.txt` -- add `openai>=1.0.0`

## Step 2: Create pre-computed analysis export script

- [ ] **Repo**: `conference-analysis`
- [ ] **New file**: `scripts/export_analysis.py`

Script that generates static JSON for visualizations (no runtime computation needed):

1. **`word_trends.json`** -- word frequency over decades for curated word sets (e.g., "Core Gospel": faith, repentance, baptism; "Christ-centered": Jesus Christ, Savior, Redeemer)
2. **`trend_changes.json`** -- top 25 increasing + 25 decreasing words comparing 1971-1989 vs 2010-2025
3. **`topic_clusters.json`** -- K-Means clusters (k=12) from OpenAI embeddings, with representative talks and top speakers per cluster

Output goes to `../ldt-data/data/public/`

## Step 3: Run the data pipeline

- [ ] Run scraper, embedding generation, and analysis export

```bash
# 1. Scrape (if not already done)
cd conference-analysis
python -m conference_analysis.scraper

# 2. Generate embeddings (~5 min, ~$0.22)
OPENAI_API_KEY=sk-... python scripts/export_embeddings_openai.py

# 3. Generate analysis JSONs
python scripts/export_analysis.py
```

## Step 4: Copy data to ldt-conference

- [ ] Copy `ldt-data/data/public/{word_trends,trend_changes,topic_clusters}.json` -> `public/data/`
- [ ] Copy `ldt-data/data/embeddings/{talk_embeddings,talk_metadata}.json` -> `data/embeddings/` (new root-level dir, for server-side only)
- [ ] Add `data/embeddings/` to `.gitignore` (too large for git; for Vercel, address separately)
- [ ] **New file**: `scripts/sync-data.sh` -- automates the copy from sibling ldt-data repo

## Step 5: Semantic search API route

- [ ] **Repo**: `ldt-conference`
- [ ] **New file**: `src/app/api/search/route.ts`
- [ ] **New dep**: `openai` package

API route that:
1. Loads pre-computed embeddings from `data/embeddings/` (cached in memory after first load)
2. Takes query param `q` (search text), optional `limit`, `yearMin`, `yearMax`
3. Calls OpenAI to encode the query into a 512-dim vector
4. Computes cosine similarity against all 4,890 talk embeddings
5. Returns top-K results with title, speaker, date, href, similarity score

**Env var needed**: `OPENAI_API_KEY` (server-side only, set in Vercel project settings + `.env.local`)

## Step 6: Build UI components

**Repo**: `ldt-conference`

- [ ] `src/components/SemanticSearch.tsx` (client component)
  - Search input with submit button
  - Optional year range filters
  - Loading state
  - Results list: title, speaker, date, similarity bar, link to churchofjesuschrist.org
  - Example query suggestions ("faith during trials", "covenant path", "ministering")

- [ ] `src/components/TrendChanges.tsx` (client component)
  - Horizontal bar chart showing top increasing (green) and decreasing (red) words
  - Data from `/data/trend_changes.json` loaded via fetch

- [ ] `src/components/WordTrends.tsx` (client component)
  - Line chart showing word frequency over decades
  - Toggle between curated word sets
  - Uses `recharts` library (add as dependency)

- [ ] `src/components/TopicClusters.tsx` (client component)
  - Grid of cluster cards (label, size, top speakers, representative talks)
  - Expandable to see more talks per cluster

## Step 7: Update main page

- [ ] **Modify**: `src/app/page.tsx`

Replace the "Coming Soon" section with real components. New page order:
1. Hero + Stats Grid (existing)
2. **Semantic Search** (new, prominent)
3. Talks by Decade + Top Speakers grid (existing)
4. **Word Trends** (new, line chart)
5. **Trending Words** (new, bar charts)
6. **Topic Clusters** (new, card grid)
7. Recent Talks (existing)

- [ ] **Also modify**: `src/lib/data.ts` -- add loader functions for new JSON files
- [ ] **Also modify**: `src/types/index.ts` -- add TypeScript interfaces

---

## Files Summary

| Repo | File | Action |
|------|------|--------|
| conference-analysis | `scripts/export_embeddings_openai.py` | CREATE |
| conference-analysis | `scripts/export_analysis.py` | CREATE |
| conference-analysis | `requirements.txt` | MODIFY (add openai) |
| ldt-conference | `src/app/api/search/route.ts` | CREATE |
| ldt-conference | `src/components/SemanticSearch.tsx` | CREATE |
| ldt-conference | `src/components/WordTrends.tsx` | CREATE |
| ldt-conference | `src/components/TrendChanges.tsx` | CREATE |
| ldt-conference | `src/components/TopicClusters.tsx` | CREATE |
| ldt-conference | `scripts/sync-data.sh` | CREATE |
| ldt-conference | `src/app/page.tsx` | MODIFY |
| ldt-conference | `src/lib/data.ts` | MODIFY |
| ldt-conference | `src/types/index.ts` | MODIFY |
| ldt-conference | `package.json` | MODIFY (add openai, recharts) |
| ldt-conference | `.env.example` | MODIFY |
| ldt-conference | `.gitignore` | MODIFY |

## Verification

1. Run `npm run dev` in ldt-conference -- page loads with all new sections
2. Search "faith during trials" -- returns relevant talks with similarity scores
3. Word trends chart renders with decade-by-decade data
4. Trend changes shows increasing/decreasing words
5. Topic clusters display with representative talks
6. `npm run type-check` passes
7. `npm run lint` passes
