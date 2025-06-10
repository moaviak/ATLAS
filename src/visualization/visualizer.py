import matplotlib.pyplot as plt
import matplotlib.patches as patches
from ..models.schedule import Schedule

class Visualizer:
    """Handles schedule visualization"""
    
    @staticmethod
    def create_gantt_chart(schedule: Schedule, title: str = "Task Schedule", ax=None):
        """Create a Gantt chart for the schedule"""
        if not schedule.tasks or not any(task.start_time is not None for task in schedule.tasks):
            print("No valid schedule to visualize")
            return
        
        if ax is None:
            _, ax = plt.subplots(figsize=(12, 8))
        
        # Get unique agents
        agents = list(set(task.assigned_agent for task in schedule.tasks if task.assigned_agent))
        agents.sort()
        
        # Color map for agents
        colors = plt.cm.Set3(range(len(agents)))
        agent_colors = {agent: colors[i] for i, agent in enumerate(agents)}
        
        # Plot tasks
        for i, task in enumerate(schedule.tasks):
            if task.start_time is not None and task.assigned_agent:
                agent_idx = agents.index(task.assigned_agent)
                
                # Create rectangle for task
                rect = patches.Rectangle(
                    (task.start_time, agent_idx - 0.4),
                    task.duration, 0.8,
                    linewidth=1, edgecolor='black',
                    facecolor=agent_colors[task.assigned_agent],
                    alpha=0.7
                )
                ax.add_patch(rect)
                
                # Add task label
                ax.text(task.start_time + task.duration/2, agent_idx,
                       task.task_id, ha='center', va='center', fontweight='bold')
        
        # Customize chart
        ax.set_xlim(0, schedule.makespan + 1)
        ax.set_ylim(-0.5, len(agents) - 0.5)
        ax.set_xlabel('Time')
        ax.set_ylabel('Agents')
        ax.set_title(f'{title}\nMakespan: {schedule.makespan}')
        ax.set_yticks(range(len(agents)))
        ax.set_yticklabels(agents)
        ax.grid(True, alpha=0.3)
        
        # Add legend
        legend_elements = [patches.Patch(color=agent_colors[agent], label=agent) 
                          for agent in agents]
        ax.legend(handles=legend_elements, loc='upper right')
        
        return ax

    @staticmethod
    def create_comparison_charts(initial_schedule: Schedule, optimized_schedule: Schedule):
        """Create side-by-side Gantt charts for comparing initial and optimized schedules"""
        # Create a figure with two subplots side by side
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 8))
        
        # Create both charts
        Visualizer.create_gantt_chart(initial_schedule, "Initial Schedule (CSP)", ax1)
        Visualizer.create_gantt_chart(optimized_schedule, "Optimized Schedule (GA)", ax2)
        
        plt.tight_layout()
        plt.show()
