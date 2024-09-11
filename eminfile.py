from datetime import datetime, timedelta

# Task structure with improved variable names and clear docstrings
class Task:
    def __init__(self, title, priority, deadline, estimated_time):
        """
        Initialize a Task with title, priority, deadline, and estimated time.
        
        :param title: str, title of the task
        :param priority: int, priority level of the task (higher means more important)
        :param deadline: datetime, deadline by which the task should be completed
        :param estimated_time: float, estimated time required to complete the task in hours
        """
        self.title = title
        self.priority = priority
        self.deadline = deadline
        self.estimated_time = estimated_time
    
    def __repr__(self):
        """Provide a string representation of the task."""
        return f"{self.title} (Priority: {self.priority}, Deadline: {self.deadline}, Estimated Time: {self.estimated_time} hours)"

# Function to sort tasks by urgency score
def sort_tasks_by_priority(tasks):
    """
    Sort tasks by their urgency score, factoring in priority, time until the deadline, and estimated time.
    
    :param tasks: list of Task objects
    :return: list of sorted Task objects by urgency
    """
    now = datetime.now()

    def calculate_urgency_score(task):
        """
        Calculate urgency score based on priority, remaining time until the deadline, and estimated completion time.
        
        :param task: Task object
        :return: float, urgency score where higher score means higher urgency
        """
        time_left = (task.deadline - now).total_seconds() / 3600  # Time left in hours
        if time_left <= 0:
            return float('inf')  # Task is overdue, highest urgency
        
        # Formula: priority * (1 / time_left) * (1 / estimated_time)
        return (task.priority / time_left) / task.estimated_time

    # Sort tasks based on calculated urgency scores
    return sorted(tasks, key=calculate_urgency_score, reverse=True)

# Example tasks with clearer comments and structure
tasks = [
    Task("Complete project report", priority=10, deadline=datetime.now() + timedelta(hours=5), estimated_time=2),
    Task("Prepare presentation slides", priority=7, deadline=datetime.now() + timedelta(hours=48), estimated_time=4),
    Task("Finish coding assignment", priority=8, deadline=datetime.now() + timedelta(hours=12), estimated_time=6),
    Task("Update project documentation", priority=6, deadline=datetime.now() + timedelta(hours=24), estimated_time=3)
]

# Sorting the tasks by priority and printing the result
sorted_tasks = sort_tasks_by_priority(tasks)
for task in sorted_tasks:
    print(task)
