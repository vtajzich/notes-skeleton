# March 2026
#work/wraps

## Month Summary
March was defined by three converging workstreams: the v2 API migration entering its final stretch, the search infrastructure decision, and the launch of onboarding v2. An API outage mid-month triggered process improvements around config deployment safety.

## Highlights
- v2 migration advanced from 9/15 to 11/15 clients, with auth adapter unblocking the remainder
- Search decision finalized: tuned Elasticsearch over Algolia, saving ~$800/month
- Onboarding v2 service registration flow reached staging
- Incident response improved: mandatory canary deployment for config changes

## Open Action Items

| Task | Owner | Due | Source |
|---|---|---|---|
| Productionize tuned ES search | Bob | 2026-04-01 | [W12](W12/2026-03-18.md) |
| Complete CI/CD template selection | Eve | 2026-04-07 | [W12](W12/2026-03-18.md) |
| Migrate next 2 legacy clients | Alice | 2026-03-25 | [W12](W12/2026-03-18.md) |
| Deliver onboarding v2 MVP | Eve | 2026-03-31 | [W11](W11/2026-03-11.md) |
| Implement canary for config changes | Dan | 2026-03-21 | [Incident debrief](../../team-a/meetings/adhoc/2026-03-14%20-%20Incident%20Debrief%20API%20Outage.md) |

## Major Themes

### v2 Migration — Final Stretch
Migration from v1 to v2 API progressed from 60% to 73%. Key blocker (undocumented legacy auth) was resolved with an adapter. Test automation coverage improved from 40% to 72%. On track for 2026-05-15 go-live.

### Search Infrastructure Decision
Bob delivered thorough benchmark (Algolia vs Elasticsearch). Team chose tuned ES after prototype hit 55ms p95 — competitive with Algolia at no additional vendor cost. Productionization underway.

### Onboarding v2
Eve kicked off implementation with service registration flow. Positive demo at weekly sync. CI/CD template selection is the next milestone.

### Reliability
API outage caused by config typo (rate limiter set to 100 instead of 1000). 45-minute impact. Led to mandatory canary deployment for config changes and pre-deploy validation checks.

## Decisions

| Date | Decision | Context |
|---|---|---|
| 2026-03-18 | Tuned Elasticsearch over Algolia | 55ms p95, no vendor cost, Bob to productionize |
| 2026-03-14 | Mandatory canary for config changes | Post-incident measure after rate limiter outage |

## Weekly Wrap Sources
- [W11](W11/week.md)
- [W12](W12/week.md)
