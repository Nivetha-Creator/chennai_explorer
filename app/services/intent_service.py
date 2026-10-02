import json
import re

from app.services.llm_service import llm_service


INTENT_PROMPT = """
You are the intent extraction engine for Chennai Explorer.

Chennai Explorer is an AI travel assistant focused specifically on Chennai, Tamil Nadu.

Your job is to understand the user's message and convert it into structured JSON.

Supported intents:

- explore_places
- find_food
- find_activities
- plan_itinerary
- check_budget
- nearby
- get_directions
- general_chennai

Extract these fields when available:

intent
start_location
destination
day
duration
group_type
budget_inr
interests
transport_preference
language

Rules:

1. Return ONLY valid JSON.
2. Do not add markdown.
3. Do not add explanations.
4. Use null when information is missing.
5. budget_inr must be a number, not a string.
6. interests must always be an array.
7. Detect English, Tamil, or Tanglish.
8. Normalize locations to common English names when possible.
   Example:
   "தாம்பரம்" -> "Tambaram"
   "தாம்பரத்துல" -> "Tambaram"
   "மெரினா" -> "Marina Beach"
9. If the user asks for a trip/plan/itinerary, use plan_itinerary.
10. If the user asks about food/restaurants/dishes, use find_food.
11. If the user asks about places to visit, use explore_places.
12. If the user asks about activities, use find_activities.
13. If the user asks how much a trip may cost, use check_budget.
14. If the user asks what is nearby, use nearby.
15. If the user asks how to travel from one place to another, use get_directions.
16. Otherwise use general_chennai.

Example:

User:
Tambaram la irundhu Saturday friends oda beach and food poganum budget 1000

JSON:
{
  "intent": "plan_itinerary",
  "start_location": "Tambaram",
  "destination": null,
  "day": "Saturday",
  "duration": null,
  "group_type": "friends",
  "budget_inr": 1000,
  "interests": ["beaches", "food"],
  "transport_preference": null,
  "language": "tanglish"
}

Example:

User:
Mylapore la enna places iruku?

JSON:
{
  "intent": "explore_places",
  "start_location": "Mylapore",
  "destination": null,
  "day": null,
  "duration": null,
  "group_type": null,
  "budget_inr": null,
  "interests": ["places"],
  "transport_preference": null,
  "language": "tanglish"
}

Example:

User:
What food should I try in Chennai?

JSON:
{
  "intent": "find_food",
  "start_location": null,
  "destination": null,
  "day": null,
  "duration": null,
  "group_type": null,
  "budget_inr": null,
  "interests": ["food"],
  "transport_preference": null,
  "language": "en"
}
"""


def _extract_json(text: str) -> dict:
    """
    Extract JSON safely from the LLM response.
    """

    text = text.strip()

    # Remove markdown code fences if Gemini adds them.
    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
        flags=re.IGNORECASE,
    )

    return json.loads(text)


def detect_language(message: str) -> str:
    """
    Basic language detection.

    This is only a hint.
    The LLM performs the actual intent extraction.
    """

    tamil_characters = re.findall(
        r"[\u0B80-\u0BFF]",
        message,
    )

    if tamil_characters:
        return "ta"

    tanglish_words = [
        "venum",
        "poganum",
        "iruku",
        "irukku",
        "epdi",
        "enna",
        "inga",
        "anga",
        "la",
        "ku",
        "oda",
        "irundhu",
        "sapda",
        "sapadu",
    ]

    message_lower = message.lower()

    for word in tanglish_words:
        if word in message_lower:
            return "tanglish"

    return "en"


def extract_intent(message: str) -> dict:
    """
    Convert a natural-language user message
    into structured intent data.
    """

    detected_language = detect_language(message)

    prompt = f"""
    {INTENT_PROMPT}

    User language hint:
    {detected_language}

    User message:
    {message}

    Return ONLY valid JSON.
    """

    response = llm_service.generate_response(prompt)

    try:

        result = _extract_json(response)

    except json.JSONDecodeError as error:

        raise ValueError(
            f"Gemini returned invalid JSON: {response}"
        ) from error

    # Make sure required fields always exist.
    result.setdefault(
        "intent",
        "general_chennai",
    )

    result.setdefault(
        "start_location",
        None,
    )

    result.setdefault(
        "destination",
        None,
    )

    result.setdefault(
        "day",
        None,
    )

    result.setdefault(
        "duration",
        None,
    )

    result.setdefault(
        "group_type",
        None,
    )

    result.setdefault(
        "budget_inr",
        None,
    )

    result.setdefault(
        "interests",
        [],
    )

    result.setdefault(
        "transport_preference",
        None,
    )

    result.setdefault(
        "language",
        detected_language,
    )

    return result