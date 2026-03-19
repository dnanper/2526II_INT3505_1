template = {
    "swagger": "2.0",
    "info": {
        "title": "User & Ticket Management API",
        "version": "1.0.0",
    },
    "definitions": {
        "User": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "readOnly": True},
                "username": {"type": "string", "example": "nguyenvana"},
                "email": {"type": "string", "format": "email", "example": "a@example.com"}
            },
            "required": ["username", "email"]
        },
        "Ticket": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "readOnly": True},
                "title": {"type": "string", "example": "Lỗi phần mềm"},
                "description": {"type": "string"},
                "priority": {"type": "string", "enum": ["low", "medium", "high"]}
            },
            "required": ["title"]
        }
    }
}