"""
Generate heatmap data for text highlighting - shows which words triggered detection
"""
import re
from typing import List, Dict, Tuple


def extract_trigger_words(text: str, patterns: List[str]) -> List[Dict]:
    """
    Find all trigger words/patterns in text and return their positions
    
    Args:
        text: Input text to analyze
        patterns: List of patterns/keywords to search for
        
    Returns:
        List of dicts with word, position, length, severity
    """
    triggers = []
    
    for pattern in patterns:
        # Find all occurrences of the pattern (case-insensitive)
        for match in re.finditer(r'\b' + re.escape(pattern) + r'\b', text, re.IGNORECASE):
            triggers.append({
                "word": text[match.start():match.end()],
                "start": match.start(),
                "end": match.end(),
                "pattern": pattern,
                "severity": "high"
            })
    
    # Sort by position
    triggers.sort(key=lambda x: x["start"])
    return triggers


def generate_text_heatmap(text: str, triggers_list: List[Dict], risk_score: float) -> Dict:
    """
    Generate heatmap visualization data for text highlighting
    
    Args:
        text: Original input text
        triggers_list: List of trigger dictionaries from ethics/injection detectors
        risk_score: Overall risk score (0-1)
        
    Returns:
        Dict with heatmap data including colored segments
    """
    if not triggers_list:
        return {
            "segments": [{"text": text, "color": "neutral"}],
            "risk_heat": 0.0,
            "highlighted_words": []
        }
    
    # Remove duplicates and sort by position
    unique_triggers = {}
    for trigger in triggers_list:
        key = (trigger.get("start"), trigger.get("end"))
        if key not in unique_triggers:
            unique_triggers[key] = trigger
    
    sorted_triggers = sorted(unique_triggers.values(), key=lambda x: x.get("start", 0))
    
    # Build segments with colors
    segments = []
    last_end = 0
    
    for trigger in sorted_triggers:
        start = trigger.get("start", 0)
        end = trigger.get("end", 0)
        
        # Add neutral text before trigger
        if start > last_end:
            segments.append({
                "text": text[last_end:start],
                "color": "neutral"
            })
        
        # Add highlighted trigger
        severity = trigger.get("severity", "high")
        color = "red" if severity == "high" else "orange" if severity == "medium" else "yellow"
        
        segments.append({
            "text": text[start:end],
            "color": color,
            "pattern": trigger.get("pattern", ""),
            "reason": trigger.get("reason", "Suspicious pattern detected")
        })
        
        last_end = end
    
    # Add remaining neutral text
    if last_end < len(text):
        segments.append({
            "text": text[last_end:],
            "color": "neutral"
        })
    
    return {
        "segments": segments,
        "risk_heat": min(1.0, risk_score),
        "highlighted_words": [t.get("word") for t in sorted_triggers],
        "trigger_count": len(sorted_triggers)
    }


def get_risk_color(score: float) -> str:
    """Get color based on risk score"""
    if score >= 0.85:
        return "red"      # Critical
    elif score >= 0.75:
        return "orange"   # High
    elif score >= 0.5:
        return "yellow"   # Medium
    else:
        return "green"    # Safe


def create_word_importance_map(text: str, injection_triggers: List[str], 
                               ethics_triggers: List[str]) -> Dict[str, float]:
    """
    Create a map of word importance/risk score for gradient visualization
    
    Returns dict with word positions and risk values for heatmap gradient
    """
    words = text.split()
    importance_map = {}
    
    for i, word in enumerate(words):
        score = 0.0
        
        # Check if word appears in injection triggers
        if any(trigger.lower() in word.lower() for trigger in injection_triggers):
            score += 0.6
        
        # Check if word appears in ethics triggers  
        if any(trigger.lower() in word.lower() for trigger in ethics_triggers):
            score += 0.8
        
        if score > 0:
            importance_map[str(i)] = min(1.0, score)
    
    return importance_map
