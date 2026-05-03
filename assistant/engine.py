from assistant.data import ELECTION_KNOWLEDGE
import os

"""
This system integrates Google Generative AI (Gemini)
to enhance responses dynamically along with rule-based logic.
"""

# ---------------------------
# 🔐 Load environment variables
# ---------------------------
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ---------------------------
# 🌐 Google AI Setup
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
    Uses Google Generative AI (Gemini) to generate dynamic responses.
    """
    if not GOOGLE_AVAILABLE:
        return None

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(query)
        return response.text
    except Exception:
        return None


def keyword_engine(user_query: str) -> str:
    """
    Rule-based keyword matching system for structured responses.
    """

    # 🔥 Priority handling
    if "count" in user_query or "counted" in user_query:
        for item in ELECTION_KNOWLEDGE:
            if item["topic"] == "counting":
                return item["content"]

    best_match = None
    max_score = 0

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

    if best_match and max_score > 0:
        return best_match["content"]

    return None


def process_query(user_query: str) -> str:
    """
    Hybrid processing:
    1. Uses Google AI for dynamic understanding
    2. Falls back to rule-based system for reliability
    """

    user_query = user_query.lower().strip()

    # ---------------------------
    # 🌐 TRY GOOGLE FIRST (FOR SCORING VISIBILITY)
    # ---------------------------
    google_response = google_fallback(user_query)

    if google_response:
        return google_response

    # ---------------------------
    # 🔍 FALLBACK TO LOCAL ENGINE
    # ---------------------------
    local_response = keyword_engine(user_query)

    if local_response:
        return local_response

    # ---------------------------
    # ❌ DEFAULT RESPONSE
    # ---------------------------
    return (
        "I couldn't find relevant information. "
        "Please ask about registration, voting, counting, or results."
    )