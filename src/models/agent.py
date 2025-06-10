from dataclasses import dataclass, field
from typing import List
from .task import Task

@dataclass
class Agent:
    """Represents an agent with its capabilities"""
    agent_id: str
    skills: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if isinstance(self.skills, str):
            self.skills = [self.skills] if self.skills else []
    
    def can_perform_task(self, task: Task) -> bool:
        """Check if agent has required skills for the task"""
        return all(resource in self.skills for resource in task.required_resources)
