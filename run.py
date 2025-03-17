import asyncio

from dynamic_system_prompt import main

user_message = "tell me joke"
response = asyncio.run(main(user_message=user_message))

print(response)
