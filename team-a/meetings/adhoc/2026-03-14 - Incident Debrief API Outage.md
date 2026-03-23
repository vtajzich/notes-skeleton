# 2026-03-14 - Incident Debrief: API Outage
#work/team-a/meetings/adhoc

## Meeting Summary
- 45-minute outage on 2026-03-13 caused by misconfigured rate limiter
- Root cause: config change deployed without canary
- Agreed on mandatory canary deployment for config changes

## Key Discussion Points
### Incident Timeline
- 14:22 — Rate limiter config deployed to all regions simultaneously
- 14:25 — Error rate spike detected by monitoring
- 14:31 — On-call (Dan) paged
- 14:45 — Config rolled back
- 15:07 — Full recovery confirmed

### Root Cause
- New rate limit threshold was 10x lower than intended (typo: 100 instead of 1000)
- No canary deployment for config changes — went straight to production
- Monitoring caught it quickly, but 19 minutes of elevated errors

### Preventive Measures
- All config changes must go through canary deployment (same as code)
- Add config validation step that compares new vs current values
- Alerting threshold for config drift

## Action Items
- [ ] Implement canary deployment for config changes @Dan 📅 2026-03-21
- [ ] Add config validation pre-deploy check @Frank 📅 2026-03-28
- [ ] Write postmortem and share with platform leads @Me 📅 2026-03-17

## Follow-Up
- Canary deployment implementation review next week
- Postmortem presentation at next platform leads meeting
