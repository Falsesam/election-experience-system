import re


def validate_query(query: str) -> bool:
    """
    Validate user input for correctness and safety.
    """

    # Type check
    if not isinstance(query, str):
        return False

    query = query.strip()

    # Empty input
    if not query:
        return False

    # Length restriction
    if len(query) > 300:
        return False

    # Block potentially harmful patterns
    blocked_patterns = [
        r"<.*?>",       # HTML/script tags
        r"DROP\s+TABLE",
        r"SELECT\s+.*",
        r"--",
        r";"
    ]

    for pattern in blocked_patterns:
        if re.search(pattern, query, re.IGNORECASE):
            return False

    # Allow only safe characters (basic filtering)
    if not re.match(r"^[a-zA-Z0-9\s\?\.,'-]+$", query):
        return False

    return True