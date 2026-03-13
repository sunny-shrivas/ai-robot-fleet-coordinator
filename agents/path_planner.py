from crewai import Agent

path_planner = Agent(
    role="Robot Navigation Planner",
    goal="Generate safe and shortest paths avoiding dynamic obstacles",
    backstory=(
        "You specialize in robotic navigation systems similar to ROS2 Nav2 stack. "
        "You ensure efficient motion planning."
    ),
    verbose=True
)
