import os
import openai
from dotenv import load_dotenv

load_dotenv()


class OpenAIProvider:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_KEY')
        openai.api_key = self.api_key

    def generate_text(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text
