from typing import Literal
from dataclasses import dataclass

from agents import (
    Agent,
    Runner,
    ItemHelpers,
    TResponseInputItem,
    trace,
    set_tracing_export_api_key,
)
from loguru import logger

import config
from common import llms_constants

set_tracing_export_api_key(api_key=config.OPENAI_API_KEY)
"""
This example shows the LLM as a judge pattern. The first agent generates an outline for a story.
The second agent judges the outline and provides feedback.
We loop until the judge is satisfied with the outline.
"""

story_generator = Agent(name="Story Generator", instructions=llms_constants.STORY_GENERATOR_SYSTEM_PROMPT)


@dataclass
class EvaluationFeedback:
    score: Literal["pass", "needs_improvements", "fail"]
    feedback: str


evaluator = Agent(name="Evaluator", instructions=llms_constants.EVALUATOR_SYSTEM_PROMPT, output_type=EvaluationFeedback)


async def main():
    msg = input("What kind of story would you like to hear? ")
    input_items: list[TResponseInputItem] = [{"content": msg, "role": "user"}]

    latest_outline: str | None = None

    with trace("LLM as a judge"):
        while True:
            story_outline_result = await Runner.run(starting_agent=story_generator, input=input_items)
            input_items = story_outline_result.to_input_list()
            latest_outline = ItemHelpers.text_message_outputs(story_outline_result.new_items)

            logger.info("Story outline generated.")

            evaluator_result = await Runner.run(starting_agent=evaluator, input=input_items)
            result: EvaluationFeedback = evaluator_result.final_output

            logger.info(f"Evaluator score: {result.score}")

            if result.score == "pass":
                logger.info("Story outline is good enough, exiting.")
                break

            logger.info("Rerunning with feedback.")

            input_items.append({"content": f"Feedback: {result.feedback}", "role": "user"})

    return f"Final story outline: {latest_outline}"
