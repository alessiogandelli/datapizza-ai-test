"""
Chatbot Logic
Handles the core chatbot functionality including session management and AI interactions.
"""
from datapizza.memory import Memory
from datapizza.type import ROLE, TextBlock
from datapizza.agents import Agent
from src import client
from src.agent_calendar import calendar_agent


class ChatbotSession:
    """Manages a single chatbot session with memory and agent."""
    
    def __init__(self):
        """Initialize a new chatbot session."""
        self.memory = Memory()
        self.agent = Agent(
            name="studybuddy",
            system_prompt="You are a helpful study assistant for university students.",
            client=client,
            memory=self.memory,
        )
        self.agent.can_call(calendar_agent)
    
    def get_response(self, user_message: str) -> str:
        """
        Get a response from the chatbot for the given user message.
        
        Args:
            user_message: The user's input message
            
        Returns:
            The chatbot's response as a string
        """
        # Get AI response
        response = self.agent.run(user_message)
        
        # Update conversation memory
        self.memory.add_turn(TextBlock(content=user_message), role=ROLE.USER)
        self.memory.add_turn(response.content, role=ROLE.ASSISTANT)
        
        return response.text
    
    def reset(self):
        """Reset the session by creating a new memory and agent."""
        self.__init__()


class ChatbotManager:
    """Manages multiple chatbot sessions (one per user)."""
    
    def __init__(self):
        """Initialize the chatbot manager."""
        self.sessions = {}
    
    def get_session(self, user_id: str) -> ChatbotSession:
        """
        Get or create a session for a user.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            The ChatbotSession for this user
        """
        if user_id not in self.sessions:
            self.sessions[user_id] = ChatbotSession()
        return self.sessions[user_id]
    
    def reset_session(self, user_id: str):
        """
        Reset a user's session.
        
        Args:
            user_id: Unique identifier for the user
        """
        if user_id in self.sessions:
            del self.sessions[user_id]
    
    def get_response(self, user_id: str, message: str) -> str:
        """
        Get a response for a user's message.
        
        Args:
            user_id: Unique identifier for the user
            message: The user's message
            
        Returns:
            The chatbot's response
        """
        session = self.get_session(user_id)
        return session.get_response(message)


def simple_chatbot():
    """Basic chatbot with conversation memory for CLI interaction."""
    session = ChatbotSession()
    
    print("Chatbot: Hello! I'm here to help. Type 'quit' to exit.")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ['quit', 'exit', 'bye', 'adios']:
            print("Chatbot: Goodbye!")
            break

        try:
            response = session.get_response(user_input)
            print(f"Chatbot: {response}")
        except Exception as e:
            print(f"Chatbot: Sorry, I encountered an error: {e}")


if __name__ == "__main__":
    simple_chatbot()