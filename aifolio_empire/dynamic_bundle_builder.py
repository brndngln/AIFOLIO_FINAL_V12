from typing import Dict, Any, List, TypedDict

class ItemDict(TypedDict):
    name: str
    price: float

class BundleTemplate(TypedDict):
    min_items: int
    max_items: int
    discount: float
    scarcity: str
    description: str

class BundleDict(TypedDict):
    items: List[ItemDict]
    bundle_type: str
    price: float
    scarcity: str
    description: str

import logging
from datetime import datetime, timedelta
from random import randint

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DynamicBundleBuilder:
    """Creates dynamic product bundles with pricing and scarcity."""

    def __init__(self) -> None:
        """Initialize the bundle builder."""
        self.bundle_templates = {
            "starter": {
                "min_items": 2,
                "max_items": 3,
                "discount": 0.2,
                "scarcity": "limited_time",
                "description": "Perfect for beginners",
            },
            "premium": {
                "min_items": 4,
                "max_items": 6,
                "discount": 0.3,
                "scarcity": "quantity",
                "description": "Advanced collection",
            },
            "ultimate": {
                "min_items": 7,
                "max_items": 10,
                "discount": 0.4,
                "scarcity": "exclusive",
                "description": "Complete mastery",
            },
        }

    def create_bundle(
        self, items: List[Dict[str, Any]], bundle_type: str = "starter"
    ) -> Dict[str, Any]:
        """Create a dynamic bundle from items."""
        template = self.bundle_templates.get(bundle_type)
        if not template:
            raise ValueError(f"Invalid bundle type: {bundle_type}")

        # Validate items
        if len(items) < int(template["min_items"]):
            raise ValueError(f"Not enough items for {bundle_type} bundle")

        # Select random items within range
        num_items = randint(int(template["min_items"]), int(template["max_items"]))
        selected_items = items[:num_items]

        # Calculate bundle price
        total_price = sum(item["price"] for item in selected_items)
        bundle_price = total_price * (1 - float(template["discount"]))

        # Create bundle
        bundle = {
            "name": f"{bundle_type.title()} Bundle",
            "items": selected_items,
            "original_price": total_price,
            "bundle_price": bundle_price,
            "discount": template["discount"],
            "description": template["description"],
            "scarcity": self._create_scarcity(bundle_type),
            "bonus": self._create_bonus(bundle_type),
        }

        return bundle

    def _create_scarcity(self, bundle_type: str) -> Dict[str, Any]:
        """Create scarcity element for bundle."""
        now = datetime.now()

        if bundle_type == "starter":
            # Limited time offer
            end_time = now + timedelta(days=1)
            return {
                "type": "limited_time",
                "end_time": end_time.isoformat(),
                "message": "This offer ends in 24 hours",
            }

        elif bundle_type == "premium":
            # Limited quantity
            remaining = randint(10, 50)
            return {
                "type": "quantity",
                "remaining": remaining,
                "message": f"Only {remaining} bundles left",
            }

        elif bundle_type == "ultimate":
            # Exclusive offer
            return {
                "type": "exclusive",
                "message": "Available exclusively to our VIP members",
            }

    def _create_bonus(self, bundle_type: str) -> Dict[str, Any]:
        """Create bonus offer for bundle."""
        if bundle_type == "starter":
            return {
                "type": "free_resource",
                "value": "Starter Guide PDF",
                "message": "Get our exclusive starter guide FREE",
            }

        elif bundle_type == "premium":
            return {
                "type": "discount",
                "value": 20,
                "message": "Get 20% off your next purchase",
            }

        elif bundle_type == "ultimate":
            return {
                "type": "lifetime_access",
                "value": "Lifetime Updates",
                "message": "Includes lifetime access to all updates",
            }

    def create_bundle_hierarchies(
        self, items: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create multiple bundles with hierarchical pricing."""
        bundles = []
        remaining_items = items.copy()

        # Create bundles from most expensive to least
        for bundle_type in ["ultimate", "premium", "starter"]:
            if not remaining_items:
                break

            bundle = self.create_bundle(remaining_items, bundle_type)
            bundles.append(bundle)

            # Remove used items
            for item in bundle["items"]:
                remaining_items = [i for i in remaining_items if i["id"] != item["id"]]

        return bundles


# Example usage
if __name__ == "__main__":
    builder = DynamicBundleBuilder()

    # Example items
    items = [
        {"id": 1, "name": "AI Mastery Guide", "price": 99.99},
        {"id": 2, "name": "Python Course", "price": 49.99},
        {"id": 3, "name": "Web Development", "price": 79.99},
        {"id": 4, "name": "Marketing Playbook", "price": 69.99},
        {"id": 5, "name": "SEO Secrets", "price": 59.99},
    ]

    # Create bundles
    bundles = builder.create_bundle_hierarchies(items)
    for bundle in bundles:
        print(f"\n{bundle['name']}")
        print(f"Original Price: ${bundle['original_price']:.2f}")
        print(f"Bundle Price: ${bundle['bundle_price']:.2f}")
        print(f"Discount: {bundle['discount']*100}%")
        print(f"Scarcity: {bundle['scarcity']['message']}")
        print(f"Bonus: {bundle['bonus']['message']}\n")
