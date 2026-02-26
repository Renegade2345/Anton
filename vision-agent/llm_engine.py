import os
from dotenv import load_dotenv
from openai import OpenAI
from openai import RateLimitError, OpenAIError

load_dotenv()


class LLMEngine:

    def __init__(self):

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            print("LLM disabled — No API key found.")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)

    def analyze(self, tracked_objects, events, threat_levels):

        if not self.client:
            return None

        if not events:
            return None

        try:

            summary = []

            for event in events:
                obj_id = event.get("id", "unknown")
                threat = threat_levels.get(obj_id, "LOW")
                label = event.get("label", "object")

                summary.append(
                    f"{label} with threat level {threat} triggered event {event['event']}"
                )

            prompt = f"""
You are ANTON, a military-grade reconnaissance AI.

Analyze the following surveillance intelligence events and produce a short threat assessment.

Events:
{summary}

Output a concise tactical assessment.
"""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=120
            )

            return response.choices[0].message.content

        except RateLimitError:
            print("LLM quota exceeded — continuing without LLM.")
            return None

        except OpenAIError:
            print("LLM error — continuing without LLM.")
            return None