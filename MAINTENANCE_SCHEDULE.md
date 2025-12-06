# LatterDay Tools Maintenance Schedule

Complete guide for keeping all LDT tools updated with current data.

---

## Overview

| Tool | Update Frequency | Effort | Automatable? |
|------|-----------------|--------|--------------|
| **Conference Analytics** | 2x/year (Apr, Oct) | 25 min | ✅ Partially |
| **Prophet Calculator** | As needed (1-2x/year) | 10 min | ❌ Manual |
| **Temple Tracker** | Quarterly or as announced | 30 min | ⚠️ Partially |

---

## 1. Conference Analytics (ldt-conference)

### Update Schedule
- **April General Conference**: First weekend of April
- **October General Conference**: First weekend of October
- **Update timing**: 1-2 days after conference ends (when talks are published)

### Process
See detailed process in [`UPDATE_PROCESS.md`](UPDATE_PROCESS.md)

**Quick version:**
```bash
# 1. Scrape new talks
cd ~/code/conference-analysis
source .venv/bin/activate
python -c "from src.conference_analysis.scraper import ConferenceScraper; scraper = ConferenceScraper(cache_file='data/raw/talks.csv'); scraper.scrape_all(); scraper.save()"

# 2. Update ldt-data
cp ~/code/conference-analysis/data/raw/talks.csv ~/code/ldt-data/data/raw/conference_talks.csv
cd ~/code/ldt-data
python scripts/generate_metadata.py
python scripts/export_for_web.py
git add data/metadata/ data/public/
git commit -m "feat(data): add [Month Year] conference talks"
git push

# 3. Update web app
cd ~/code/ldt-conference
cp ~/code/ldt-data/data/public/*.json public/data/
git add public/data/
git commit -m "data: update with [Month Year] conference"
git push
vercel --prod
```

### Automation Potential
- ✅ Scraping can be automated
- ✅ Data processing is automated
- ⚠️ Deployment could be automated with GitHub Actions
- ❌ Still need to verify quality

### Next Updates
- April 2026 General Conference
- October 2026 General Conference

---

## 2. Prophet Calculator (ldt-prophet)

### Update Schedule
**Event-driven** - Update when changes occur in Church leadership:

1. **New Apostle Called** (uncommon, ~1-2x per decade)
   - Add to apostles.csv with birth date and ordination date

2. **Apostle Passes Away** (variable, ~1x per year)
   - Mark as deceased in apostles.csv

3. **First Presidency Reorganization** (when Prophet passes)
   - Update succession after new Prophet is sustained

### Data File
Location: `~/code/ldt-prophet/raw_data/apostles.csv`

**Format:**
```csv
Name,Birth Date,Ordained Apostle
Dallin H Oaks,1932-08-12,1984-04-07
Jeffrey R Holland,1940-12-03,1994-06-23
```

### Update Process

#### Adding a New Apostle
```bash
cd ~/code/ldt-prophet

# 1. Edit apostles.csv
# Add new row with: Name, Birth Date (YYYY-MM-DD), Ordination Date (YYYY-MM-DD)
nano raw_data/apostles.csv

# 2. Regenerate derived data
Rscript run_all.R

# 3. Test locally
# Open app.R in RStudio or run Shiny app

# 4. Update web version if needed
cd web
# (Rebuild and deploy if web version exists)

# 5. Commit
git add raw_data/apostles.csv derived_data/
git commit -m "data: add Elder [Name] to apostle succession"
git push
```

#### Recording a Passing
```bash
cd ~/code/ldt-prophet

# 1. Update apostles_all.csv (historical record)
# Add death date column if needed

# 2. Remove from apostles.csv (active apostles)
nano raw_data/apostles.csv
# Delete the row for the deceased apostle

# 3. Regenerate calculations
Rscript run_all.R

# 4. Commit
git add raw_data/
git commit -m "data: update apostle succession after passing of Elder [Name]"
git push
```

### Automation Potential
- ❌ Cannot automate (requires awareness of Church announcements)
- ⚠️ Could set up alerts for Church newsroom RSS feed
- ✅ Calculation pipeline is automated once data is updated

### Monitoring
- Follow Church newsroom: https://newsroom.churchofjesuschrist.org
- April & October General Conference (new apostles often called)
- Subscribe to Church News notifications

---

## 3. Temple Tracker (ldt-temples)

### Update Schedule
**Multiple trigger events:**

1. **New Temple Announcements** (~10-30 per year)
   - Usually during General Conference
   - Sometimes in other church meetings

2. **Groundbreaking** (construction begins)

3. **Dedication** (temple opens)

4. **Status Changes** (construction progress)

### Data Source
Primary: https://churchofjesuschrist.org/temples/list
Temple details: Individual temple pages

### Update Process

