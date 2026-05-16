import json
from utils.llm import llm
from datetime import datetime


def account_details(user_id, language="english"):

    # ================= LOAD DATA ================= #

    with open("data/users.json", "r", encoding="utf-8") as f:
        users = json.load(f)

    # ================= LANGUAGE PROMPTS ================= #

    language_map = {
        "english": "English",
        "kannada": "Kannada",
        "hindi": "Hindi",
        "tamil": "Tamil",
        "telugu": "Telugu",
        "malayalam": "Malayalam"
    }

    selected_language = language_map.get(language.lower(), "English")

    # ================= USER NOT FOUND ================= #

    if user_id not in users:

        prompt = f"""
You are a professional multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Keep response professional and customer friendly
- Banking tone only

User requested account details for:
{user_id}

The account does NOT exist.

Generate response including:
- account not found
- ask customer to verify account ID
- polite banking assistance message
- short response
"""

        response = llm.invoke(prompt)

        return {
            "response": response.content,
            "status": "failed",
            "language": selected_language,
            "timestamp": str(datetime.now())
        }

    # ================= USER FOUND ================= #

    user_data = users[user_id]

    prompt = f"""
You are a professional multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Keep response professional
- Banking style response
- Use emojis minimally

User Account Data:
{json.dumps(user_data, indent=2)}

Generate a clean banking response including:
- account holder name
- account number
- account type
- available balance
- account status
- short customer-friendly summary

Keep formatting clean and readable.
"""

    response = llm.invoke(prompt)

    return {
        "response": response.content,
        "status": "success",
        "language": selected_language,
        "timestamp": str(datetime.now())
    }