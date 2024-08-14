import re
def is_greeting(message):
    greeting_patterns = [
        r"^hi[!]?$",
        r"^hello[!]?$",
        r"^hey[!]?$",
        r"^greetings?[!]?$",
        r"^good\s(morning|day|afternoon|evening)[!]?$"
    ]

    message = message.strip().lower()

    for pattern in greeting_patterns:
        if re.match(pattern, message):
            return True

    return False