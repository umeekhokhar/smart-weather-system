from abc import ABC, abstractmethod
from typing import Dict, Any

# --- STRUCTURAL PATTERN: AUTHENTICATION INTERFACE ---
class IUserService(ABC):
    @abstractmethod
    def register(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def login(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def validate_schema(self, data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        pass

# Schema definitions for validation
USER_SCHEMA = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 1},
        "password": {"type": "string", "minLength": 1},
        "host_city": {"type": "string", "minLength": 1}
    },
    "required": ["username", "password", "host_city"]
}

LOGIN_SCHEMA = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minLength": 1},
        "password": {"type": "string", "minLength": 1}
    },
    "required": ["username", "password"]
}

# Simple schema validator function
def validate_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """
    Basic schema validation function.
    In a real app, use a library like jsonschema for comprehensive validation.
    """
    if not isinstance(data, dict):
        return False

    # Check required fields
    required = schema.get("required", [])
    for field in required:
        if field not in data or not data[field]:
            return False

    # Check types (basic check)
    properties = schema.get("properties", {})
    for field, field_schema in properties.items():
        if field in data:
            expected_type = field_schema.get("type")
            if expected_type == "string" and not isinstance(data[field], str):
                return False
            # Add more type checks as needed

    return True
