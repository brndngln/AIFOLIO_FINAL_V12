# vault_funding_manager.py
# Manages funding, reinvestment, and vault-level allocation logic
import json
from .liquidity_buffer_guard import LiquidityBufferGuard
from .income_splitter import IncomeSplitter
from .purchase_authorization_engine import PurchaseAuthorizationEngine
from .reinvestment_detector import ReinvestmentDetector
from .billionaire_brain_profiles import BillionaireBrainProfiles
from .goal_priority_matrix import GoalPriorityMatrix
from .multi_vault_growth_sync import MultiVaultGrowthSync
from .AI_reinvestment_logicsuite import AIReinvestmentLogicSuite

class VaultFundingManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.load_config()
        self.liquidity_guard = LiquidityBufferGuard(self.config['liquidity_min'])
        self.splitter = IncomeSplitter(self.config['income_split'])
        self.auth_engine = PurchaseAuthorizationEngine()
        self.reinvest_detector = ReinvestmentDetector()
        self.brain_profiles = BillionaireBrainProfiles()
        self.goal_matrix = GoalPriorityMatrix()
        self.growth_sync = MultiVaultGrowthSync()
        self.reinvest_logic = AIReinvestmentLogicSuite()

    def load_config(self):
        with open(self.config_path) as f:
            self.config = json.load(f)

    def process_income(self, vault_id, amount):
        split = self.splitter.split_income(amount)
        self.liquidity_guard.update_buffer(split['liquidity'])
        self.growth_sync.sync(vault_id, split)
        return split

    def propose_reinvestments(self, vault_id, vault_stats):
        proposals = self.reinvest_detector.detect(vault_stats)
        proposals = self.reinvest_logic.rank_and_filter(proposals, self.brain_profiles)
        proposals = self.liquidity_guard.filter_by_buffer(proposals)
        return proposals

    def authorize_purchase(self, proposal, user_id):
        return self.auth_engine.authorize(proposal, user_id)
