import copy
import random
from typing import List, Optional
from ..models.task import Task
from ..models.agent import Agent
from ..models.schedule import Schedule
from .csp_solver import CSPSolver

class GeneticAlgorithm:
    """Genetic Algorithm for schedule optimization"""
    
    def __init__(self, tasks: List[Task], agents: List[Agent], 
                 population_size: int = 50, generations: int = 100,
                 mutation_rate: float = 0.1, elite_size: int = 10):
        self.tasks = tasks
        self.agents = agents
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elite_size = elite_size
        self.csp_solver = CSPSolver(tasks, agents)
    
    def optimize(self, initial_schedule: Schedule) -> Schedule:
        """Optimize schedule using genetic algorithm"""
        print("Starting Genetic Algorithm optimization...")
        
        # Initialize population
        population = self._initialize_population(initial_schedule)
        
        best_schedule = None
        best_fitness = 0
        
        for generation in range(self.generations):
            # Evaluate fitness
            fitness_scores = [self._fitness(schedule) for schedule in population]
            
            # Track best solution
            max_fitness_idx = fitness_scores.index(max(fitness_scores))
            current_best = population[max_fitness_idx]
            current_fitness = fitness_scores[max_fitness_idx]
            
            if current_fitness > best_fitness:
                best_fitness = current_fitness
                best_schedule = copy.deepcopy(current_best)
            
            if generation % 20 == 0:
                print(f"Generation {generation}: Best makespan = {best_schedule.makespan}")
            
            # Selection and reproduction
            new_population = []
            
            # Elite selection
            elite_indices = sorted(range(len(fitness_scores)), 
                                 key=lambda i: fitness_scores[i], reverse=True)[:self.elite_size]
            for idx in elite_indices:
                new_population.append(copy.deepcopy(population[idx]))
            
            # Generate offspring
            while len(new_population) < self.population_size:
                parent1 = self._tournament_selection(population, fitness_scores)
                parent2 = self._tournament_selection(population, fitness_scores)
                
                offspring = self._crossover(parent1, parent2)
                if offspring and random.random() < self.mutation_rate:
                    offspring = self._mutate(offspring)
                
                if offspring and offspring.is_valid():
                    offspring.calculate_makespan()
                    new_population.append(offspring)
                else:
                    # Add a random valid schedule if offspring is invalid
                    valid_schedule = self._create_random_schedule()
                    if valid_schedule:
                        new_population.append(valid_schedule)
            
            population = new_population[:self.population_size]
        
        print(f"GA optimization completed. Final makespan: {best_schedule.makespan}")
        return best_schedule
    
    def _initialize_population(self, initial_schedule: Schedule) -> List[Schedule]:
        """Initialize population with random valid schedules"""
        population = [copy.deepcopy(initial_schedule)]
        
        while len(population) < self.population_size:
            schedule = self._create_random_schedule()
            if schedule:
                population.append(schedule)
        
        return population
    
    def _create_random_schedule(self) -> Optional[Schedule]:
        """Create a random valid schedule"""
        # Use CSP solver with randomized agent selection
        original_agents = self.agents[:]
        random.shuffle(self.agents)
        
        schedule = self.csp_solver.solve()
        self.agents = original_agents
        
        return schedule
    
    def _fitness(self, schedule: Schedule) -> float:
        """Calculate fitness (inverse of makespan)"""
        if schedule.makespan <= 0:
            schedule.calculate_makespan()
        
        return 1000.0 / (schedule.makespan + 1)  # Add 1 to avoid division by zero
    
    def _tournament_selection(self, population: List[Schedule], fitness_scores: List[float]) -> Schedule:
        """Tournament selection"""
        tournament_size = 3
        tournament_indices = random.sample(range(len(population)), min(tournament_size, len(population)))
        best_idx = max(tournament_indices, key=lambda i: fitness_scores[i])
        return population[best_idx]
    
    def _crossover(self, parent1: Schedule, parent2: Schedule) -> Optional[Schedule]:
        """Order crossover for schedules"""
        try:
            child_tasks = []
            
            for task1, task2 in zip(parent1.tasks, parent2.tasks):
                child_task = copy.deepcopy(task1)
                
                # Randomly choose assignment from either parent
                if random.random() < 0.5:
                    child_task.assigned_agent = task1.assigned_agent
                else:
                    child_task.assigned_agent = task2.assigned_agent
                
                child_tasks.append(child_task)
            
            # Reconstruct schedule with new assignments
            child_schedule = Schedule(child_tasks, self.agents)
            if self._repair_schedule(child_schedule):
                return child_schedule
            
        except Exception:
            pass
        
        return None
    
    def _mutate(self, schedule: Schedule) -> Optional[Schedule]:
        """Mutate schedule by reassigning random tasks"""
        try:
            mutated_schedule = copy.deepcopy(schedule)
            
            # Select random tasks to mutate
            num_mutations = max(1, int(len(self.tasks) * 0.1))
            tasks_to_mutate = random.sample(mutated_schedule.tasks, num_mutations)
            
            for task in tasks_to_mutate:
                # Find capable agents
                capable_agents = [agent for agent in self.agents 
                                if agent.can_perform_task(task)]
                
                if capable_agents:
                    task.assigned_agent = random.choice(capable_agents).agent_id
            
            # Repair the schedule
            if self._repair_schedule(mutated_schedule):
                return mutated_schedule
            
        except Exception:
            pass
        
        return schedule
    
    def _repair_schedule(self, schedule: Schedule) -> bool:
        """Repair schedule by recalculating start times"""
        try:
            # Sort tasks by dependencies
            sorted_tasks = self.csp_solver._topological_sort(schedule.tasks)
            
            # Reset start times
            for task in sorted_tasks:
                task.start_time = None
            
            # Recalculate start times
            for task in sorted_tasks:
                if task.assigned_agent:
                    agent = next((a for a in self.agents if a.agent_id == task.assigned_agent), None)
                    if agent:
                        earliest_start = self.csp_solver._get_earliest_start_time(
                            task, agent, [t for t in sorted_tasks if t.start_time is not None])
                        if earliest_start is not None:
                            task.start_time = earliest_start
                        else:
                            return False
            
            schedule.calculate_makespan()
            return schedule.is_valid()
            
        except Exception:
            return False
