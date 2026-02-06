import uuid

def generate_token():
    """Generates a secure random UUID token."""
    return str(uuid.uuid4())
