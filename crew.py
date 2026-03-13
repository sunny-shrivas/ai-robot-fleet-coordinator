from crewai import Crew, Task

from agents.task_manager import task_manager
from agents.path_planner import path_planner
from agents.battery_monitor import battery_monitor
from agents.mission_executor import mission_executor


task_allocation = Task(
    description="Analyze robot fleet and assign a delivery mission to the best available robot.",
    agent=task_manager,
    expected_output="Robot ID selected and mission assigned."
)

path_planning = Task(
    description="Plan a safe and shortest navigation path for the robot to reach the delivery location.",
    agent=path_planner,
    expected_output="Step-by-step navigation path."
)

battery_check = Task(
    description="Verify robot battery status before mission execution and recommend charging if required.",
    agent=battery_monitor,
    expected_output="Battery status confirmation."
)

mission_execution = Task(
    description="Execute the assigned delivery mission and report mission completion.",
    agent=mission_executor,
    expected_output="Mission success report."
)


fleet_crew = Crew(
    agents=[
        task_manager,
        path_planner,
        battery_monitor,
        mission_executor
    ],
    tasks=[
        task_allocation,
        path_planning,
        battery_check,
        mission_execution
    ],
    verbose=True
)
