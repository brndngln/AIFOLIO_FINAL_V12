import redis
import os
import json
from datetime import datetime

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
r = redis.from_url(REDIS_URL)
ROLE_KEY = "aifolio:admin_roles"


# Role schema: {admin_id: {roles: ["OWNER","AUDITOR","OPERATOR"], "created": ...}}
def set_admin_roles(admin_id, roles):
    data = {"roles": roles, "created": datetime.utcnow().isoformat()}
    r.hset(ROLE_KEY, admin_id, json.dumps(data))


def get_admin_roles(admin_id):
    val = r.hget(ROLE_KEY, admin_id)
    if not val:
        return []
    try:
        return json.loads(val)["roles"]
    except Exception:
        return []


def is_admin_in_role(admin_id, role):
    return role in get_admin_roles(admin_id)


# List all admins and roles
def list_admins():
    out = {}
    for k, v in r.hgetall(ROLE_KEY).items():
        try:
            out[k.decode()] = json.loads(v)["roles"]
        except Exception:
            out[k.decode()] = []
    return out
