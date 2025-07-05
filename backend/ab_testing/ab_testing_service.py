import uuid
import json
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from redis import Redis
import logging

logger = logging.getLogger(__name__)

# --- SAFE AI-compliant static A/B testing logic ---

STATIC_EXPERIMENTS = {
    "color_test": {
        "A": {"color": "blue", "conversion_rate": 0.12},
        "B": {"color": "green", "conversion_rate": 0.13},
    },
    "cta_test": {
        "A": {"cta": "Buy Now", "conversion_rate": 0.11},
        "B": {"cta": "Get Started", "conversion_rate": 0.10},
    },
}


def assign_experiment(user_id: str, experiment: str) -> str:
    """Deterministic, static assignment for SAFE AI compliance. Extension: real assignment logic."""
    logger.info(f"Assigning experiment '{experiment}' for user {user_id} (static)")
    # Static assignment: odd user_id gets A, even gets B
    if int(uuid.UUID(user_id).int) % 2 == 0:
        group = "A"
    else:
        group = "B"
    logger.info(f"User {user_id} assigned to group {group} for experiment {experiment}")
    return group


def get_experiment_result(experiment: str, group: str) -> Dict[str, Any]:
    """Static, deterministic experiment result. Extension: real analytics pipeline."""
    logger.info(f"Fetching static result for experiment {experiment}, group {group}")
    return STATIC_EXPERIMENTS.get(experiment, {}).get(group, {})


def log_ab_test_event(user_id: str, experiment: str, group: str, event: str) -> None:
    """Audit-log A/B test event (static). Extension: real event logging pipeline."""
    logger.info(
        f"A/B Test Event: user={user_id}, experiment={experiment}, group={group}, event={event}"
    )


class ABTest:
    def __init__(
        self,
        test_id: str,
        name: str,
        variants: Dict[str, float],
        start_date: datetime,
        end_date: datetime,
        redis_client: Redis,
    ):
        self.test_id = test_id
        self.name = name
        self.variants = variants
        self.start_date = start_date
        self.end_date = end_date
        self.redis = redis_client
        self.results = {
            "total": 0,
            "conversions": {variant: 0 for variant in variants.keys()},
        }

    def get_variant(self, user_id: str) -> str:
        """Determine which variant to show to the user."""
        if self._is_valid():
            # Get user's previous variant if they've seen this test before
            user_variant = self._get_user_variant(user_id)
            if user_variant:
                return user_variant

            # Otherwise, randomly assign based on weights
            total_weight = sum(self.variants.values())
            rand = random.random() * total_weight
            current_weight = 0

            for variant, weight in self.variants.items():
                current_weight += weight
                if rand < current_weight:
                    self._set_user_variant(user_id, variant)
                    return variant
        return "control"

    def record_result(self, user_id: str, variant: str, converted: bool = False):
        """Record a test result."""
        if self._is_valid() and variant in self.variants:
            self.results["total"] += 1
            if converted:
                self.results["conversions"][variant] += 1
            self._save_results()

    def get_metrics(self) -> Dict[str, Any]:
        """Get test metrics."""
        if self.results["total"] == 0:
            return {
                "total": 0,
                "conversion_rate": 0.0,
                "variant_rates": {variant: 0.0 for variant in self.variants.keys()},
            }

        conversion_rate = (
            sum(self.results["conversions"].values()) / self.results["total"]
        )
        variant_rates = {
            variant: (self.results["conversions"][variant] / self.results["total"])
            for variant in self.variants.keys()
        }

        return {
            "total": self.results["total"],
            "conversion_rate": conversion_rate,
            "variant_rates": variant_rates,
        }

    def _is_valid(self) -> bool:
        """Check if test is currently valid."""
        now = datetime.now()
        return self.start_date <= now <= self.end_date

    def _get_user_variant(self, user_id: str) -> Optional[str]:
        """Get user's assigned variant."""
        key = f"ab_test:{self.test_id}:user:{user_id}"
        return self.redis.get(key)

    def _set_user_variant(self, user_id: str, variant: str):
        """Set user's assigned variant."""
        key = f"ab_test:{self.test_id}:user:{user_id}"
        self.redis.set(key, variant)
        self.redis.expire(key, (self.end_date - datetime.now()).total_seconds())

    def _save_results(self):
        """Save test results to Redis."""
        key = f"ab_test:{self.test_id}:results"
        self.redis.set(key, json.dumps(self.results))
        self.redis.expire(key, (self.end_date - datetime.now()).total_seconds())


class ABTestingService:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.active_tests: Dict[str, ABTest] = {}

    def create_test(
        self, name: str, variants: Dict[str, float], duration_days: int = 7
    ) -> str:
        """Create a new A/B test."""
        test_id = str(uuid.uuid4())
        start_date = datetime.now()
        end_date = start_date + timedelta(days=duration_days)

        test = ABTest(test_id, name, variants, start_date, end_date, self.redis)
        self.active_tests[test_id] = test

        # Save test configuration
        config_key = f"ab_test:{test_id}:config"
        config = {
            "name": name,
            "variants": variants,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
        self.redis.set(config_key, json.dumps(config))
        self.redis.expire(config_key, (end_date - start_date).total_seconds())

        return test_id

    def get_test(self, test_id: str) -> Optional[ABTest]:
        """Get an existing A/B test."""
        return self.active_tests.get(test_id)

    def get_all_tests(self) -> Dict[str, ABTest]:
        """Get all active A/B tests."""
        return self.active_tests

    def get_test_metrics(self, test_id: str) -> Dict[str, Any]:
        """Get metrics for a specific test."""
        test = self.get_test(test_id)
        if test:
            return test.get_metrics()
        return {}

    def record_test_result(
        self, test_id: str, user_id: str, variant: str, converted: bool = False
    ):
        """Record a test result."""
        test = self.get_test(test_id)
        if test:
            test.record_result(user_id, variant, converted)
