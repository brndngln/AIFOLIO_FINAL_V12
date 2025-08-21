"""Access control utilities for AIFOLIO."""

import functools
from enum import Enum
from typing import Set, List

class Permission(Enum):
    READ_PORTFOLIO = "read_portfolio"
    WRITE_PORTFOLIO = "write_portfolio"
    ADMIN_ACCESS = "admin_access"

class Role(Enum):
    GUEST = "guest"
    USER = "user"
    ADMIN = "admin"

ROLE_PERMISSIONS = {
    Role.GUEST: {Permission.READ_PORTFOLIO},
    Role.USER: {Permission.READ_PORTFOLIO, Permission.WRITE_PORTFOLIO},
    Role.ADMIN: set(Permission)
}

class User:
    def __init__(self, user_id: str, roles: List[Role] = None):
        self.user_id = user_id
        self.roles = roles or [Role.GUEST]
        self._permissions = self._calculate_permissions()
    
    def _calculate_permissions(self) -> Set[Permission]:
        permissions = set()
        for role in self.roles:
            permissions.update(ROLE_PERMISSIONS.get(role, set()))
        return permissions
    
    def has_permission(self, permission: Permission) -> bool:
        return permission in self._permissions

def require_permission(permission: Permission):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Implementation depends on your authentication system
            return func(*args, **kwargs)
        return wrapper
    return decorator
