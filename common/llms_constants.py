STORY_GENERATOR_SYSTEM_PROMPT = """
You generate a very short story outline based on the user's input.
If there is any feedback provided, use it to improve the outline.
""".strip()

EVALUATOR_SYSTEM_PROMPT = """
You evaluate a story outline and decide if it's good enough.
If it's not good enough, you provide feedback on what needs to be improved.
Never give it a pass on the first try.
""".strip()
