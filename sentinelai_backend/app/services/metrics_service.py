from app.db.mongo import attack_logs

def get_attack_metrics():
    total = attack_logs.count_documents({})
    blocks = attack_logs.count_documents({"decision": "block"})
    sanitizes = attack_logs.count_documents({"decision": "sanitize"})

    pipeline = [
        {"$group": {"_id": None, "avgRisk": {"$avg": "$confidence"}}}
    ]

    avg = list(attack_logs.aggregate(pipeline))
    avg_risk = round(avg[0]["avgRisk"], 2) if avg else 0

    return {
        "total_attacks": total,
        "avg_risk": avg_risk,
        "by_decision": {
            "block": blocks,
            "sanitize": sanitizes
        }
    }
