from google import genai

from app.config import settings


class LLMService:

    def __init__(self):
        self.client = None

    def _get_client(self):
        if not settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. "
                "Add your Gemini API key to the .env file."
            )

        if self.client is None:
            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )

        return self.client

    def generate_response(self, prompt: str) -> str:

        client = self._get_client()

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text.strip()


llm_service = LLMService()