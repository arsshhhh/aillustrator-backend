from pydantic_ai import Agent
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.models.google import GoogleModel
from config import settings

provider = GoogleProvider(api_key=settings.GOOGLE_API_KEY)

model = GoogleModel("gemini-2.5-flash", provider=provider)
agent = Agent(
    model,
    system_prompt="""
    You are a notes generator.
    Always return structured academic notes.
    - Use clear section headings
    - Keep content concise and student-friendly
    """
)
