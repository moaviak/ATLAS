"""
AI-Powered Autonomous Task Scheduler for Multi-Agent Systems
Main Entry Point
"""

import json
import argparse
import os
import sys
from pathlib import Path
from src.task_scheduler import TaskScheduler

DEFAULT_SCENARIO_FILE = "scenarios/default_scenario.json"

def create_default_scenario():
    """Create a default scenario file if it doesn't exist"""
    scenario_data = {
        "tasks": [
            {"task_id": "T1", "duration": 3, "dependencies": [], "required_resources": ["skill_A"]},
            {"task_id": "T2", "duration": 2, "dependencies": [], "required_resources": ["skill_B"]},
            {"task_id": "T3", "duration": 4, "dependencies": ["T1"], "required_resources": ["skill_A"]},
            {"task_id": "T4", "duration": 1, "dependencies": ["T2"], "required_resources": ["skill_C"]},
            {"task_id": "T5", "duration": 3, "dependencies": ["T1", "T2"], "required_resources": ["skill_B"]},
            {"task_id": "T6", "duration": 2, "dependencies": ["T3", "T4"], "required_resources": ["skill_A"]},
            {"task_id": "T7", "duration": 1, "dependencies": ["T5"], "required_resources": ["skill_C"]},
            {"task_id": "T8", "duration": 2, "dependencies": ["T6", "T7"], "required_resources": ["skill_B"]},
            {"task_id": "T9", "duration": 2, "dependencies": ["T3"], "required_resources": ["skill_C"]},
            {"task_id": "T10", "duration": 1, "dependencies": ["T8", "T9"], "required_resources": ["skill_A"]}
        ],
        "agents": [
            {"agent_id": "A1", "skills": ["skill_A", "skill_B"]},
            {"agent_id": "A2", "skills": ["skill_B", "skill_C"]},
            {"agent_id": "A3", "skills": ["skill_A", "skill_C"]},
            {"agent_id": "A4", "skills": ["skill_A", "skill_B", "skill_C"]}
        ]
    }
    
    # Create scenarios directory if it doesn't exist
    os.makedirs(os.path.dirname(DEFAULT_SCENARIO_FILE), exist_ok=True)
    
    with open(DEFAULT_SCENARIO_FILE, 'w') as f:
        json.dump(scenario_data, f, indent=2)
    
    print(f"Default scenario file created at: {DEFAULT_SCENARIO_FILE}")

def validate_scenario_file(file_path: str) -> bool:
    """Validate if the scenario file exists and has the correct format"""
    try:
        if not os.path.exists(file_path):
            print(f"Error: Scenario file not found: {file_path}")
            return False
            
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        # Basic validation of required fields
        if not isinstance(data.get('tasks'), list) or not isinstance(data.get('agents'), list):
            print("Error: Scenario file must contain 'tasks' and 'agents' lists")
            return False
            
        return True
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file: {file_path}")
        return False
    except Exception as e:
        print(f"Error validating scenario file: {str(e)}")
        return False

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='AI-Powered Autonomous Task Scheduler')
    parser.add_argument('--scenario', '-s', type=str, default=DEFAULT_SCENARIO_FILE,
                      help='Path to the scenario JSON file (default: scenarios/default_scenario.json)')
    return parser.parse_args()

def main():
    """Main function to run the task scheduler simulation"""
    args = parse_arguments()
    
    # If default scenario doesn't exist, create it
    if args.scenario == DEFAULT_SCENARIO_FILE and not os.path.exists(DEFAULT_SCENARIO_FILE):
        create_default_scenario()
    
    # Validate scenario file
    if not validate_scenario_file(args.scenario):
        sys.exit(1)
    
    # Initialize and run the scheduler
    scheduler = TaskScheduler()
    scheduler.load_scenario(args.scenario)
    scheduler.solve_csp()
    scheduler.optimize_with_ga()
    scheduler.compare_results()
    scheduler.visualize_schedules()

if __name__ == "__main__":
    main()