**Option A: Manual Update** (Current)
```bash
cd ~/code/ldt-temples/temple-web

# 1. Update public/data/temples.json
# Add new temples or update status
nano public/data/temples.json

# Format:
# {
#   "name": "City Name Temple",
#   "location": "City, State/Country",
#   "announced": "2024-04-01",
#   "groundbreaking": "2025-01-15",  # or null
#   "dedication": null,
#   "status": "announced" | "under-construction" | "completed",
#   "coordinates": [latitude, longitude]
# }

# 2. Rebuild
npm run build

# 3. Deploy
vercel --prod

# 4. Commit
git add public/data/temples.json
git commit -m "data: add [Temple Name] / update [Temple Name] status"
git push
```

**Option B: Scrape from Church Website** (Future)
```bash
# Create scraper in ldt-data
cd ~/code/ldt-data

# Run temple scraper
python scripts/scrape_temples.py

# This would:
# - Fetch temple list from churchofjesuschrist.org
# - Parse temple pages for status/dates
# - Generate temples.json
# - Export to ldt-data/data/public/temples.json
```

### Automation Potential
- ⚠️ Scraping possible but Church website structure may change
- ✅ Could set up quarterly cron job to check for updates
- ⚠️ Geocoding coordinates may require manual verification
- ✅ Deployment could be automated

### Monitoring
- Church newsroom: https://newsroom.churchofjesuschrist.org
- Temple page: https://churchofjesuschrist.org/temples/list
- General Conference announcements (April/October)

### Next Major Updates
- April 2026 General Conference (likely new temple announcements)
- October 2026 General Conference (likely new temple announcements)
- Ongoing: Groundbreakings and dedications throughout year

---

## Maintenance Calendar

### Quarterly Tasks (Every 3 months)

**January:**
- ✅ Check for temple status updates (construction/dedications from Oct-Dec)
- ✅ Verify all sites are running smoothly

**April:**
- 🔥 **Update Conference Analytics** (April General Conference)
- 🔥 **Check Prophet Calculator** (if new apostle called)
- 🔥 **Update Temple Tracker** (new temples often announced)

**July:**
- ✅ Check for temple status updates (construction/dedications from Apr-Jun)
- ✅ Review any Church leadership changes

**October:**
- 🔥 **Update Conference Analytics** (October General Conference)
- 🔥 **Check Prophet Calculator** (if new apostle called)
- 🔥 **Update Temple Tracker** (new temples often announced)

### As-Needed Tasks

**When Church announces:**
- New apostle → Update Prophet Calculator
- Apostle passing → Update Prophet Calculator
- New temple → Update Temple Tracker
- Temple dedication → Update Temple Tracker

---

## Future Automation Ideas

### GitHub Actions Workflows

**1. Conference Scraper** (Semi-automated)
```yaml
# .github/workflows/scrape-conference.yml
# Manually triggered after each General Conference
on: workflow_dispatch

jobs:
  scrape:
    - Run conference scraper
    - Generate metadata
    - Create PR with new data
    - Notify for review
```

**2. Temple Monitor** (Automated)
```yaml
# .github/workflows/monitor-temples.yml
# Runs monthly to check for temple updates
on: schedule (monthly)

jobs:
  check:
    - Scrape temple list
    - Compare with existing data
    - Create PR if changes detected
    - Notify for review
```

**3. Deployment** (Automated)
```yaml
# Auto-deploy on main branch push
on: push to main

jobs:
  deploy:
    - Build application
    - Run tests
    - Deploy to Vercel
```

### Monitoring Dashboard

Create a simple dashboard showing:
- ✅ Last update date for each tool
- ⚠️ Days since last conference (reminder to update)
- 📅 Next expected conference date
- 🏛️ Number of temples tracked
- 👔 Number of apostles tracked

---

## Quick Reference

### When to Update Each Tool

| Event | Conference | Prophet | Temples |
|-------|-----------|---------|---------|
| April Gen Conf | ✅ Update | ⚠️ Check | ⚠️ Check |
| October Gen Conf | ✅ Update | ⚠️ Check | ⚠️ Check |
| New Apostle Called | - | ✅ Update | - |
| Apostle Passes | - | ✅ Update | - |
| Temple Announced | - | - | ✅ Update |
| Temple Dedicated | - | - | ✅ Update |
| Quarterly Review | - | - | ✅ Update |

### Update Time Estimates

- **Conference Analytics**: 25 minutes (after each conference)
- **Prophet Calculator**: 10 minutes (when leadership changes)
- **Temple Tracker**: 5-10 minutes per temple update

**Total annual time commitment: ~2-3 hours/year**

---

## Emergency Contacts / Resources

- **Church Newsroom**: https://newsroom.churchofjesuschrist.org
- **Temples List**: https://churchofjesuschrist.org/temples/list
- **Conference Archive**: https://churchofjesuschrist.org/study/general-conference
- **Leadership Changes**: Usually announced during General Conference

---

Last updated: December 2025
Next review: April 2026
