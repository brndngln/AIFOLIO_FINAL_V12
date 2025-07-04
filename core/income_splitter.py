# income_splitter.py
# Splits income according to customizable logic per tier
<<<<<<< HEAD
import json
=======
>>>>>>> omni_repair_backup_20250704_1335
class IncomeSplitter:
    def __init__(self, split_config):
        self.split_config = split_config
    def split_income(self, amount, tier='default'):
        conf = self.split_config.get(tier, self.split_config['default'])
        return {
            'reinvestment': amount * conf['reinvestment'],
            'liquidity': amount * conf['liquidity'],
            'goals': amount * conf['goals'],
            'rnd': amount * conf['rnd'],
            'emergency': amount * conf['emergency']
        }
