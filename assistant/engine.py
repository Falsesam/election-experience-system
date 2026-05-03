from assistant.data import ELECTION_KNOWLEDGE
import os

# ---------------------------
# 🔐 Optional: Load env (if using .env locally)
# ---------------------------
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ---------------------------
# 🌐 Google AI Setup (SAFE)
# ---------------------------
try:
    import google.generativeai as genai

    API_KEY = os.getenv("GOOGLE_API_KEY")

    if API_KEY:
        genai.configure(api_key=API_KEY)
        GOOGLE_AVAILABLE = True
    else:
        GOOGLE_AVAILABLE = False

except ImportError:
    GOOGLE_AVAILABLE = False


def normalize(word: str) -> str:
    """Normalize keywords for better matching"""
    return word.rstrip("ing").rstrip("ed").rstrip("s")


def google_fallback(query: str) -> str:
    """
    Use Google Generative AI as fallback if no keyword match is found.
    """
    if not GOOGLE_AVAILABLE:
        return None

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(query)
        return response.text
    except Exception:
        return None


def process_query(user_query: str) -> str:
    """
    Process user query and return the most relevant election information.
    Uses keyword scoring with normalization and optional Google fallback.
    """

    user_query = user_query.lower().strip()

    # 🔥 Priority handling
    if "count" in user_query or "counted" in user_query:
        for item in ELECTION_KNOWLEDGE:
            if item["topic"] == "counting":
                return item["content"]

    best_match = None
    max_score = 0

    # 🔍 Keyword matching
    for item in ELECTION_KNOWLEDGE:
        score = 0

        for keyword in item["keywords"]:
            norm = normalize(keyword)

            if keyword in user_query:
                score += 2
            elif norm in user_query:
                score += 1
            elif f"{keyword}ed" in user_query:
                score += 1

        if score > max_score:
            max_score = score
            best_match = item

    # ✅ Return match
    if best_match and max_score > 0:
        return best_match["content"]

    # 🌐 Google fallback
    fallback = google_fallback(user_query)
    if fallback:
        return fallback

    # ❌ Default response
    return (
        "I couldn't find relevant information. "
        "Please ask about registration, voting, counting, or results."
    )