# Automation Setup Guide

Complete guide for setting up automated daily updates for all LatterDay Tools.

---

## Overview

**Automated Workflows:**

| Tool | Frequency | Trigger | Action |
|------|-----------|---------|--------|
| **Prophet Calculator** | Daily | 6 AM UTC | Recalculate ages/probabilities |
| **Temple Tracker** | Daily | 7 AM UTC | Check for temple updates |
| **Conference Analytics** | Daily (Apr 1-14, Oct 1-14) | 8 AM UTC | Scrape new conference talks |

All workflows auto-commit and deploy if changes are detected.

---

## Setup Instructions

### 1. Configure GitHub Secrets

Each repository needs Vercel deployment tokens. Add these secrets in GitHub:

#### For ldt-prophet, ldt-temples, ldt-conference

Go to **Settings → Secrets and variables → Actions → New repository secret**

Add these three secrets:

**VERCEL_TOKEN**
```bash
# Get your Vercel token
vercel login
vercel whoami

# Create a token at: https://vercel.com/account/tokens
# Copy the token value
```

**VERCEL_ORG_ID**
```bash
# Get from .vercel/project.json in each project
cd ~/code/ldt-prophet/web  # or ldt-temples/temple-web, ldt-conference
cat .vercel/project.json | grep orgId
# Copy the value (e.g., "team_xxxxx")
```

**VERCEL_PROJECT_ID**
```bash
# Get from .vercel/project.json
cat .vercel/project.json | grep projectId
# Copy the value (e.g., "prj_xxxxx")
```

### 2. Enable GitHub Actions

For each repository (ldt-prophet, ldt-temples, ldt-conference):

1. Go to **Settings → Actions → General**
2. Under "Workflow permissions", select:
   - ✅ Read and write permissions
   - ✅ Allow GitHub Actions to create and approve pull requests
3. Click **Save**

### 3. Commit Workflows

```bash
# Prophet Calculator
cd ~/code/ldt-prophet
git add .github/workflows/daily-update.yml
git commit -m "ci: add daily automated age/probability updates"
git push

# Temple Tracker
cd ~/code/ldt-temples
git add .github/workflows/daily-update.yml
git commit -m "ci: add daily automated temple data checks"
git push

# Conference Analytics
cd ~/code/ldt-conference
git add .github/workflows/conference-check.yml
git commit -m "ci: add automated conference talk scraping"
git push
```

### 4. Test Workflows

Trigger manually to test:

1. Go to **Actions** tab in GitHub
2. Select the workflow (e.g., "Daily Prophet Calculator Update")
3. Click **Run workflow** → **Run workflow**
4. Watch the logs to verify it works

---

## How It Works

### Prophet Calculator (Daily)

```
6 AM UTC Daily
    ↓
Run R calculations with today's date
    ↓
Ages increment on birthdays → probabilities change
    ↓
If changed: Commit derived_data/ → Deploy to Vercel
```

**Why daily?**
- Apostle ages change on birthdays
- Probabilities recalculate based on current ages
- Ensures accuracy without manual updates

### Temple Tracker (Daily)

```
7 AM UTC Daily
    ↓
Scrape churchofjesuschrist.org/temples
    ↓
Compare with existing temple data
    ↓
If changed: Update temples.json → Deploy to Vercel
```

**Why daily?**
- Temple announcements can happen anytime
- Construction status updates frequently
- Groundbreakings and dedications occur year-round

### Conference Analytics (Seasonal)

```
8 AM UTC Daily (April 1-14, October 1-14 only)
    ↓
Scrape latest conference from Church website
    ↓
Check if new talks exist
    ↓
If new talks:
  1. Update ldt-data (metadata + exports)
  2. Update ldt-conference (JSON files)
  3. Deploy to Vercel
```

