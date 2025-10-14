from datapizza.tools import tool  
from datapizza.agents import Agent
from src import client



@tool(name="get_calendar_events", description="Get calendar events for a given date (ISO or natural language). If no date is provided, defaults to today.")
def get_calendar_events(date: str = "today"):
    """Mock function to get calendar events for a given date."""
    # In a real implementation, this would query a calendar API.
    return f"Events on {date}: Meeting with Bob at 10 AM, Lunch with Alice at 1 PM."

@tool
def add_calendar_event(date, time, event):
    """Mock function to add an event to the calendar."""
    # In a real implementation, this would interact with a calendar API.
    return f"Added event '{event}' on {date} at {time}."

calendar_agent = Agent(
    name="calendar-assistant",
    system_prompt="You are a assistant that knows the user's calendar and can help them manage their schedule.",
    client=client,
    tools=[get_calendar_events, add_calendar_event],

)



