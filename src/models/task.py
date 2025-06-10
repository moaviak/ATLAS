from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Task:
    """Represents a task with its properties"""
    task_id: str
    duration: int
    dependencies: List[str] = field(default_factory=list)
    required_resources: List[str] = field(default_factory=list)
    start_time: Optional[int] = None
    assigned_agent: Optional[str] = None
    
    def __post_init__(self):
        if isinstance(self.dependencies, str):
            self.dependencies = [self.dependencies] if self.dependencies else []
        if isinstance(self.required_resources, str):
            self.required_resources = [self.required_resources] if self.required_resources else []
