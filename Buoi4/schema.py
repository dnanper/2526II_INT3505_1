template = {
    "openapi": "3.1.0",
    "info": {
        "title": "User & Ticket Management API",
        "version": "1.0.0",
    },
    "servers": [
        {
            "url": "http://127.0.0.1:5000",
            "description": "Local Development Server"
        },
        {
            "url": "https://2526-ii-int-3505-1-git-main-dnanpers-projects.vercel.app",
            "description": "Vercel Production Server"
        }
    ],
    "components": {
        "schemas": {
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
        }
    },
}