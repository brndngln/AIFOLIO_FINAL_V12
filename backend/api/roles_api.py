"""SAFE AI MODULE"""

ct = None  # TODO: Define ct
data = {}  # TODO: Define data
admin_id = ""  # TODO: Define admin_id
roles = []  # TODO: Define roles

"SAFE AI MODULE"
"SAFE AI MODULE"
from fastapi import Body

from security.role_manager import list_admins


def list_roles():
    return list_admins()


def set_roles(data: dict = Body(...)):
    return {"success": True, "adminId": admin_id, "roles": roles}
