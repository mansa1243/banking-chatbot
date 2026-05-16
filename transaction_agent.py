import json

from datetime import datetime, timedelta
from collections import defaultdict

from utils.llm import llm


TRANSACTION_FILE = "data/transactions.json"


# ==================================================
# LANGUAGE SUPPORT
# ==================================================

LANGUAGE_MAP = {
    "english": "English",
    "kannada": "Kannada",
    "hindi": "Hindi",
    "tamil": "Tamil",
    "telugu": "Telugu",
    "malayalam": "Malayalam"
}


# ==================================================
# LOAD TRANSACTIONS
# ==================================================

def load_transactions():

    try:

        with open(TRANSACTION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except:
        return []


# ==================================================
# SAVE TRANSACTIONS
# ==================================================

def save_transactions(data):

    with open(TRANSACTION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ==================================================
# RECENT TRANSACTIONS
# ==================================================

def get_recent_transactions(
    user,
    days=7,
    limit=10,
    language="english"
):

    selected_language = LANGUAGE_MAP.get(
        language.lower(),
        "English"
    )

    data = load_transactions()

    now = datetime.now()

    cutoff = now - timedelta(days=days)

    filtered = []

    for txn in data:

        if txn.get("user") != user:
            continue

        try:

            txn_date = datetime.strptime(
                txn["date"],
                "%Y-%m-%d %H:%M:%S"
            )

            if txn_date >= cutoff:
                filtered.append(txn)

        except:
            continue

    filtered.sort(
        key=lambda x: x["date"],
        reverse=True
    )

    # ==================================================
    # NO TRANSACTIONS
    # ==================================================

    if not filtered:

        response = llm.invoke(f"""
You are a professional multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Keep response short
- Professional banking tone

No transactions found for user:
{user}

Time Range:
Last {days} days

Generate customer-friendly banking response.
""")

        return {
            "response": response.content,
            "status": "empty",
            "language": selected_language,
            "timestamp": str(datetime.now())
        }

    # ==================================================
    # ANALYSIS
    # ==================================================

    response = llm.invoke(f"""
You are a multilingual banking analytics AI.

IMPORTANT:
- Respond ONLY in {selected_language}
- Professional banking style
- Short and clear response
- Use bullet points

Analyze transactions:
{filtered[:limit]}

Generate:
- transaction summary
- spending pattern
- financial insights
- customer advice
""")

    return {
        "response": response.content,
        "status": "success",
        "language": selected_language,
        "timestamp": str(datetime.now())
    }


# ==================================================
# MONTHLY SUMMARY
# ==================================================

def monthly_summary(user, language="english"):

    selected_language = LANGUAGE_MAP.get(
        language.lower(),
        "English"
    )

    data = load_transactions()

    now = datetime.now()

    total = 0
    count = 0

    for txn in data:

        if txn.get("user") != user:
            continue

        try:

            t = datetime.strptime(
                txn["date"],
                "%Y-%m-%d %H:%M:%S"
            )

            if t.month == now.month and t.year == now.year:

                total += txn["amount"]
                count += 1

        except:
            continue

    avg = total / count if count else 0

    response = llm.invoke(f"""
You are a multilingual banking financial advisor AI.

IMPORTANT:
- Respond ONLY in {selected_language}
- Keep response professional
- Short and practical

Monthly Financial Summary:

Transactions: {count}
Total Spent: ₹{total}
Average Spending: ₹{avg:.2f}

Generate:
- spending insights
- budgeting tips
- savings advice
- financial recommendation
""")

    return {
        "response": response.content,
        "status": "success",
        "language": selected_language,
        "timestamp": str(datetime.now())
    }


# ==================================================
# CATEGORY SUMMARY
# ==================================================

def category_summary(user, language="english"):

    selected_language = LANGUAGE_MAP.get(
        language.lower(),
        "English"
    )

    data = load_transactions()

    cat = defaultdict(int)

    for txn in data:

        if txn.get("user") == user:
            cat[txn["to"]] += txn["amount"]

    # ==================================================
    # EMPTY DATA
    # ==================================================

    if not cat:

        response = llm.invoke(f"""
You are a multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Keep response short
- Professional banking style

No spending data found.

Generate customer-friendly response.
""")

        return {
            "response": response.content,
            "status": "empty",
            "language": selected_language,
            "timestamp": str(datetime.now())
        }

    # ==================================================
    # CATEGORY ANALYSIS
    # ==================================================

    response = llm.invoke(f"""
You are a multilingual banking analytics AI.

IMPORTANT:
- Respond ONLY in {selected_language}
- Professional banking tone
- Use bullet points
- Keep response concise

Analyze category spending:
{dict(cat)}

Generate:
- top spending category
- spending insights
- savings recommendations
""")

    return {
        "response": response.content,
        "status": "success",
        "language": selected_language,
        "timestamp": str(datetime.now())
    }


# ==================================================
# ADD TRANSACTION
# ==================================================

def add_transaction(
    user,
    to,
    amount,
    language="english"
):

    selected_language = LANGUAGE_MAP.get(
        language.lower(),
        "English"
    )

    data = load_transactions()

    data.append({
        "user": user,
        "to": to,
        "amount": amount,
        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    })

    save_transactions(data)

    response = llm.invoke(f"""
You are a multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Professional banking style
- Keep response short
- Customer friendly

Transaction Successful:

User: {user}
To: {to}
Amount: ₹{amount}

Generate clean confirmation message.
""")

    return {
        "response": response.content,
        "status": "success",
        "language": selected_language,
        "timestamp": str(datetime.now())
    }


# ==================================================
# SPENDING INSIGHTS
# ==================================================

def spending_insights(user, language="english"):

    selected_language = LANGUAGE_MAP.get(
        language.lower(),
        "English"
    )

    data = load_transactions()

    user_txns = [
        t for t in data
        if t.get("user") == user
    ]

    # ==================================================
    # EMPTY HISTORY
    # ==================================================

    if not user_txns:

        response = llm.invoke(f"""
You are a multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Professional banking tone
- Keep response short

No transaction history found.

Generate customer-friendly response.
""")

        return {
            "response": response.content,
            "status": "empty",
            "language": selected_language,
            "timestamp": str(datetime.now())
        }

    # ==================================================
    # INSIGHTS
    # ==================================================

    response = llm.invoke(f"""
You are a multilingual banking analytics AI.

IMPORTANT:
- Respond ONLY in {selected_language}
- Professional banking style
- Keep response concise
- Use bullet points

Analyze spending behavior:
{user_txns[-10:]}

Generate:
- spending habits
- unusual activity
- savings suggestions
- budgeting insights
""")

    return {
        "response": response.content,
        "status": "success",
        "language": selected_language,
        "timestamp": str(datetime.now())
    }