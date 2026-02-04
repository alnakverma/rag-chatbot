import os
from dotenv import load_dotenv
from google import genai


# Load environment variables (.env)
load_dotenv()


# Create Gemini client once
# (reuse connection for speed)
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Intent Classification Function
def classify_intent(query: str) -> str:
    """
    Classifies user query into one of:
    - HR_POLICY
    - GENERAL_CHAT

    Uses:
    - Few-shot prompting
    - Low temperature (deterministic)
    - Output normalization
    - Safety fallback

    Returns: string intent
    """


    # Few-shot prompt
    prompt = f"""
You are an INTENT CLASSIFIER.

Your job:
Classify the user query into ONLY ONE of these labels:

HR_POLICY
GENERAL_CHAT


Rules:
If question is about:
- leave
- benefits
- policy
- insurance
- office timings
- office hours
- employees
- HR rules

→ HR_POLICY

Otherwise → GENERAL_CHAT


Examples:

Office timings please → HR_POLICY
How many annual leave → HR_POLICY
Maternity leave duration → HR_POLICY
Medical insurance available → HR_POLICY

Hi → GENERAL_CHAT
Tell me a joke → GENERAL_CHAT
What is AI → GENERAL_CHAT


Return ONLY the label.
No explanation.

Sentence: {query}
"""


    # Call Gemini
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config={
            "temperature": 0,          # deterministic output
            "max_output_tokens": 1000     # only small answer needed
        }
    )


    # Safety checks (very important)
    if not response or not response.text:
        print("Intent model returned empty → default GENERAL_CHAT")
        return "GENERAL_CHAT"


    # normalize text
    raw_intent = response.text.strip().upper()

    print("Raw model output:", raw_intent)


    # Mapping (CRITICAL)
    # Handles cases like:
    # HR, HR POLICY, Hr_policy, etc.
    if "HR" in raw_intent:
        return "HR_POLICY"

    return "GENERAL_CHAT"
