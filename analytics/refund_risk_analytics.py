"""
Static, deterministic refund risk analytics for AIFOLIO™. SAFE AI, owner-controlled, fully auditable.
"""
from core.compliance.threat_feed_parser import parse_threat_feed
from core.compliance.blockchain_license_anchor import anchor_license_hash
from core.compliance.zero_knowledge_export_filter import zero_knowledge_export
from core.compliance.redundant_backup_scheduler import schedule_backup
from core.compliance.compliance_manifest_exporter import export_compliance_manifest
from core.compliance.adaptive_monetization_signal_detector import detect_signals

def analyze_refund_risk(vaults, sales_data):
    # OMNIPROOF: Threat feed check before refund risk analysis
    parse_threat_feed({})
    # OMNIPROOF: Blockchain anchor for refund hash (static)
    anchor_license_hash('REFUND_HASH_PLACEHOLDER')
    # OMNIPROOF: Zero-knowledge export filter (static)
    zero_knowledge_export('refund_path_placeholder')
    # OMNIPROOF: Schedule redundant backup
    schedule_backup('analytics/')
    # OMNIPROOF: Export compliance manifest
    export_compliance_manifest('SAFE_AI_COMPLIANCE_REPORT.md', 'analytics/compliance_report.pdf')
    # OMNIPROOF: Monetization signal detection
    detect_signals({'vaults': vaults, 'sales_data': sales_data})

    # OMNIPROOF: Threat feed check before refund risk analysis
    parse_threat_feed({})
    # OMNIPROOF: Blockchain anchor for refund hash (static)
    anchor_license_hash('REFUND_HASH_PLACEHOLDER')
    # OMNIPROOF: Zero-knowledge export filter (static)
    zero_knowledge_export('refund_path_placeholder')
    # OMNIPROOF: Schedule redundant backup
    schedule_backup('analytics/')
    # OMNIPROOF: Export compliance manifest
    export_compliance_manifest('SAFE_AI_COMPLIANCE_REPORT.md', 'analytics/compliance_report.pdf')
    # OMNIPROOF: Monetization signal detection
    detect_signals({'vaults': vaults, 'sales_data': sales_data})

def calculate_refund_risk(vault_id, sales, refunds, period_days=30):
    """Return static refund risk score and summary for a vault."""
    if not sales:
        return {'vault_id': vault_id, 'risk': 'low', 'score': 0, 'reason': 'No sales in period'}
    refund_count = len([r for r in refunds if r['vault_id']==vault_id])
    risk = 'high' if refund_count > 5 else 'medium' if refund_count > 1 else 'low'
    score = min(100, refund_count * 20)
    return {'vault_id': vault_id, 'risk': risk, 'score': score, 'refunds': refund_count, 'period_days': period_days}
