from enum import Enum
from typing import List
from models.models import UserRole

class Action(str, Enum):
    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

class Resource(str, Enum):
    INVENTORY = "inventory"

ROLE_PERMISSIONS = {
    UserRole.MASTER: {
        Resource.INVENTORY: [Action.READ, Action.CREATE, Action.UPDATE, Action.DELETE],
    },
    UserRole.VENDOR: {
        Resource.INVENTORY: [Action.READ, Action.CREATE],
    },
    UserRole.USER: {
        Resource.INVENTORY: [Action.READ],
    }
}