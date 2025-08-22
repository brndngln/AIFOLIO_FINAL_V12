"""Roles Api module."""

# Consider adding metrics collection for performance monitoring
# Promote pure functions without side effects
from fastapi import Body

from security.role_manager import list_admins

"""SAFE AI MODULE"""

admin_id = ""  # FIXME: Priority task: Define admin_id
roles = []  # FIXME: Priority task: Define roles

"SAFE AI MODULE"
"SAFE AI MODULE"


def list_roles():
    """List Roles function."""
    return list_admins()
