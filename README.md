# AI-Powered Autonomous Task Scheduler

A Python-based implementation of an autonomous task scheduler that uses AI techniques (Constraint Satisfaction Problem solving and Genetic Algorithms) to efficiently schedule tasks among multiple agents.

## Features

- Constraint Satisfaction Problem (CSP) solver for initial feasible solution
- Genetic Algorithm (GA) optimization for schedule improvement
- Multi-agent task scheduling with skill requirements
- Dependency management between tasks
- Visual representation using Gantt charts
- JSON-based scenario input/output

## Project Structure

```
.
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── src/                    # Source code
│   ├── models/            # Data models
│   │   ├── task.py       # Task class definition
│   │   ├── agent.py      # Agent class definition
│   │   └── schedule.py   # Schedule class definition
│   ├── solvers/          # Scheduling algorithms
│   │   ├── csp_solver.py    # Constraint Satisfaction Problem solver
│   │   └── genetic_algorithm.py # Genetic Algorithm optimizer
│   ├── utils/            # Utility functions
│   │   └── input_handler.py # Input handling utilities
│   └── visualization/    # Visualization tools
│       └── visualizer.py # Gantt chart visualization
```

## Requirements

- Python 3.8+
- matplotlib
- Additional dependencies listed in requirements.txt

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd AI-Semester-Project
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Basic usage with default scenario:

```bash
python main.py
```

2. Using custom scenario file:

```bash
python main.py --scenario path/to/your/scenario.json
# or
python main.py -s path/to/your/scenario.json
```

3. Programmatic usage:

```python
from src.task_scheduler import TaskScheduler

scheduler = TaskScheduler()
scheduler.load_scenario('path/to/your/scenario.json')
scheduler.solve_csp()
scheduler.optimize_with_ga()
scheduler.compare_results()
scheduler.visualize_schedules()
```

## Input Format

The scheduler accepts JSON files with the following structure:

```json
{
  "tasks": [
    {
      "task_id": "T1",
      "duration": 3,
      "dependencies": [],
      "required_resources": ["skill_A"]
    }
  ],
  "agents": [
    {
      "agent_id": "A1",
      "skills": ["skill_A", "skill_B"]
    }
  ]
}
```

## Algorithm Details

### CSP Solver

- Uses backtracking to find initial feasible solution
- Handles task dependencies and resource constraints
- Ensures agent capability requirements

### Genetic Algorithm

- Population-based optimization
- Uses crossover and mutation operators
- Maintains schedule validity during evolution
- Optimizes for minimal makespan

## Visualization

The scheduler provides Gantt chart visualization showing:

- Task assignments to agents
- Task dependencies
- Schedule timeline
- Agent workload distribution

## License

This project is licensed under the MIT License - see the LICENSE file for details.
