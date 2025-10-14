from datapizza.memory import Memory
from datapizza.type import ROLE, TextBlock
from datapizza.agents import Agent
from src import client
from src.agent_calendar import calendar_agent







def simple_chatbot():
    """Basic chatbot with conversation memory."""


    memory = Memory()

    studybuddy_agent = Agent(
    name="studybuddy",
    system_prompt="You are a helpful study assistant for university students.",
    client=client,
    memory=memory,
    )

    studybuddy_agent.can_call(calendar_agent)


    print("Chatbot: Hello! I'm here to help. Type 'quit' to exit.")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ['quit', 'exit', 'bye', 'adios']:
            print("Chatbot: Goodbye!")
            break

        # Get AI response with memory context
        response = studybuddy_agent.run(user_input)
        print(f"Chatbot: {response.text}")

        # Update conversation memory
        memory.add_turn(TextBlock(content=user_input), role=ROLE.USER)
        memory.add_turn(response.content, role=ROLE.ASSISTANT)


if __name__ == "__main__":
    simple_chatbot()