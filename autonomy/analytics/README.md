# AIFOLIO Analytics & SAFE AI Audit Logs

All analytics, audit logs, and SAFE AI outputs are stored here for admin review and compliance documentation.

## SAFE AI Analytics Modules
- `buyer_analytics.py`: Static group segmentation (first-time, repeat, high-value, region)
- `revenue_tracker.py`: Tracks total revenue, by vault/niche/time, refund-adjusted
- `vault_performance.py`: Vault performance by revenue, sales, conversion rate
- `compliance_tracker.py`: Legal/compliance stats (% with policy, confirmations, receipts)
- `nl_query_parser.py`: Safe static NL query parsing for analytics
- `segment_trend_detector.py`: Static trend detection for segments
- `revenue_milestone_tracker.py`: Logs revenue milestones
- `vault_launch_impact_report.py`: Logs stats after vault launch
- `refund_ratio_monitor.py`: Refund % monitor and admin alert

## Dashboard & Data Files
- `analytics_dashboard.json`: Dashboard config
- `analytics_dashboard.md`: Dashboard documentation
- `buyer_segments.json`: Group stats only (no profiling)
- `analytics_log.json`: Append-only log of all analytics actions

## Exports & Reports
- `revenue_report_export.py`: PDF export (static template, admin-only)
- All exports and admin views are logged for audit
- Email summary (admin only, requires SendGrid API)

## SAFE AI Compliance
- No adaptive logic, no profiling of individuals, no optimization/targeting
- No AI rewriting of reports, all exports use static templates
- 100% static, deterministic, and human-reviewed for compliance
- All actions are logged, no autonomous or sentient logic

Admins can view, export, and audit all logs and reports from the dashboard. All analytics are static, non-sentient, and SAFE AI compliant.
