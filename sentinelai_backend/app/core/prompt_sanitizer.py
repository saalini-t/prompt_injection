import re

INJECTION_PATTERNS = [
    r"ignore.*instructions",
    r"forget.*instructions",
    r"disregard.*instructions",
    r"override.*instructions",
    r"system\s*override",
    r"you\s*are\s*(?:chatgpt|dan|gpt|an\s+\w+)",
    r"send\s+.*secrets",
    r"reveal\s+(?:password|data|secrets|admin)",
    r"execute\s+.*command",
    r"access\s+(?:database|admin|system)",
    r"disable\s+(?:security|firewall)",
    r"bypass\s+(?:firewall|security)",
    r"jailbreak",
    r"act\s+as\s+(?:if\s+)?you\s+(?:are|have)",
    r"pretend.*restrictions",
    r"unrestricted"
]

def sanitize_prompt(text: str):
    """Remove injection attack patterns from prompt"""
    cleaned = text
    
    # Remove each pattern
    for pattern in INJECTION_PATTERNS:
        cleaned = re.sub(pattern, "[BLOCKED]", cleaned, flags=re.IGNORECASE)
    
    # Also convert to lowercase for second pass to catch variants
    if cleaned == text:  # If nothing removed, try lowercase patterns
        text_lower = text.lower()
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, text_lower):
                cleaned = re.sub(pattern, "[BLOCKED]", cleaned, flags=re.IGNORECASE)
    
    return cleaned if cleaned != text else text
