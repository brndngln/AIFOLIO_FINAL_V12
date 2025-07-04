# PHASE 91–110: Empire Vault Strategist — Static, SAFE AI, Owner-Controlled
# Gives weekly summary of where $/effort should be focused, suggests parallel deployment

class EmpireVaultStrategist:
    _weekly_reports = []

    @staticmethod
    def generate_weekly_report(vaults):
        # Suggest $ focus and parallel deployment
        focus = sorted(vaults, key=lambda v: v.get('profit',0), reverse=True)[:3]
        parallel = [v for v in vaults if v.get('threat_level') == 'Max ROI']
        report = {
            'focus_vaults': [v['id'] for v in focus],
            'parallel_candidates': [v['id'] for v in parallel],
        }
        EmpireVaultStrategist._weekly_reports.append(report)
        return report

    @staticmethod
    def get_reports():
        return list(EmpireVaultStrategist._weekly_reports)
