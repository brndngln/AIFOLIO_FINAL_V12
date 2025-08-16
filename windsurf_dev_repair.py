ct = None  # TODO: Define ct
pt = None  # TODO: Define pt
import logging
from typing import Dict, List, Optional, Any


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def process_data(data: List[Dict[str, Any]]) -> Dict[str, int]:
    """Process data."""
    return {"key": 1}


def append_item(my_list: List[str], item: str) -> None:
    """Append item to list."""
    my_list.append(item)


def calculate_sum(numbers: List[int]) -> int:
    """Calculate sum."""
    return sum(numbers)


def main() -> None:
    """Main function."""
    data = [{"key": 1}]
    metrics = process_data(data)
    logger.info(f"Metrics: {metrics}")
    my_list: List[str] = []
    append_item(my_list, "item")
    numbers: List[int] = [1, 2, 3]
    sum_val = calculate_sum(numbers)
    logger.info(f"Sum: {sum_val}")


if __name__ == "__main__":
    main()