**Why first 2 weeks?**
- Talks usually published 1-2 days after conference ends
- Checking daily ensures we catch them immediately
- Only runs during conference months (April/October)
- Stops checking after 2 weeks (talks won't be added later)

---

## Monitoring

### Check Workflow Status

**GitHub Actions Dashboard:**
- https://github.com/cnoyes/ldt-prophet/actions
- https://github.com/cnoyes/ldt-temples/actions
- https://github.com/cnoyes/ldt-conference/actions

### Workflow Notifications

Configure email notifications:
1. Go to **Settings → Notifications** (your user settings)
2. Under "Actions", choose:
   - ✅ Send notifications for failed workflows
   - ⚠️ (Optional) Send notifications for successful workflows

### Verify Deployments

Check Vercel dashboard:
- https://vercel.com/dashboard

Each successful deployment will show:
- Deployment URL
- Build logs
- Status

---

## Workflow Files

**Location of automation configs:**

```
ldt-prophet/.github/workflows/daily-update.yml
ldt-temples/.github/workflows/daily-update.yml
ldt-conference/.github/workflows/conference-check.yml
```

---

## Customizing Schedules

Edit cron expressions in workflow files:

```yaml
schedule:
  - cron: '0 6 * * *'  # Daily at 6 AM UTC
```

**Cron format:** `minute hour day month weekday`

**Examples:**
```
'0 6 * * *'        # Daily at 6 AM UTC
'0 8 1-14 4,10 *'  # Daily 8 AM UTC, April 1-14 and Oct 1-14
'0 0 * * 0'        # Weekly on Sunday at midnight
'0 12 1 * *'       # Monthly on the 1st at noon
```

**Timezone note:** GitHub Actions uses UTC. Convert to your timezone:
- 6 AM UTC = 11 PM MST (previous day)
- 8 AM UTC = 1 AM MST

---

## Cost Estimate

### GitHub Actions (Free Tier)

- **Free**: 2,000 minutes/month for public repos
- **Usage estimate**:
  - Prophet: ~2 min/day × 30 = 60 min/month
  - Temples: ~3 min/day × 30 = 90 min/month
  - Conference: ~5 min/day × 14 = 70 min/month (seasonal)
  - **Total: ~220 min/month (well within free tier)**

### Vercel (Hobby Plan)

- **Free tier**: 100 GB bandwidth, 100 deployments/day
- **Usage estimate**:
  - ~60-90 deployments/month (only when changes detected)
  - Well within free tier limits

**Total cost: $0/month** ✅

---

## Troubleshooting

### Workflow fails with "Permission denied"

**Fix:** Enable write permissions in repository settings
- Settings → Actions → General → Workflow permissions
- Select "Read and write permissions"

### Vercel deployment fails

**Fix:** Check secrets are set correctly
```bash
# Verify secrets exist in GitHub:
# Settings → Secrets and variables → Actions

# Should have:
# - VERCEL_TOKEN
# - VERCEL_ORG_ID
# - VERCEL_PROJECT_ID
```

### Conference scraper finds no new talks

**Possible reasons:**
- Talks not published yet (wait 1-2 days after conference)
- Church website structure changed (update scraper)
- Already scraped (working as intended)

### Python dependencies fail to install

**Fix:** Update requirements.txt in conference-analysis
```bash
cd ~/code/conference-analysis
pip freeze > requirements.txt
git add requirements.txt
git commit -m "deps: update requirements for GitHub Actions"
git push
```

---

## Maintenance

### Update Workflow Files

If you need to modify workflows:

```bash
# Edit the workflow
cd ~/code/ldt-prophet
nano .github/workflows/daily-update.yml

# Commit changes
git add .github/workflows/
git commit -m "ci: update workflow schedule"
git push

# Test manually in GitHub Actions tab
```

### Pause Automation

**Disable a workflow:**
1. Go to **Actions** tab
2. Select the workflow
3. Click **⋯** → **Disable workflow**

**Re-enable later:**
1. Same location
2. Click **Enable workflow**

---

## Benefits of Automation

✅ **Always up to date**
- Prophet ages update daily (automatic on birthdays)
- Temple data refreshes daily (catch announcements immediately)
- Conference talks added within hours of publication

✅ **Zero manual effort**
- No need to remember to update
- No manual deployments
- Runs while you sleep

✅ **Reliable**
- Consistent schedule
- Automatic error recovery
- GitHub Actions infrastructure

✅ **Transparent**
- All changes logged in git history
- Workflow runs visible in Actions tab
- Failed runs trigger notifications

---

## Next Steps

1. ✅ Set up GitHub secrets for all three repos
2. ✅ Enable GitHub Actions permissions
3. ✅ Commit workflow files
4. ✅ Test each workflow manually
5. ✅ Monitor for first week to ensure stability
6. 🎉 Enjoy automatic updates!

---

**Last updated:** December 2025
**Status:** Ready for deployment
