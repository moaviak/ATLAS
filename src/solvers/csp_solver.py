import copy
from typing import List, Dict, Optional
from ..models.task import Task
from ..models.agent import Agent
from ..models.schedule import Schedule

class CSPSolver:
    """Constraint Satisfaction Problem solver using backtracking"""
    
    def __init__(self, tasks: List[Task], agents: List[Agent]):
        self.tasks = tasks
        self.agents = agents
        self.task_dict = {task.task_id: task for task in tasks}
        self.agent_dict = {agent.agent_id: agent for agent in agents}
    
    def solve(self) -> Optional[Schedule]:
        """Find a feasible schedule using backtracking"""
        # Create a copy of tasks to avoid modifying originals
        schedule_tasks = [copy.deepcopy(task) for task in self.tasks]
        
        # Sort tasks by dependencies (topological sort)
        sorted_tasks = self._topological_sort(schedule_tasks)
        
        if self._backtrack(sorted_tasks, 0):
            schedule = Schedule(schedule_tasks, self.agents)
            schedule.calculate_makespan()
            return schedule
        
        return None
    
    def _topological_sort(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks based on dependencies"""
        task_dict = {task.task_id: task for task in tasks}
        visited = set()
        temp_visited = set()
        result = []
        
        def visit(task_id: str):
            if task_id in temp_visited:
                return  # Cycle detected, skip
            if task_id in visited:
                return
            
            temp_visited.add(task_id)
            task = task_dict.get(task_id)
            if task:
                for dep_id in task.dependencies:
                    if dep_id in task_dict:
                        visit(dep_id)
                
                temp_visited.remove(task_id)
                visited.add(task_id)
                result.append(task)
        
        for task in tasks:
            if task.task_id not in visited:
                visit(task.task_id)
        
        return result
    
    def _backtrack(self, tasks: List[Task], task_index: int) -> bool:
        """Backtracking algorithm to assign tasks to agents"""
        if task_index >= len(tasks):
            return True  # All tasks assigned
        
        current_task = tasks[task_index]
        
        # Find capable agents
        capable_agents = [agent for agent in self.agents 
                         if agent.can_perform_task(current_task)]
        
        if not capable_agents:
            return False  # No capable agent found
        
        # Try assigning to each capable agent
        for agent in capable_agents:
            # Find earliest possible start time
            earliest_start = self._get_earliest_start_time(current_task, agent, tasks[:task_index])
            
            if earliest_start is not None:
                # Assign task
                current_task.assigned_agent = agent.agent_id
                current_task.start_time = earliest_start
                
                # Continue with next task
                if self._backtrack(tasks, task_index + 1):
                    return True
                
                # Backtrack
                current_task.assigned_agent = None
                current_task.start_time = None
        
        return False
    
    def _get_earliest_start_time(self, task: Task, agent: Agent, assigned_tasks: List[Task]) -> Optional[int]:
        """Find the earliest possible start time for a task"""
        # Check dependency constraints
        min_start_time = 0
        for dep_id in task.dependencies:
            for assigned_task in assigned_tasks:
                if assigned_task.task_id == dep_id and assigned_task.start_time is not None:
                    min_start_time = max(min_start_time, assigned_task.start_time + assigned_task.duration)
        
        # Check agent availability
        agent_tasks = [t for t in assigned_tasks if t.assigned_agent == agent.agent_id and t.start_time is not None]
        agent_tasks.sort(key=lambda x: x.start_time)
        
        # Try to fit the task in agent's schedule
        current_time = min_start_time
        
        for agent_task in agent_tasks:
            if current_time + task.duration <= agent_task.start_time:
                return current_time
            current_time = max(current_time, agent_task.start_time + agent_task.duration)
        
        return current_time
