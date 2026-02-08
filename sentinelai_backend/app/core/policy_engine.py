POLICIES = {
    "low":      {"min": 0.0,  "max": 0.65, "action": "allow"},
    "medium":   {"min": 0.65, "max": 0.75, "action": "sanitize"},
    "high":     {"min": 0.75, "max": 1.0,  "action": "block"},
}

def evaluate_policy(detection_result: dict):
    """
    Evaluate security policy based on hybrid detection results.
    
    Supports both legacy single-brain and new 3-brain hybrid results.
    
    Policy thresholds:
    - risk 0.0-0.40: ALLOW (low risk)
    - risk 0.40-0.65: SANITIZE (medium risk)
    - risk 0.65-1.0: BLOCK (high risk)
    
    Args:
        detection_result: Either legacy {confidence, malicious} or hybrid {risk, decision, ...}
    
    Returns:
        dict: {decision, confidence/risk, malicious, triggered_by}
    """
    # Handle new hybrid format (has 'risk' and 'decision' fields)
    if "risk" in detection_result and "decision" in detection_result:
        return {
            "decision": detection_result["decision"],
            "risk": detection_result["risk"],
            "triggered_by": detection_result.get("triggered_by", []),
            "injection": detection_result.get("injection", {}),
            "ethics": detection_result.get("ethics", {}),
            "narrative": detection_result.get("narrative", {})
        }
    
    # Legacy single-brain format (backward compatibility)
    confidence = detection_result.get("confidence", 0.0)
    malicious = detection_result.get("malicious", False)

    # Find policy level based on confidence score
    decision = "allow"  # default
    for level, rule in POLICIES.items():
        if rule["min"] <= confidence < rule["max"]:
            decision = rule["action"]
            break

    # If classifier marked it malicious AND current decision is allow, upgrade to sanitize
    if malicious and decision == "allow":
        decision = "sanitize"

    return {
        "decision": decision,
        "confidence": confidence,
        "malicious": malicious,
        "patterns": detection_result.get("patterns", [])
    }
