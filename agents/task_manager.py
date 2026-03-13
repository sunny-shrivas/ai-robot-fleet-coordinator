from crewai import Agent

task_manager = Agent(
    role="Fleet Task Manager",
    goal="Assign optimal delivery and navigation tasks to available robots",
    backstory=(
        "You are an intelligent fleet coordination expert working in a smart warehouse. "
        "You analyze robot availability, workload, and mission priorities."
    ),
    verbose=True
)
