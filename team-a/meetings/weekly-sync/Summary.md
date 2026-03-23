# Weekly Sync — Summary
#work/team-a/meetings/weekly-sync

> Cadence: Tuesdays 10:00 | Last updated: 2026-03-18 | Meetings summarized: 3

## Hot Topics
- v2 API migration — auth adapter merged, 11 of 15 clients migrated, on track for 2026-05-15
- Portal search — team decided on tuned Elasticsearch (55ms p95), Bob productionizing
- Onboarding v2 — service registration flow complete in staging, CI/CD template selection next

## Open Action Items
- [ ] Productionize tuned ES search @Bob 📅 2026-04-01 ([2026-03-18](2026-03-18.md))
- [ ] Complete CI/CD template selection step @Eve 📅 2026-04-07 ([2026-03-18](2026-03-18.md))
- [ ] Migrate next 2 legacy clients @Alice 📅 2026-03-25 ([2026-03-18](2026-03-18.md))
- [ ] Deliver onboarding v2 MVP @Eve 📅 2026-03-31 ([2026-03-11](2026-03-11.md))
- [x] Complete auth flow investigation @Alice ([2026-03-04](2026-03-04.md))
- [x] Deliver search benchmark results @Bob ([2026-03-04](2026-03-04.md))
- [x] Complete auth adapter review and merge @Me ([2026-03-11](2026-03-11.md))
- [x] Prototype tuned Elasticsearch config @Bob ([2026-03-11](2026-03-11.md))

## Key Decisions

| Date | Decision | Context |
|---|---|---|
| 2026-03-18 | Proceed with tuned ES, skip Algolia | Bob's prototype hit 55ms p95 — good enough, avoids vendor cost |
| 2026-03-11 | Bob to prototype tuned ES before final search decision | Benchmark showed Algolia faster but expensive |

## Topic History

| Topic | First Raised | Last Discussed | Status |
|---|---|---|---|
| v2 migration | 2026-03-04 | 2026-03-18 | On track — 11/15 clients done |
| Search performance | 2026-03-04 | 2026-03-18 | Decided: tuned ES, productionizing |
| Onboarding v2 | 2026-03-04 | 2026-03-18 | In progress — registration flow in staging |
| Architecture review | 2026-03-18 | 2026-03-18 | Scheduled 2026-03-21 |

## Summarized Meetings
- 2026-03-18 ✓
- 2026-03-11 ✓
- 2026-03-04 ✓
