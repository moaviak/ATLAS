import time
from typing import Optional
from src.models.task import Task
from src.models.agent import Agent
from src.models.schedule import Schedule
from src.utils.input_handler import InputHandler
from src.solvers.csp_solver import CSPSolver
from src.solvers.genetic_algorithm import GeneticAlgorithm
from src.visualization.visualizer import Visualizer

class TaskScheduler:
    """Main application class"""
    
    def __init__(self):
        self.tasks = []
        self.agents = []
        self.initial_schedule = None
        self.optimized_schedule = None
    
    def load_scenario(self, filepath: str = None):
        """Load scenario from file or create sample"""
        if filepath:
            self.tasks, self.agents = InputHandler.load_from_json(filepath)
        else:
            print("Creating sample scenario...")
            self.tasks, self.agents = InputHandler.create_sample_scenario()
        
        print(f"Loaded {len(self.tasks)} tasks and {len(self.agents)} agents")
        self._print_scenario_info()
    
    def _print_scenario_info(self):
        """Print scenario information"""
        print("\n=== SCENARIO INFO ===")
        print("Tasks:")
        for task in self.tasks:
            deps = ", ".join(task.dependencies) if task.dependencies else "None"
            resources = ", ".join(task.required_resources) if task.required_resources else "None"
            print(f"  {task.task_id}: Duration={task.duration}, Dependencies=[{deps}], Resources=[{resources}]")
        
        print("\nAgents:")
        for agent in self.agents:
            skills = ", ".join(agent.skills) if agent.skills else "None"
            print(f"  {agent.agent_id}: Skills=[{skills}]")
    
    def solve_csp(self):
        """Solve using CSP to find initial feasible solution"""
        print("\n=== CSP SOLVING ===")
        print("Finding initial feasible schedule...")
        
        csp_solver = CSPSolver(self.tasks, self.agents)
        self.initial_schedule = csp_solver.solve()
        
        if self.initial_schedule:
            print(f"Initial schedule found with makespan: {self.initial_schedule.makespan}")
            self._print_schedule(self.initial_schedule, "Initial Schedule")
        else:
            print("No feasible schedule found!")
            return False
        
        return True
    
    def optimize_with_ga(self):
        """Optimize schedule using Genetic Algorithm"""
        if not self.initial_schedule:
            print("No initial schedule available for optimization")
            return
        
        print("\n=== GENETIC ALGORITHM OPTIMIZATION ===")
        
        ga = GeneticAlgorithm(self.tasks, self.agents, population_size=30, generations=50)
        self.optimized_schedule = ga.optimize(self.initial_schedule)
        
        print(f"Optimized schedule makespan: {self.optimized_schedule.makespan}")
        self._print_schedule(self.optimized_schedule, "Optimized Schedule")
    
    def _print_schedule(self, schedule: Schedule, title: str):
        """Print schedule details"""
        print(f"\n--- {title} ---")
        for task in sorted(schedule.tasks, key=lambda t: t.start_time or 0):
            if task.start_time is not None:
                end_time = task.start_time + task.duration
                print(f"{task.task_id}: Agent={task.assigned_agent}, "
                      f"Start={task.start_time}, End={end_time}")
    
    def compare_results(self):
        """Compare initial and optimized schedules"""
        if not self.initial_schedule or not self.optimized_schedule:
            print("Both schedules needed for comparison")
            return
        
        print("\n=== RESULTS COMPARISON ===")
        print(f"Initial Schedule Makespan: {self.initial_schedule.makespan}")
        print(f"Optimized Schedule Makespan: {self.optimized_schedule.makespan}")
        
        improvement = self.initial_schedule.makespan - self.optimized_schedule.makespan
        improvement_pct = (improvement / self.initial_schedule.makespan) * 100 if self.initial_schedule.makespan > 0 else 0
        
        print(f"Improvement: {improvement} time units ({improvement_pct:.1f}%)")
        
    def visualize_schedules(self):
        """Create Gantt charts for both schedules"""
        if self.initial_schedule and self.optimized_schedule:
            print("\nGenerating comparison Gantt charts...")
            Visualizer.create_comparison_charts(self.initial_schedule, self.optimized_schedule)
        elif self.initial_schedule:
            print("\nGenerating Initial Schedule Gantt Chart...")
            Visualizer.create_gantt_chart(self.initial_schedule, "Initial Schedule (CSP)")
        elif self.optimized_schedule:
            print("Generating Optimized Schedule Gantt Chart...")
            Visualizer.create_gantt_chart(self.optimized_schedule, "Optimized Schedule (GA)")
    
    def run_simulation(self):
        """Run the complete simulation"""
        print("="*60)
        print("AI-POWERED AUTONOMOUS TASK SCHEDULER")
        print("="*60)
        
        start_time = time.time()
        
        # Load scenario
        self.load_scenario()
        
        # Solve with CSP
        if not self.solve_csp():
            return
        
        # Optimize with GA
        self.optimize_with_ga()
        
        # Compare results
        self.compare_results()
        
        # Show execution time
        execution_time = time.time() - start_time
        print(f"\nTotal execution time: {execution_time:.2f} seconds")
        
        # Generate visualizations
        self.visualize_schedules()
        
        print("\nSimulation completed successfully!")
