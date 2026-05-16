from datetime import datetime
from utils.llm import llm


def detect_fraud(transaction=None, language="english"):

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ================= LANGUAGE SUPPORT ================= #

    language_map = {
        "english": "English",
        "kannada": "Kannada",
        "hindi": "Hindi",
        "tamil": "Tamil",
        "telugu": "Telugu",
        "malayalam": "Malayalam"
    }

    selected_language = language_map.get(
        language.lower(),
        "English"
    )

    # ==================================================
    # EXPLANATION MODE
    # ==================================================

    if transaction is None:

        prompt = f"""
You are an enterprise multilingual banking fraud detection AI.

IMPORTANT:
- Respond ONLY in {selected_language}
- Keep response short
- Professional banking tone
- Customer friendly

Explain fraud detection in banking.

Include:
- AI monitoring
- anomaly detection
- suspicious transactions
- risk scoring
- device + location tracking

Keep response:
- simple
- clear
- practical
"""

        response = llm.invoke(prompt)

        return {
            "response": response.content,
            "risk_score": None,
            "status": "EXPLANATION",
            "language": selected_language,
            "timestamp": current_time
        }

    # ==================================================
    # ANALYSIS MODE
    # ==================================================

    score = 0
    alerts = []

    amount = transaction.get("amount", 0)
    location = transaction.get("location", "India")
    txn_time = transaction.get("time", "")
    device = transaction.get("device", "Mobile")

    # ================= FRAUD RULES ================= #

    if amount > 50000:
        score += 30
        alerts.append("High transaction amount")

    if any(x in location.lower() for x in ["foreign", "vpn", "russia", "unknown"]):
        score += 25
        alerts.append("Suspicious location")

    if any(x in txn_time.lower() for x in ["night", "02", "03"]):
        score += 20
        alerts.append("Odd-time transaction")

    if any(x in device.lower() for x in ["unknown", "new"]):
        score += 20
        alerts.append("Unknown device")

    # ================= RISK LABEL ================= #

    if score >= 60:
        label = "HIGH RISK 🚨"
    elif score >= 30:
        label = "MEDIUM RISK ⚠️"
    else:
        label = "LOW RISK ✅"

    # ==================================================
    # CLEAN ALERT TEXT
    # ==================================================

    alerts_text = (
        "\n".join([f"- {a}" for a in alerts])
        if alerts
        else "No suspicious activity detected"
    )

    # ==================================================
    # LLM FRAUD REPORT
    # ==================================================

    prompt = f"""
You are a senior multilingual banking fraud analyst AI.

IMPORTANT:
- Respond ONLY in {selected_language}
- Professional banking style
- Keep response short and clean
- Explain clearly
- Use emojis minimally

Analyze the transaction and generate a professional fraud report.

Transaction Details:
- Amount: ₹{amount}
- Location: {location}
- Device: {device}
- Time: {txn_time}

Risk Score: {score}%
Risk Status: {label}

Fraud Alerts:
{alerts_text}

Generate response including:
- short fraud analysis
- clear risk explanation
- AI monitoring insight
- recommendation for customer

Keep it professional and customer friendly.
"""

    response = llm.invoke(prompt)

    return {
        "response": response.content,
        "risk_score": score,
        "status": label,
        "language": selected_language,
        "timestamp": current_time
    }