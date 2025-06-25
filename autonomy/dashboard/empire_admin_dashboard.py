"""
AIFOLIO™ Empire Admin Dashboard (Backend Logic)
Surfaces SAFE AI engine logs, compliance alerts, crisis events, and legacy DNA for owner review.
Static, deterministic, non-sentient. Owner-controlled. No adaptive logic.
"""
import importlib
from typing import Dict, List

MODULES = [
    'ai_partner_ecosystem_builder',
    'multi_brand_engine',
    'ai_license_to_enter_engine',
    'ai_market_signal_engine',
    'ai_compliance_governance_monitor',
    'ai_royalty_engine',
    'private_banking_interface',
    'future_sale_value_optimizer',
    'ai_growth_dna_engine',
    'ai_global_risk_guardian',
    'ai_predictive_market_monitor',
    'ai_platform_decoupling_engine',
    'ai_empire_capital_engine',
    'ai_family_trust_planner',
    'ai_unknown_risk_monitor',
    'ai_global_vault_router',
    'ai_peer_monitor',
    'ai_crisis_mode_protocols',
    'ai_ultimate_empire_dna_engine',
    'ai_phase_60_legacy_empire_engine'
]

class EmpireAdminDashboard:
    def __init__(self):
        self.engines = {}
        for mod in MODULES:
            try:
                self.engines[mod] = importlib.import_module(f"autonomy.ai_static_engines.{mod}")
            except Exception as e:
                self.engines[mod] = None

    def get_all_logs(self) -> Dict[str, List[Dict]]:
        logs = {}
        for mod, module in self.engines.items():
            if module and hasattr(module, 'export_legacy_log'):
                logs[mod] = module.export_legacy_log()
            elif module:
                # Try common log methods
                for log_method in [
                    'export_partner_log', 'export_brand_log', 'export_license_log', 'export_signal_log',
                    'get_alerts', 'get_royalty_history', 'export_banking_log', 'export_valuation_log',
                    'get_growth_dna_archive', 'get_risk_alerts', 'get_market_signals',
                    'export_decoupling_log', 'get_capital_log', 'export_trust_log',
                    'get_unknown_risks', 'export_routing_log', 'get_peer_moves',
                    'get_crisis_events', 'get_empire_dna_archive']:
                    if hasattr(module, log_method):
                        logs[mod] = getattr(module, log_method)()
                        break
        return logs
