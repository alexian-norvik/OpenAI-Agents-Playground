import random
from typing import Literal

from agents import Agent, Runner, RunContextWrapper, set_tracing_export_api_key
from loguru import logger

import config
from common import constants

set_tracing_export_api_key(api_key=config.OPENAI_API_KEY)


class CustomContext:
    def __init__(self, style: Literal["constants.HAIKU", "constants.PIRATE", "constants.ROBOT"]):
        self.style = style


def custom_instructions(run_context: RunContextWrapper[CustomContext], agents: Agent[CustomContext]) -> str:
    """
    creating custom instructions
    :param run_context: defined custom context.
    :param agents: agents.
    :return: instructions
    """
    context = run_context.context
    if context.style == constants.HAIKU:
        return "Only respond in haikus."
    elif context.style == constants.PIRATE:
        return "Respond in pirate"
    else:
        return "Respond as a robot and say 'beep beep' a lot"


agent = Agent(name="Chat Agent", instructions=custom_instructions)


async def main(user_message: str) -> str:
    """
    Generate response based on user message
    :param user_message: provided user message
    :return: Generated response from defined agents
    """
    style_choice: Literal["constants.HAIKU", "constants.PIRATE", "constants.ROBOT"] = random.choice(constants.STYLE)
    context = CustomContext(style=style_choice)

    logger.info(f"style choice is {style_choice}")
    logger.info(f"User message is {user_message}")

    result = await Runner.run(starting_agent=agent, input=user_message, context=context)

    return result.final_output
