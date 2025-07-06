"""
Multi-Generational IP Guardian Layer — OMNIELITE SYSTEM
- Persistent registry for all IP assets (code, brands, patents, media, etc.)
- Tracks owner, creation, lineage, and inheritance
- Enforces multi-generational IP protection, transfer, and audit
- Integrates with EMMA for logging, audit, and rollback
"""
import os
import json
import threading
from datetime import datetime
from typing import Dict, Any, Optional, List, cast
from core.compliance.emma_guardian import emma

IP_REGISTRY_PATH = os.path.join(
    os.path.dirname(__file__), "../audit/exports/ip_registry.json"
)
IP_LOCK = threading.Lock()


class IPGuardian:
    _instance: Optional["IPGuardian"] = None

    @staticmethod
    def instance() -> "IPGuardian":
        if IPGuardian._instance is None:
            IPGuardian._instance = IPGuardian()
        return IPGuardian._instance

    def __init__(self) -> None:
        self.registry_path: str = IP_REGISTRY_PATH
        if not os.path.exists(os.path.dirname(self.registry_path)):
            os.makedirs(os.path.dirname(self.registry_path), exist_ok=True)
        if not os.path.exists(self.registry_path):
            with open(self.registry_path, "w") as f:
                json.dump([], f)

    def register_ip(self, asset: Dict[str, Any]) -> str:
        with IP_LOCK:
            now: str = datetime.utcnow().isoformat()
            asset["registered_at"] = now
            asset["lineage"] = asset.get("lineage", []) + [asset.get("owner", "unknown")]
            reg: List[Dict[str, Any]] = self._read_registry()
            reg.append(asset)
            self._write_registry(reg)
            emma.log_event("ip_register", asset, critical=True)
            return str(asset.get("id", "unknown"))

    def transfer_ip(self, asset_id: str, new_owner: str, reason: Optional[str] = None) -> bool:
        with IP_LOCK:
            reg: List[Dict[str, Any]] = self._read_registry()
            for asset in reg:
                if asset.get("id") == asset_id:
                    asset["owner"] = new_owner
                    asset["lineage"].append(new_owner)
                    asset["transferred_at"] = datetime.utcnow().isoformat()
                    asset["transfer_reason"] = reason
                    self._write_registry(reg)
                    emma.log_event(
                        "ip_transfer",
                        {"asset_id": asset_id, "new_owner": new_owner, "reason": reason},
                        critical=True,
                    )
                    return True
            return False

    def get_ip(self, asset_id: str) -> Optional[Dict[str, Any]]:
        reg: List[Dict[str, Any]] = self._read_registry()
        for asset in reg:
            if asset.get("id") == asset_id:
                return asset
        return None

    def list_ip(self, owner: Optional[str] = None) -> List[Dict[str, Any]]:
        reg: List[Dict[str, Any]] = self._read_registry()
        if owner:
            return [a for a in reg if a.get("owner") == owner]
        return reg

    def enforce_protection(self, asset_id: str, action: str, actor: str) -> bool:
        asset: Optional[Dict[str, Any]] = self.get_ip(asset_id)
        if not asset:
            return False
        # Example: Block non-owner destructive actions
        if action in ["delete", "export", "transfer"] and actor != asset.get("owner"):
            emma.log_event(
                "ip_protection_blocked",
                {"asset_id": asset_id, "action": action, "actor": actor},
                critical=True,
            )
            return False
        emma.log_event(
            "ip_action",
            {"asset_id": asset_id, "action": action, "actor": actor},
            critical=False,
        )
        return True

    def _read_registry(self) -> List[Dict[str, Any]]:
        with open(self.registry_path, "r") as f:
            return cast(List[Dict[str, Any]], json.load(f))

    def _write_registry(self, reg: List[Dict[str, Any]]) -> None:
        with open(self.registry_path, "w") as f:
            json.dump(reg, f, indent=2)


# Singleton instance for global use
ip_guardian: IPGuardian = IPGuardian.instance()
