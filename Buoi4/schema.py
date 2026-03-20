template = {
    "swagger": "2.0",
    "info": {
        "title": "User & Ticket Management API",
        "version": "1.0.0",
    },
    "definitions": {
        "Error": {
            "type": "object",
            "properties": {
                "error": {"type": "string", "example": "Missing required fields"}
            },
            "required": ["error"],
        },
        "User": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "readOnly": True},
                "username": {"type": "string", "example": "nguyenvana"},
                "email": {
                    "type": "string",
                    "format": "email",
                    "example": "a@example.com",
                },
            },
            "required": ["username", "email"],
        },
        "Ticket": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "readOnly": True},
                "user_id": {"type": "integer", "example": 1},
                "title": {"type": "string", "example": "Loi phan mem"},
                "description": {
                    "type": "string",
                    "example": "Khong dang nhap duoc vao he thong",
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "example": "medium",
                },
            },
            "required": ["user_id", "title", "description"],
        },
    },
}
