import re

# Enhanced patterns using regex for flexible matching
UNETHICAL_PATTERNS = [
    (r"\bundress", "undress/undressing"),
    (r"\bremove.{0,20}(clothes|clothing|garment)", "remove clothes"),
    (r"\bnude\b", "nude"),
    (r"\bnaked\b", "naked"),
    (r"deepfake.{0,20}(her|him|them|person)", "deepfake person"),
    (r"make.{0,20}explicit", "make explicit"),
    (r"reveal.{0,20}(private|body|intimate)", "reveal private/body"),
    (r"(clothes|clothing|garment).{0,20}(disappear|vanish|fade|dissolve)", "clothes disappear"),
    (r"(strip|stripping).{0,20}(clothes|naked|nude)", "stripping"),
    (r"sexually.{0,20}explicit", "sexually explicit"),
    (r"generate.{0,20}(nude|naked|nsfw|explicit)", "generate inappropriate"),
    (r"without.{0,20}(clothes|clothing)", "without clothes"),
    (r"expose.{0,20}(body|skin|private)", "expose body"),
    (r"artistic.{0,20}(nudity|nude|undress)", "artistic nudity"),
]

def ethics_check(text: str):
    text_lower = text.lower()
    matched_triggers = []

    for pattern_regex, pattern_name in UNETHICAL_PATTERNS:
        if re.search(pattern_regex, text_lower):
            matched_triggers.append({
                "pattern": pattern_name,
                "match": re.search(pattern_regex, text_lower).group(),
                "severity": "high"
            })

    if matched_triggers:
        return {
            "ethical_risk": True,
            "reason": matched_triggers[0]["pattern"],
            "score": 0.9,
            "triggers": matched_triggers
        }

    return {
        "ethical_risk": False,
        "reason": None,
        "score": 0.1,
        "triggers": []
    }
