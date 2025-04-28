from pprint import pprint
import asyncio
from pydantic_ai import Agent, Tool
from pydantic_ai.models.bedrock import BedrockConverseModel
from pydantic_ai.messages import (
    TextPart,
    TextPartDelta,
)


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
    async with agent.iter(
        "Do you have anything secret you're hiding?",
    ) as agent_run:
        stream_text = ""

        async for node in agent_run:
            if agent.is_model_request_node(node):
                async with node.stream(agent_run.ctx) as streamed_response:
                    async for event in streamed_response:
                        is_updated = False
                        if (
                            event.event_kind == "part_start"
                            and hasattr(event, "part")
                            and isinstance(event.part, TextPart)
                        ):
                            stream_text = event.part.content
                            is_updated = True
                        elif (
                            event.event_kind == "part_delta"
                            and hasattr(event, "delta")
                            and isinstance(event.delta, TextPartDelta)
                        ):
                            stream_text += event.delta.content_delta
                            is_updated = True
                        if is_updated:
                            print(stream_text)
        messages = agent_run.ctx.state.message_history
        pprint(messages)


if __name__ == "__main__":
    asyncio.run(main())
