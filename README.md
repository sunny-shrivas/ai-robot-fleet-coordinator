# 🤖 AI Robot Fleet Coordinator (Multi-Agent System)

An intelligent **robot fleet coordination system** built using **CrewAI** that simulates real-world Autonomous Mobile Robot (AMR) decision making.

This project demonstrates how multiple AI agents collaborate to:

* Allocate missions
* Plan robot navigation paths
* Monitor battery intelligence
* Execute delivery missions

Inspired by real industrial robotics fleet orchestration systems.

---

## 🚀 Project Motivation

Modern warehouses and factories deploy fleets of Autonomous Mobile Robots (AMRs).
Efficient coordination requires intelligent decision-making across multiple subsystems.

This project explores **multi-agent AI orchestration** for robotics fleet management using CrewAI.

---

## 🧠 System Architecture

Fleet Coordination Flow:

```
Mission Request
     ↓
Task Manager Agent
     ↓
Path Planner Agent
     ↓
Battery Monitor Agent
     ↓
Mission Execution Agent
     ↓
Mission Completion Report
```

---

## 🤖 Agents Overview

### 🔹 Fleet Task Manager

* Assigns optimal mission to available robot
* Considers workload and availability

### 🔹 Navigation Planner

* Generates safe and shortest paths
* Inspired by ROS2 Nav2 planning stack

### 🔹 Battery Intelligence Agent

* Predicts mission feasibility based on power levels
* Prevents mid-mission failures

### 🔹 Mission Execution Controller

* Executes delivery mission
* Confirms successful completion

---

## ⚙️ Tech Stack

* CrewAI (Multi-Agent Orchestration)
* Python
* LLM-Driven Reasoning
* Robotics Fleet Coordination Concepts

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your_api_key"
python3 main.py
```

---

## 📊 Future Enhancements

* ROS2 Navigation Stack Integration
* Real Robot Telemetry Input
* Dynamic Task Reallocation
* Web Dashboard for Fleet Monitoring
* Reinforcement Learning for Mission Optimization
* Multi-Robot Simulation using Gazebo / Isaac Sim

---

## 🎯 Engineering Value

This project demonstrates:

✅ Multi-Agent System Design
✅ AI Decision Orchestration
✅ Robotics Fleet Thinking
✅ System Architecture Skills
✅ Production-Mindset Repository Structuring

---

## 👨‍💻 Author

Sunny Shrivas
AI Engineer | Robotics Enthusiast | Autonomous Systems Developer
