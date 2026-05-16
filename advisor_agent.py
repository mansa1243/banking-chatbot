from utils.llm import llm
from datetime import datetime


def financial_advice(query, language="english"):

    # ================= LANGUAGE SUPPORT ================= #

    language_map = {
        "english": "English",
        "kannada": "Kannada",
        "hindi": "Hindi",
        "tamil": "Tamil",
        "telugu": "Telugu",
        "malayalam": "Malayalam"
    }

    selected_language = language_map.get(language.lower(), "English")

    # ================= PROMPT ================= #

    prompt = f"""
You are a professional multilingual AI financial advisor working in a banking system.

IMPORTANT:
- Respond ONLY in {selected_language}
- Keep response short and practical
- Use professional banking tone
- Use bullet points
- Give easy-to-understand advice
- Use emojis minimally

User Question:
{query}

Your responsibilities:
- Give simple financial advice
- Provide budgeting tips
- Suggest savings strategies
- Recommend safe investment ideas
- Help with spending optimization

Rules:
- Avoid long explanations
- Focus on actionable advice
- Keep response customer friendly
"""

    response = llm.invoke(prompt)

    return {
        "response": response.content,
        "status": "success",
        "language": selected_language,
        "timestamp": str(datetime.now())
    }