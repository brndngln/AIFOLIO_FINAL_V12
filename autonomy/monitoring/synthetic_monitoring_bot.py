import time
import json
import random
import datetime
import os
from typing import Dict, Any, List

MONITOR_LOG = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "../../analytics/synthetic_monitor_log.jsonl"
    )
)
os.makedirs(os.path.dirname(MONITOR_LOG), exist_ok=True)

USER_FLOWS = [
    {
        "name": "buy_vault",
        "steps": ["visit_home", "select_vault", "checkout", "download"],
    },
    {"name": "request_refund", "steps": ["login", "find_order", "initiate_refund"]},
    {"name": "admin_audit", "steps": ["admin_login", "view_logs", "export_report"]},
]


def simulate_user_flow(flow: Dict[str, Any]) -> Dict[str, Any]:
    result = {"flow": flow["name"], "steps": [], "success": True}
    for step in flow["steps"]:
        latency = round(random.uniform(0.05, 1.5), 2)
        fail = random.random() < 0.01
        result["steps"].append({"step": step, "latency": latency, "fail": fail})
        if fail:
            result["success"] = False
            break
        time.sleep(0.01)
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "result": result,
    }
    with open(MONITOR_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return result


def run_all_flows() -> List[Dict[str, Any]]:
    return [simulate_user_flow(flow) for flow in USER_FLOWS]


if __name__ == "__main__":
    print(run_all_flows())
