reseller_schema = {
    "type": "object",
    "properties": {
        "cpf": {"type": "string"},
        "fullname": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["cpf", "fullname", "email", "password"],
}

authentication_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["email", "password"],
}


sale_schema = {
    "type": "object",
    "properties": {
        "code": {"type": "string"},
        "date": {"type": "string"},
        "value": {"type": "number"},
    },
    "required": ["code", "date", "value"],
}
