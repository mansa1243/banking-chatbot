import json
import os
import hashlib
import re

from datetime import datetime, timedelta
from utils.llm import llm


# ==================================================
# TIME PARSER
# ==================================================

def parse_time(schedule_time):

    now = datetime.now()

    if isinstance(schedule_time, datetime):
        return schedule_time

    text = str(schedule_time).lower()

    if "tomorrow" in text:

        base = now + timedelta(days=1)

        match = re.search(r'(\d{1,2})(:(\d{2}))?\s*(am|pm)?', text)

        hour = 10
        minute = 0

        if match:

            hour = int(match.group(1))
            minute = int(match.group(3) or 0)

            if match.group(4) == "pm" and hour != 12:
                hour += 12

            if match.group(4) == "am" and hour == 12:
                hour = 0

        return base.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0
        )

    try:
        return datetime.strptime(text, "%Y-%m-%d %H:%M:%S")

    except:
        return now + timedelta(days=1)


# ==================================================
# MAIN FUNCTION
# ==================================================

def schedule_transaction(
    sender,
    receiver,
    amount,
    schedule_time,
    period="once",
    language="english"
):

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_path = "data/schedules.json"

    os.makedirs("data", exist_ok=True)

    # ==================================================
    # LANGUAGE SUPPORT
    # ==================================================

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
    # VALIDATION
    # ==================================================

    if not sender or not receiver:

        response = llm.invoke(f"""
You are a multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Professional banking tone
- Keep response short

Generate banking validation response:
Sender and receiver are required.
""")

        return {
            "status": "failed",
            "message": response.content,
            "language": selected_language,
            "timestamp": current_time
        }

    # ==================================================

    if sender == receiver:

        response = llm.invoke(f"""
You are a multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Professional banking tone
- Keep response concise

Generate banking validation message:
Sender and receiver cannot be same user.
""")

        return {
            "status": "failed",
            "message": response.content,
            "language": selected_language,
            "timestamp": current_time
        }

    # ==================================================

    try:
        amount = float(amount)

    except:

        response = llm.invoke(f"""
You are a multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Keep response customer friendly

Generate banking error response:
Invalid amount format.
""")

        return {
            "status": "failed",
            "message": response.content,
            "language": selected_language,
            "timestamp": current_time
        }

    # ==================================================

    if amount <= 0:

        response = llm.invoke(f"""
You are a multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Professional banking style

Generate validation response:
Amount must be greater than zero.
""")

        return {
            "status": "failed",
            "message": response.content,
            "language": selected_language,
            "timestamp": current_time
        }

    # ==================================================
    # TIME PARSING
    # ==================================================

    parsed_time = parse_time(schedule_time)

    schedule_str = parsed_time.strftime("%Y-%m-%d %H:%M:%S")

    # ==================================================
    # LOAD DATA
    # ==================================================

    if not os.path.exists(file_path):

        with open(file_path, "w") as f:
            json.dump([], f)

    try:

        with open(file_path, "r") as f:
            data = json.load(f)

    except:
        data = []

    # ==================================================
    # DUPLICATE CHECK
    # ==================================================

    tx_hash = hashlib.md5(
        f"{sender}-{receiver}-{amount}-{schedule_str}".encode()
    ).hexdigest()

    for tx in data:

        if tx.get("tx_hash") == tx_hash:

            response = llm.invoke(f"""
You are a multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Professional banking tone
- Keep response short

Generate banking warning:
Duplicate scheduled transaction detected.
""")

            return {
                "status": "failed",
                "message": response.content,
                "language": selected_language,
                "timestamp": current_time
            }

    # ==================================================
    # CREATE ENTRY
    # ==================================================

    new_entry = {
        "id": f"SCH-{len(data)+1}",
        "tx_hash": tx_hash,
        "from": sender,
        "to": receiver,
        "amount": amount,
        "scheduled_time": schedule_str,
        "period": period,
        "status": "Pending",
        "created_at": current_time
    }

    data.append(new_entry)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    # ==================================================
    # LLM CONFIRMATION RESPONSE
    # ==================================================

    response = llm.invoke(f"""
You are a professional multilingual banking scheduler assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Professional banking style
- Keep response concise
- Customer friendly
- Use emojis minimally

Create a clean transaction scheduling confirmation message.

Transaction Details:
From: {sender}
To: {receiver}
Amount: ₹{amount}
Scheduled Time: {schedule_str}
Repeat Type: {period}
Status: Pending

Generate:
- confirmation message
- schedule summary
- short banking note
""")

    return {
        "status": "success",
        "message": response.content,
        "language": selected_language,
        "timestamp": current_time,
        "summary": {
            "from": sender,
            "to": receiver,
            "amount": amount,
            "scheduled_time": schedule_str,
            "period": period,
            "status": "Pending"
        }
    }