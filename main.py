from crew import fleet_crew

def run_fleet_system():
    print("\n🚀 Starting AI Robot Fleet Coordinator...\n")
    
    result = fleet_crew.kickoff()
    
    print("\n✅ Fleet Mission Result:\n")
    print(result)

if __name__ == "__main__":
    run_fleet_system()
