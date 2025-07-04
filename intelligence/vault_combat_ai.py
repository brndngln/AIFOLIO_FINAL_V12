# PHASE 91–110: Vault Combat AI — Static, SAFE AI, Owner-Controlled
# Ranks vaults by survivability, profit potential, and scale readiness. Assigns threat levels.

class VaultCombatAI:
    _vaults = []  # [{id, title, earnings, survivability, profit, scale, threat_level}]

    @staticmethod
    def rank_vaults(vaults):
        # Rank by survivability, profit, scale
        for v in vaults:
            v['survivability'] = v.get('earnings', 0) / 1000
            v['profit'] = v.get('earnings', 0)
            v['scale'] = v.get('region_count', 1)
            v['threat_level'] = VaultCombatAI.assign_threat_level(v)
        VaultCombatAI._vaults = vaults
        return vaults

    @staticmethod
    def assign_threat_level(vault):
        if vault['profit'] > 50000:
            return 'Max ROI'
        elif vault['profit'] > 10000:
            return 'High Return'
        elif vault['profit'] > 1000:
            return 'Low Risk'
        else:
            return 'Retire Soon'

    @staticmethod
    def get_vaults():
        return list(VaultCombatAI._vaults)
