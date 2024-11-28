from fastapi import HTTPException, status
from functools import wraps
from typing import Callable
from .roles import Action, Resource, ROLE_PERMISSIONS, UserRole

class PermissionChecker:
    def __init__(self, user_role: UserRole):
        self.user_role = user_role
        self.permissions = ROLE_PERMISSIONS.get(user_role, {})

    def has_permission(self, resource: Resource, action: Action) -> bool:
        if resource not in self.permissions:
            return False
        return action in self.permissions[resource]

def require_permission(resource: Resource, action: Action):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, current_user=None, **kwargs):
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            checker = PermissionChecker(current_user.role)
            if not checker.has_permission(resource, action):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"User doesn't have {action} permission for {resource}"
                )
            
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator