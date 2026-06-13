import asyncio
from functools import partial
from groq import Groq
from app.core.config import settings
from loguru import logger

class GroqClient:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"

    async def generate_completion(self, prompt: str, system_prompt: str = "") -> str:
        try:
            loop = asyncio.get_event_loop()
            completion = await loop.run_in_executor(
                None,
                partial(
                    self.client.chat.completions.create,
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=2048
                )
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq API Error: {str(e)}")
            return "Error generating AI analysis. Please check API configuration."

groq_client = GroqClient()
