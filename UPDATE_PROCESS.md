# Conference Data Update Process

This guide explains how to update the conference talk data after a new General Conference.

## Overview

After each General Conference (April and October), follow these steps to update the data:

1. **Scrape new talks** from churchofjesuschrist.org
2. **Generate metadata** for version control
3. **Export public JSON** files for web consumption
4. **Commit changes** to ldt-data
5. **Update ldt-conference** with new data
6. **Redeploy** to production

---

## Step-by-Step Process

### 1. Scrape New Conference Talks

The scraping code lives in the `conference-analysis` project. We'll use it to update the raw data.

```bash
cd ~/code/conference-analysis

# Activate virtual environment
source .venv/bin/activate

# Run the scraper (updates data/raw/talks.csv)
python -c "
from src.conference_analysis.scraper import ConferenceScraper
from datetime import date

scraper = ConferenceScraper(cache_file='data/raw/talks.csv')

# Scrape from the last known conference to today
# (it will only add new talks that don't exist)
scraper.scrape_all(start_date=date(2025, 10, 1))  # Adjust date as needed
scraper.save()
print(f'Total talks: {len(scraper.talks_df)}')
"
```

### 2. Copy Updated Data to ldt-data

```bash
# Copy the updated talks to ldt-data
cp ~/code/conference-analysis/data/raw/talks.csv ~/code/ldt-data/data/raw/conference_talks.csv
```

### 3. Generate Metadata

```bash
cd ~/code/ldt-data

# Generate metadata (version controlled)
python scripts/generate_metadata.py
```

**Output:**
- Updates `data/metadata/conference_talks.csv` with new talks
- Shows summary of date range, conferences, speakers, etc.

### 4. Export Public Data

```bash
# Generate JSON files for web consumption
python scripts/export_for_web.py
```

**Output:**
- `data/public/conference_stats.json`
- `data/public/talks_by_year.json`
- `data/public/top_speakers.json`
- `data/public/recent_talks.json`

### 5. Commit to ldt-data

```bash
# Review changes
git status
git diff data/metadata/
git diff data/public/

# Commit metadata and public exports
git add data/metadata/ data/public/
git commit -m "feat(data): add [Month] [Year] general conference

- Add [N] new talks from [Month] [Year] conference
- Update talk statistics and metadata
- Refresh public JSON exports

Total talks: [X,XXX]
Date range: 1971-04-01 to [YYYY-MM-DD]
"

# Push to GitHub
git push
```

### 6. Update ldt-conference

```bash
cd ~/code/ldt-conference

# Copy updated JSON files
cp ~/code/ldt-data/data/public/*.json public/data/

# Rebuild to verify
npm run build

# Commit
git add public/data/
git commit -m "data: update with [Month] [Year] conference talks"
git push

# Deploy to production
vercel --prod
```

The new data will be live at https://conference.latterdaytools.io

---

## Automated Script (Future)

For convenience, you can create a script that automates the entire process:

```bash
# Future: scripts/update_latest_conference.sh
#!/bin/bash
set -e

echo "📥 Scraping latest conference..."
cd ~/code/conference-analysis
source .venv/bin/activate
python scripts/scrape_latest.py

echo "📋 Copying to ldt-data..."
cp data/raw/talks.csv ~/code/ldt-data/data/raw/conference_talks.csv

echo "🔄 Generating metadata..."
cd ~/code/ldt-data
python scripts/generate_metadata.py
python scripts/export_for_web.py

echo "💾 Committing changes..."
git add data/metadata/ data/public/
git commit -m "feat(data): add latest conference talks"
git push

echo "🌐 Updating web app..."
cd ~/code/ldt-conference
cp ~/code/ldt-data/data/public/*.json public/data/
git add public/data/
git commit -m "data: update with latest conference"
git push
vercel --prod

echo "✅ Update complete!"
```

---

## Verification Checklist

After updating, verify:

- [ ] New talks appear in `data/metadata/conference_talks.csv`
- [ ] `conference_stats.json` shows updated total
- [ ] `recent_talks.json` includes talks from latest conference
- [ ] `talks_by_year.json` reflects new data
- [ ] ldt-conference builds successfully
- [ ] https://conference.latterdaytools.io shows new data

---

## Troubleshooting

### Scraper doesn't find new talks
- Verify the conference has been published on churchofjesuschrist.org
- Check the URL pattern matches: `/study/general-conference/YYYY/MM`
- Ensure the HTML structure hasn't changed (may need to update selectors)

### Metadata generation fails
- Check that `data/raw/conference_talks.csv` is valid CSV
- Verify all required columns exist: title, speaker, href, date, text

### Vercel deployment fails
- Ensure all JSON files are in `public/data/`
- Check build logs for file path issues
- Verify data.ts points to correct directory

---

## Data Sources

- **Primary**: churchofjesuschrist.org/study/general-conference
- **Scraper**: ~/code/conference-analysis/src/conference_analysis/scraper.py
- **Storage**: ~/code/ldt-data/data/

## Update Frequency

- **After each General Conference**: April and October
- **Time**: Usually available within 1-2 days after conference ends
- **Effort**: ~15 minutes per update (when scripted)

---

Last updated: December 2025
