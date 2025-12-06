# Session Notes - December 6, 2025

## Summary
Fixed failing GitHub Actions workflows and completed Phase 1 of automation setup for LatterDay Tools ecosystem.

---

## Accomplishments

### 1. Prophet Calculator Automation - ✅ OPERATIONAL

**Problems Resolved:**
- ❌ R package installation failures (tidyverse too large)
- ❌ MASS package incompatible with R 4.3
- ❌ Disk space errors during package compilation
- ❌ Git push permission denied (403)
- ❌ Slow workflow execution (6-11 minutes)

**Solutions Implemented:**
- Replaced `library('tidyverse')` with specific packages in 4 R scripts:
  - `src/1_load_apostles.R` → readr, tidyr, dplyr
  - `src/2_fit_death_curve.R` → MASS, ggplot2, dplyr
  - `src/3_calculate_prophet.R` → dplyr
  - `src/4_make_plots.R` → ggplot2, dplyr, scales
- Upgraded R from 4.3 to 4.4 (required for MASS package)
- Added disk cleanup (remove dotnet, ghc, boost) - frees ~10GB
- Added R package caching for faster subsequent runs
- Added `permissions: contents: write` to workflow
- Added `use-public-rspm: true` for faster binary package installation
- Added 10-minute timeout protection

**Results:**
- Workflow runtime: **2m39s** (down from 6-11 minutes)
- Automated commits working: ✅
- Daily updates at 6 AM UTC: ✅
- Last successful run: `cb69d09` (December 6, 2025)

### 2. Conference Analytics Workflow - ⏱️ CONFIGURED

**Fixes Applied:**
- Added 15-minute timeout protection
- Added `permissions: contents: write`
- Added `persist-credentials: true` for cross-repo commits
- Canceled runaway 50+ minute workflow

**Status:**
- Ready for testing during next conference season (April/October 2025)
- Will scrape new talks daily during first 2 weeks of conference months
- Auto-updates ldt-data and ldt-conference repos

### 3. Documentation Updates

**Updated Files:**
- `ldt-data/AUTOMATION_SETUP.md` - Added Phase 1 completion status
- Created `ldt-data/SESSION_NOTES_2025-12-06.md` - This file
- `ldt-prophet/.gitignore` - Added test file exclusions

---

## Repository Changes

### ldt-prophet (6 commits)
```
e88c2ab - chore: update navigation and gitignore
cb69d09 - chore: update apostle succession probabilities (daily recalculation) [automated]
cf3a757 - fix: add disk cleanup, package caching, and write permissions
6fa07e3 - fix: add 10-minute timeout to prevent runaway workflows
9823288 - fix: replace tidyverse with specific packages and update R to 4.4
050be2b - fix: install specific R packages instead of tidyverse meta-package
```

### ldt-conference (2 commits)
```
900cf1c - fix: add write permissions for automated commits
9d08573 - fix: add 15-minute timeout to prevent runaway workflows
```

### ldt-data (1 commit)
```
f84ec0b - docs: update automation status - Phase 1 complete
```

### conference-analysis (3 commits)
```
be80ccf - fix: use minimal requirements to avoid disk space issues
a4f86ee - feat: add minimal requirements for CI/CD scraping
88bafcc - fix: remove invalid sqlite3-python package from requirements
```

---

## Architecture Plan Created

**File:** `/Users/claynoyes/.claude/plans/async-wobbling-owl.md`

**Key Decisions:**
- Platform: Google Cloud Platform (GCP) over AWS
  - Reason: Skills transferable to day job
  - Cost: ~50% cheaper ($2-3/month vs $5/month)
- Architecture: Hybrid GitHub Actions + Cloud Run Jobs + Vertex AI
- Timeline: 12 weeks to full production
- Budget: $2-3/month now, $7-8/month at 3x scale

**Phases:**
1. ✅ Fix GitHub Actions (Week 1) - **COMPLETE**
2. ⏳ Containerize Jobs (Weeks 2-3)
3. ⏳ GCP Infrastructure Setup (Week 4)
4. ⏳ Migrate ldt-prophet to Cloud Run (Week 5)
5. ⏳ Migrate remaining jobs (Weeks 6-8)
6. ⏳ Add GenAI capabilities (Weeks 9-12)

---

## Key Technical Learnings

1. **tidyverse is a meta-package** - Installing it pulls 100+ dependencies
   - Solution: Use specific packages (dplyr, tidyr, readr, ggplot2)

2. **GitHub Actions disk space** - Runners have limited disk (~14GB free)
   - Solution: Clean up dotnet, ghc, boost before heavy operations

3. **R package versions** - MASS requires R >= 4.4.0
   - Solution: Upgrade R version in workflow

4. **GitHub Actions permissions** - Need explicit `permissions: contents: write`
   - Solution: Add to workflow YAML at top level

5. **Package caching** - Dramatically speeds up subsequent runs
   - Solution: Use `actions/cache@v3` with `R_LIBS_USER` path

---

## Next Steps

### Immediate (Optional)
- [ ] Configure Vercel deployment secrets in GitHub
  - VERCEL_TOKEN, VERCEL_ORG_ID, VERCEL_PROJECT_ID
  - Enables auto-deployment after data updates

### Phase 2+ (When Ready)
- [ ] Implement Temple Tracker scraper
- [ ] Containerize R/Python workloads
- [ ] Set up GCP Cloud Run Jobs
- [ ] Add GenAI features (conference summaries, embeddings)

---

## Testing Results

**Prophet Calculator Workflow:**
- ✅ R package installation (2m 0s)
- ✅ Monte Carlo simulation (100K iterations, 2s)
- ✅ Data derivation (apostles_with_prob.rds)
- ✅ Git commit and push
- ⏳ Vercel deployment (secrets not configured)

**Conference Analytics Workflow:**
- Not tested (no new conference talks available)
- Workflow will activate during April 1-14 and October 1-14

---

## Cost Analysis

**Current (GitHub Actions only):**
- Usage: ~100 minutes/month
- Cost: **$0** (well within 2,000 min/month free tier)

**Future (with GCP):**
- GitHub Actions (light jobs): $0
- Cloud Run Jobs (intensive): $2-3/month
- Vertex AI (GenAI): $0-5/month (usage-based)
- **Total: $2-8/month**

---

**Session Duration:** ~2 hours
**Status:** ✅ Phase 1 Complete - Automation operational
**Next Session:** Temple Tracker implementation or Phase 2 (containerization)
