from pprint import pprint
import asyncio
from pydantic_ai import Agent, Tool
from pydantic_ai.models.bedrock import BedrockConverseModel


# Not a helpful tool, but illustrates the problem
def get_the_super_secret_info() -> str:
    """Retrieve the super secret info."""
    return "six times seven is 42"


system_prompt = """
Act as a helpful chat agent.

When the user asks if you're hiding information, call the `get_the_super_secret_info` to reveal the information.
""".strip()

agent = Agent(
    model=BedrockConverseModel(
        "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    ),
    system_prompt=system_prompt,
    tools=[Tool(get_the_super_secret_info, takes_ctx=False)],
    output_retries=3,
    output_type=str,
)


async def main():
    async with agent.run_stream(
        "Do you have anything secret you're hiding?",
    ) as response:
        async for output in response.stream():
            print(output)

    messages = response.new_messages()
    pprint(messages)


if __name__ == "__main__":
    asyncio.run(main())
