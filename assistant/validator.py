import re


def validate_query(query: str) -> bool:
    """
    Validate user input for correctness and safety.
    """

    # Check type
    if not isinstance(query, str):
        return False

    query = query.strip()

    # Empty input check
    if len(query) == 0:
        return False

    # Length limit
    if len(query) > 300:
        return False

    # Basic sanitization (prevent unusual characters)
    if re.search(r"[<>]", query):
        return False

    return True