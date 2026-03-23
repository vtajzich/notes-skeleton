# 2026-03-15 - v2 Migration Review
#work/team-a/product-x/meetings

## Meeting Summary
- Cross-team review of v2 API migration progress
- 9 of 15 clients migrated, auth adapter unblocks remaining 6
- Agreed on rollback strategy for go-live

## Key Discussion Points
### Migration Status
- 9 clients fully migrated and validated
- Auth adapter for legacy token format written and in review
- 6 remaining clients can proceed once adapter merges

### Rollback Strategy
- v1 endpoints stay live for 30 days post-migration
- Feature flag per client for instant rollback
- Monitoring: latency alerts at p95 > 200ms trigger auto-rollback

### Timeline
- Remaining 6 clients: 3 weeks
- Testing and validation: 2 weeks
- Go-live target: 2026-05-15

## Action Items
- [ ] Document rollback procedure in runbook @Dan 📅 2026-03-22
- [ ] Set up per-client feature flags @Frank 📅 2026-03-22
- [ ] Configure latency alerting for v2 endpoints @Alice 📅 2026-03-20

## Follow-Up
- Weekly migration status in team sync
- Full go-live readiness review at 2026-05-01
