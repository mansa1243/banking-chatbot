import json
from datetime import datetime
from utils.llm import llm


# ==================================================
# FILE PATHS
# ==================================================

TRANSACTION_FILE = "data/transactions.json"

USERS_FILE = "data/users.json"


# ==================================================
# LOAD TRANSACTIONS
# ==================================================

def load_data():

    try:

        with open(
            TRANSACTION_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return []


# ==================================================
# SAVE TRANSACTIONS
# ==================================================

def save_data(data):

    with open(
        TRANSACTION_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# ==================================================
# LOAD USERS
# ==================================================

def load_users():

    try:

        with open(
            USERS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

            # ==========================================
            # SUPPORT LIST FORMAT
            # ==========================================

            if isinstance(data, list):

                users = {}

                for item in data:

                    username = item.get("user")

                    if username:
                        users[username] = item

                return users

            # ==========================================
            # SUPPORT DICT FORMAT
            # ==========================================

            return data

    except:

        return {}


# ==================================================
# SAVE USERS
# ==================================================

def save_users(users):

    with open(
        USERS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            users,
            f,
            indent=4,
            ensure_ascii=False
        )


# ==================================================
# DETECT LANGUAGE
# ==================================================

def detect_language(text):

    text = str(text).lower()

    # Kannada
    if any(word in text for word in [

        "ಕಳುಹಿಸು",
        "ಕಳಿಸು",
        "ವರ್ಗಾವಣೆ",
        "ರಿಂದ",
        "ಗೆ"

    ]):

        return "Kannada"

    # Telugu
    elif any(word in text for word in [

        "పంపించు",
        "డబ్బు పంపు",
        "నుంచి",
        "కి"

    ]):

        return "Telugu"

    # Hindi
    elif any(word in text for word in [

        "भेजो",
        "ट्रांसफर",
        "से",
        "को"

    ]):

        return "Hindi"

    # Tamil
    elif any(word in text for word in [

        "அனுப்பு"

    ]):

        return "Tamil"

    # Malayalam
    elif any(word in text for word in [

        "അയക്കുക"

    ]):

        return "Malayalam"

    return "English"


# ==================================================
# TRANSFER MONEY
# ==================================================

def transfer_money(
    sender,
    receiver,
    amount,
    query="",
    scheduled=False,
    language=None
):

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # ==================================================
    # LOAD USERS
    # ==================================================

    users = load_users()

    # ==================================================
    # DETECT LANGUAGE
    # ==================================================

    if language:

        selected_language = language.capitalize()

    else:

        selected_language = detect_language(query)

    # ==================================================
    # VALIDATE SENDER
    # ==================================================

    if sender not in users:

        response = llm.invoke(f"""
You are a multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Professional banking tone
- Keep response short

User attempted money transfer.

Sender account not found:
{sender}

Generate banking validation response.
""")

        return {
            "response": response.content,
            "status": "failed",
            "language": selected_language,
            "timestamp": current_time
        }

    # ==================================================
    # VALIDATE RECEIVER
    # ==================================================

    if receiver not in users:

        response = llm.invoke(f"""
You are a multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Professional banking style
- Keep response concise

Receiver account not found:
{receiver}

Generate banking response.
""")

        return {
            "response": response.content,
            "status": "failed",
            "language": selected_language,
            "timestamp": current_time
        }

    # ==================================================
    # SAME USER CHECK
    # ==================================================

    if sender == receiver:

        response = llm.invoke(f"""
You are a multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Keep response professional

Generate validation response:
Sender and receiver cannot be same.
""")

        return {
            "response": response.content,
            "status": "failed",
            "language": selected_language,
            "timestamp": current_time
        }

    # ==================================================
    # VALIDATE AMOUNT
    # ==================================================

    try:

        amount = float(amount)

    except:

        response = llm.invoke(f"""
You are a multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}

Generate response:
Invalid amount format.
""")

        return {
            "response": response.content,
            "status": "failed",
            "language": selected_language,
            "timestamp": current_time
        }

    # ==================================================
    # NEGATIVE AMOUNT
    # ==================================================

    if amount <= 0:

        response = llm.invoke(f"""
You are a multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}

Generate validation response:
Amount must be greater than zero.
""")

        return {
            "response": response.content,
            "status": "failed",
            "language": selected_language,
            "timestamp": current_time
        }

    # ==================================================
    # CHECK BALANCE
    # ==================================================

    if users[sender]["balance"] < amount:

        response = llm.invoke(f"""
You are a multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Professional banking tone

Customer balance insufficient.

Available Balance:
₹{users[sender]["balance"]}

Requested Amount:
₹{amount}

Generate banking response.
""")

        return {
            "response": response.content,
            "status": "failed",
            "language": selected_language,
            "timestamp": current_time
        }

    # ==================================================
    # UPDATE BALANCE
    # ==================================================

    users[sender]["balance"] -= amount

    users[receiver]["balance"] += amount

    # ==================================================
    # SAVE USERS
    # ==================================================

    save_users(users)

    # ==================================================
    # TRANSACTION ID
    # ==================================================

    transaction_id = f"TXN{datetime.now().strftime('%H%M%S')}"

    # ==================================================
    # SAVE TRANSACTION
    # ==================================================

    data = load_data()

    txn = {

        "transaction_id": transaction_id,

        "user": sender,

        "to": receiver,

        "amount": amount,

        "date": current_time,

        "type": (
            "SCHEDULED"
            if scheduled
            else "INSTANT"
        ),

        "status": "SUCCESS"
    }

    data.append(txn)

    save_data(data)

    # ==================================================
    # TRANSACTION TYPE
    # ==================================================

    transaction_type = (

        "Scheduled Transfer"

        if scheduled else

        "Instant Transfer"
    )

    # ==================================================
    # AI RESPONSE
    # ==================================================

    response = llm.invoke(f"""
You are a professional multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Professional banking style
- Keep response concise
- Customer friendly
- Use emojis minimally

Generate a clean money transfer confirmation.

Transaction Details:
Transaction ID: {transaction_id}

From: {sender}
To: {receiver}

Amount: ₹{amount}

Time: {current_time}

Transaction Type:
{transaction_type}

Status:
SUCCESS

Generate:
- success confirmation
- transaction summary
- short banking note
""")

    # ==================================================
    # FINAL RESPONSE
    # ==================================================

    return {

        "response": response.content,

        "status": "success",

        "language": selected_language,

        "timestamp": current_time,

        "transaction": {

            "transaction_id": transaction_id,

            "from": sender,

            "to": receiver,

            "amount": amount,

            "time": current_time,

            "type": transaction_type,

            "status": "SUCCESS"
        }
    }