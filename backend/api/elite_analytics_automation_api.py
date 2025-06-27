"""
Elite analytics, automation, and integration API for AIFOLIO™. Exposes all new static modules and integrations. SAFE AI, owner-controlled, fully auditable.
"""
from fastapi import APIRouter, Request
from analytics import (
    refund_risk_analytics, churn_retention_analytics, asset_health_analytics, tone_voice_analytics, reviewer_performance_heatmap, elite_funnel_analytics, high_ticket_vault_leaderboard
)

router = APIRouter()

@router.post('/analytics/refund_risk')
def refund_risk(data: dict):
    return refund_risk_analytics.calculate_refund_risk(**data)

@router.post('/analytics/churn_retention')
def churn_retention(data: dict):
    return churn_retention_analytics.calculate_churn_retention(**data)

@router.post('/analytics/asset_health')
def asset_health(data: dict):
    return asset_health_analytics.check_asset_health(**data)

@router.post('/analytics/tone_voice')
def tone_voice(data: dict):
    return tone_voice_analytics.check_tone_voice(**data)

@router.post('/analytics/reviewer_heatmap')
def reviewer_heatmap(data: dict):
    return reviewer_performance_heatmap.reviewer_performance_heatmap(**data)

@router.post('/analytics/funnel')
def funnel(data: dict):
    return elite_funnel_analytics.funnel_analytics(**data)

@router.post('/analytics/high_ticket_leaderboard')
def high_ticket_leaderboard(data: dict):
    return high_ticket_vault_leaderboard.high_ticket_vault_leaderboard(**data)
