from crewai import Agent

battery_monitor = Agent(
    role="Robot Battery Intelligence Agent",
    goal="Monitor robot battery levels and recommend charging missions",
    backstory=(
        "You prevent mission failures due to power loss by predicting battery usage."
    ),
    verbose=True
)
