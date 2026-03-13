from crewai import Agent

mission_executor = Agent(
    role="Mission Execution Controller",
    goal="Execute assigned missions and confirm successful completion",
    backstory=(
        "You control industrial autonomous robots and ensure task completion."
    ),
    verbose=True
)
