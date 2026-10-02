from app.database.session import SessionLocal
from app.services.intent_service import extract_intent
from app.services.chat_service import retrieve_context


def main():
    message = "Mylapore la enna places iruku?"

    intent_data = extract_intent(message)

    print("\nINTENT:")
    print(intent_data)

    db = SessionLocal()

    try:
        context = retrieve_context(
            db=db,
            intent_data=intent_data,
        )

        print("\nRETRIEVED CONTEXT:")
        print(context)

    finally:
        db.close()


if __name__ == "__main__":
    main()