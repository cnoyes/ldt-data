# LatterDay Tools Development Roadmap

This document outlines the development phases, priorities, and next steps for the LatterDay Tools ecosystem.

**Last Updated**: February 2026

---

## Current Status Summary

| Component | Status | Notes |
|-----------|--------|-------|
| ldt-prophet | Production | Daily automated updates |
| ldt-temples | Production | Web app + video generation working |
| ldt-web | Production | Landing page live |
| ldt-conference | Basic | Stats dashboard only |
| conference-analysis | Functional | NLP toolkit ready |
| ldt-ui | Active | 7 components built |
| ldt-data | Active | 4,890 talks indexed |
| bishop-toolkit | Production | Agenda tool working |

---

## Phase 1: Foundation (COMPLETED)

### Completed Tasks
- [x] Set up all repositories with proper structure
- [x] Deploy ldt-prophet with Monte Carlo simulation
- [x] Deploy ldt-temples with interactive map
- [x] Create ldt-web landing page
- [x] Build ldt-ui component library (7 components)
- [x] Index 4,890 conference talks in ldt-data
- [x] Complete bishop-toolkit agenda management tool
- [x] Fix hard-coded paths in ldt-temples
- [x] Consolidate landing pages into ldt-web
- [x] Create central ecosystem documentation

---

## Phase 2: Integration (CURRENT PRIORITY)

### 2.1 Connect conference-analysis to ldt-conference
**Priority**: HIGH
**Effort**: Medium (1-2 weeks)

**Goal**: Make the NLP capabilities from conference-analysis available in the ldt-conference web UI.

**Tasks**:
- [ ] Export embeddings from conference-analysis to ldt-data
- [ ] Create semantic search API in ldt-conference
- [ ] Build search UI component
- [ ] Add topic clustering visualization
- [ ] Implement trend analysis charts

**Files to Modify**:
- `conference-analysis/scripts/export_embeddings.py` (create)
- `ldt-data/data/embeddings/` (new directory)
- `ldt-conference/src/app/api/search/route.ts` (create)
- `ldt-conference/src/components/Search.tsx` (create)

### 2.2 Centralize Data in ldt-data
**Priority**: MEDIUM
**Effort**: Medium (1 week)

**Goal**: Make ldt-data the true single source of truth.

**Tasks**:
- [ ] Move temple data schema to ldt-data
- [ ] Create shared data access patterns
- [ ] Document data update workflows
- [ ] Set up automated data sync

### 2.3 Integrate ldt-ui Across Projects
**Priority**: LOW
**Effort**: Low (1-2 days)

**Goal**: Have all web projects consume shared components from ldt-ui.

**Tasks**:
- [ ] Set up npm workspace or link
- [ ] Update ldt-web to use ldt-ui components
- [ ] Update ldt-conference to use ldt-ui components
- [ ] Update ldt-temples/temple-web to use ldt-ui components

---

## Phase 3: Feature Development

### 3.1 ldt-conference NLP Features
**Priority**: HIGH (after Phase 2.1)

**Features to Add**:
- [ ] Semantic search ("find talks about faith during trials")
- [ ] Topic modeling visualization (what topics dominate each decade)
- [ ] Speaker analysis (how has speaker X's language evolved)
- [ ] Citation network (which talks reference which scriptures)
- [ ] Trend discovery (what words are increasing/decreasing)

### 3.2 ldt-temples Enhancements
**Priority**: LOW

**Features to Add**:
- [ ] Temple search by name/location
- [ ] Regional zoom presets
- [ ] Comparison views (growth by region)
- [ ] Temple detail pages

### 3.3 Bishop Toolkit - Calling Tracker
**Priority**: MEDIUM

**Tasks**:
- [ ] Test calling tracker with real bishopric workflow
- [ ] Refine form fields based on feedback
- [ ] Deploy for actual use
- [ ] Add reporting/analytics

---

## Phase 4: Automation & Infrastructure

### 4.1 Automated Data Pipelines
**Priority**: MEDIUM

**Tasks**:
- [ ] GitHub Actions for post-conference data updates (April/October)
- [ ] Automatic JSON export generation
- [ ] Slack/email notifications on data changes
- [ ] Health checks for all services

### 4.2 Testing Infrastructure
**Priority**: MEDIUM

**Tasks**:
- [ ] Add Jest tests to all Next.js projects
- [ ] Add pytest tests to all Python projects
- [ ] Set up CI/CD pipelines
- [ ] Aim for 80% coverage

### 4.3 Monitoring & Analytics
**Priority**: LOW

**Tasks**:
- [ ] Add error tracking (Sentry)
- [ ] Add analytics (Plausible/PostHog)
- [ ] Performance monitoring
- [ ] Uptime monitoring

---

## Phase 5: Polish & Growth

### 5.1 SEO & Marketing
- [ ] Add OpenGraph meta tags to all sites
- [ ] Create sitemap.xml files
- [ ] Write blog posts about the projects
- [ ] Social media presence

### 5.2 Documentation
- [ ] Video tutorials for each tool
- [ ] API documentation
- [ ] User guides

### 5.3 Community
- [ ] Open source contribution guidelines
- [ ] Issue templates
- [ ] Feature request process

---

## Decision Log

### December 2024
- **Decision**: Use ldt-data as central documentation hub
- **Rationale**: Already positioned as data hub, natural extension

- **Decision**: Keep ldt-web's clean, simple design as the main landing page
- **Rationale**: User preference for cleaner look

- **Decision**: Build out ldt-ui rather than remove it
- **Rationale**: Consistency across projects worth the investment

---

## Backlog (Unscheduled)

These items are good ideas but not currently prioritized:

- [ ] Mobile apps (React Native)
- [ ] User accounts and saved searches
- [ ] API for third-party developers
- [ ] Multilingual support
- [ ] PDF export of conference talks
- [ ] Talk audio integration
- [ ] Machine learning predictions (next prophet, temple announcements)

---

## How to Contribute

1. Pick an item from Phase 2 or 3
2. Create a GitHub issue in the relevant repo
3. Reference this roadmap in your issue
4. Create a feature branch
5. Submit a PR with tests

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

---

## Contact

- **Repository Owner**: @cnoyes
- **GitHub**: https://github.com/cnoyes
