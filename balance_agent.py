import json
from utils.llm import llm
from datetime import datetime


def check_balance(user, language="english"):

    try:

        # ================= LOAD DATA ================= #

        with open("data/users.json", "r", encoding="utf-8") as f:
            users = json.load(f)

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

        # ================= USER NOT FOUND ================= #

        if user not in users:

            prompt = f"""
You are a professional multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Keep response short
- Professional banking tone
- Customer friendly

User requested balance check for:
{user}

The account does NOT exist.

Generate response including:
- account not found
- ask user to verify account ID
- polite assistance message
"""

            response = llm.invoke(prompt)

            return {
                "response": response.content,
                "status": "failed",
                "language": selected_language,
                "timestamp": str(datetime.now())
            }

        # ================= USER FOUND ================= #

        data = users[user]

        prompt = f"""
You are a professional multilingual banking assistant.

IMPORTANT:
- Respond ONLY in {selected_language}
- Professional banking style
- Keep response short and clean
- Use emojis minimally

Customer Details:
Name: {data['name']}
Balance: ₹{data['balance']}

Generate response including:
- customer name
- available balance
- account status
- short friendly banking message

Format response professionally.
"""

        response = llm.invoke(prompt)

        return {
            "response": response.content,
            "status": "success",
            "language": selected_language,
            "timestamp": str(datetime.now())
        }

    except Exception as e:

        prompt = f"""
You are a multilingual banking error assistant.

IMPORTANT:
- Respond in simple professional English
- Keep message short

System Error:
{str(e)}

Generate a professional banking error message.
"""

        response = llm.invoke(prompt)

        return {
            "response": response.content,
            "status": "error",
            "timestamp": str(datetime.now())
        }