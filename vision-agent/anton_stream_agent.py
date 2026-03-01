from vision_agents.core import Agent
from vision_agents.core.processors.base_processor import Processor

class AntonProcessor(Processor):

    @property
    def name(self):
        return "anton-vision-processor"

    async def close(self):
        pass

    async def on_video(self, frame):
        return {"text": "ANTON processing frame"}

agent = Agent(
    instructions="You are ANTON, a military-grade reconnaissance AI.",
    processors=[AntonProcessor()]
)