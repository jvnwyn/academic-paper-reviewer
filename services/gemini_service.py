from google import genai
from google.genai import types

from config import Config


class GeminiServiceError(Exception):
    """Raised when Gemini cannot generate an answer."""


_client: genai.Client | None = None


def get_gemini_client() -> genai.Client:
    global _client

    if not Config.GEMINI_API_KEY:
        raise GeminiServiceError(
            "Gemini is not configured. Add GEMINI_API_KEY to your .env file."
        )

    if _client is None:
        _client = genai.Client(api_key=Config.GEMINI_API_KEY)

    return _client


def generate_answer(question: str, context: str) -> str:
    """Generate a document-grounded answer from retrieved context only."""
    client = get_gemini_client()

    prompt = f"""Answer the question using only the retrieved paper excerpts.

Rules:
- Do not use outside knowledge.
- If the excerpts do not contain the answer, say so clearly.
- Give a concise, direct answer.
- Cite supporting pages in this format: [Page N].
- Do not invent citations.
- Answer the question as helpfully as possible using the information available in the excerpts.
- Do not mention that excerpts are incomplete, cut off, or partial unless the user specifically asks about missing or incomplete information.
- Write the answer in plain text. Do not use Markdown bullets, asterisks, headings, or bold formatting.
Question:
{question}

Retrieved paper excerpts:
{context}
"""

    try:
        response = client.models.generate_content(
            model=Config.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=1000,
                thinking_config=types.ThinkingConfig(
                    thinking_level="low",
                ),
            ),
        )
    except Exception as error:
        error_text = str(error)

        if "RESOURCE_EXHAUSTED" in error_text or "429" in error_text:
            raise GeminiServiceError(
                "Gemini request limit reached. Please wait a bit and try again, or use a different Gemini model/API key."
            ) from error

        raise GeminiServiceError(
            f"Gemini could not generate an answer: {error}"
        ) from error

    answer = (response.text or "").strip()

    if not answer:
        raise GeminiServiceError("Gemini returned an empty answer.")

    return answer