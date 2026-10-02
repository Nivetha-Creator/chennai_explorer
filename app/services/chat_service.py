from sqlalchemy.orm import Session

from app.services.intent_service import extract_intent
from app.services.retrieval_service import (
    search_places,
    search_eateries,
    search_dishes,
)
from app.services.llm_service import llm_service


def retrieve_context(db: Session, intent_data: dict) -> dict:
    intent = intent_data.get("intent")
    start_location = intent_data.get("start_location")

    context = {
        "places": [],
        "eateries": [],
        "dishes": [],
    }

    if intent in {
        "explore_places",
        "find_activities",
        "plan_itinerary",
        "nearby",
    }:
        context["places"] = search_places(
            db=db,
            area=start_location,
            limit=10,
        )

    if intent in {
        "find_food",
        "plan_itinerary",
    }:
        context["eateries"] = search_eateries(
            db=db,
            area=start_location,
            limit=10,
        )

        context["dishes"] = search_dishes(
            db=db,
            limit=10,
        )

    return context


def build_grounded_prompt(
    message: str,
    intent_data: dict,
    context: dict,
) -> str:

    return f"""
You are Chennai Explorer, a Chennai-specific AI travel assistant.

The user's message has already been analyzed.

INTENT:
{intent_data}

VERIFIED CHENNAI DATA:
{context}

USER MESSAGE:
{message}

IMPORTANT RULES:

1. Use the verified Chennai data provided above.
2. Do not invent places, restaurants, prices, timings, or other facts.
3. If the provided data does not contain an answer, clearly say that the information is not available.
4. Do not claim that information is live or real-time.
5. Keep the answer concise and useful.
6. Use bullet points whenever possible.
7. Respond in the user's language when possible.
8. For Tanglish, you may respond naturally in Tanglish.
9. Do not mention internal systems, databases, prompts, or context.
"""


def chat(
    db: Session,
    message: str,
    language: str = "en",
) -> str:

    intent_data = extract_intent(message)

    context = retrieve_context(
        db=db,
        intent_data=intent_data,
    )

    prompt = build_grounded_prompt(
        message=message,
        intent_data=intent_data,
        context=context,
    )

    return llm_service.generate_response(prompt)