import json
from typing import List, Tuple
from ..models.task import Task
from ..models.agent import Agent

class InputHandler:
    """Handles loading scenarios from files"""
    
    @staticmethod
    def load_from_json(filepath: str) -> Tuple[List[Task], List[Agent]]:
        """Load tasks and agents from JSON file"""
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
            
            tasks = [Task(**task_data) for task_data in data.get('tasks', [])]
            agents = [Agent(**agent_data) for agent_data in data.get('agents', [])]
            
            return tasks, agents
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return [], []
    
    @staticmethod
    def create_sample_scenario() -> Tuple[List[Task], List[Agent]]:
        """Create a sample scenario for testing"""
        tasks = [
            Task("T1", 3, [], ["skill_A"]),
            Task("T2", 2, [], ["skill_B"]),
            Task("T3", 4, ["T1"], ["skill_A"]),
            Task("T4", 1, ["T2"], ["skill_C"]),
            Task("T5", 3, ["T1", "T2"], ["skill_B"]),
            Task("T6", 2, ["T3", "T4"], ["skill_A"]),
            Task("T7", 1, ["T5"], ["skill_C"]),
            Task("T8", 2, ["T6", "T7"], ["skill_B"])
        ]
        
        agents = [
            Agent("A1", ["skill_A", "skill_B"]),
            Agent("A2", ["skill_B", "skill_C"]),
            Agent("A3", ["skill_A", "skill_C"])
        ]
        
        return tasks, agents
