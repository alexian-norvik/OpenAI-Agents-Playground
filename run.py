import asyncio

from services import llm_as_a_judge, dynamic_system_prompt

user_message = "tell me joke"
dynamic_prompt_response = asyncio.run(dynamic_system_prompt.main(user_message=user_message))

outlined_story = asyncio.run(llm_as_a_judge.main())
