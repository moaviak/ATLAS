from dataclasses import dataclass
from typing import List
from .task import Task
from .agent import Agent

@dataclass
class Schedule:
    """Represents a complete schedule"""
    tasks: List[Task]
    agents: List[Agent]
    makespan: int = 0
    
    def calculate_makespan(self) -> int:
        """Calculate the total makespan of the schedule"""
        if not self.tasks or not any(task.start_time is not None for task in self.tasks):
            return 0
        
        max_end_time = 0
        for task in self.tasks:
            if task.start_time is not None:
                end_time = task.start_time + task.duration
                max_end_time = max(max_end_time, end_time)
        
        self.makespan = max_end_time
        return self.makespan
    
    def is_valid(self) -> bool:
        """Check if the schedule satisfies all constraints"""
        # Check if all tasks are assigned
        for task in self.tasks:
            if task.assigned_agent is None or task.start_time is None:
                return False
        
        # Check agent capabilities
        agent_dict = {agent.agent_id: agent for agent in self.agents}
        for task in self.tasks:
            agent = agent_dict.get(task.assigned_agent)
            if not agent or not agent.can_perform_task(task):
                return False
        
        # Check dependency constraints
        task_dict = {task.task_id: task for task in self.tasks}
        for task in self.tasks:
            for dep_id in task.dependencies:
                if dep_id in task_dict:
                    dep_task = task_dict[dep_id]
                    if dep_task.start_time + dep_task.duration > task.start_time:
                        return False
        
        # Check agent availability conflicts
        agent_schedules = {}
        for task in self.tasks:
            agent_id = task.assigned_agent
            if agent_id not in agent_schedules:
                agent_schedules[agent_id] = []
            agent_schedules[agent_id].append((task.start_time, task.start_time + task.duration))
        
        for agent_id, time_slots in agent_schedules.items():
            time_slots.sort()
            for i in range(len(time_slots) - 1):
                if time_slots[i][1] > time_slots[i + 1][0]:
                    return False
        
        return True
