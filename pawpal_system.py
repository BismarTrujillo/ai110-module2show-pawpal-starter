from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from itertools import count

_task_id_counter = count(1)


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    title: str
    time: datetime
    duration_minutes: int
    priority: Priority
    completed: bool = False
    id: int = field(default_factory=lambda: next(_task_id_counter))

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def __str__(self):
        status = "[x]" if self.completed else "[ ]"
        return (
            f"{status} #{self.id} {self.title} | "
            f"{self.time.strftime('%Y-%m-%d %H:%M')} | "
            f"{self.duration_minutes}min | {self.priority.value}"
        )


@dataclass
class Pet:
    name: str
    breed: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def addTask(self, task: Task):
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def deleteTask(self, task: Task):
        """Remove a task from this pet's list by its id."""
        self.tasks = [t for t in self.tasks if t.id != task.id]

    def displaySchedule(self):
        """Print this pet's tasks sorted by time."""
        print(f"\n--- Schedule for {self.name} ---")
        if not self.tasks:
            print("  No tasks scheduled.")
            return
        for task in sorted(self.tasks, key=lambda t: t.time):
            print(f"  {task}")

    def get_pending_tasks(self) -> list[Task]:
        """Return all tasks that have not been completed."""
        return [t for t in self.tasks if not t.completed]

    def get_tasks_by_priority(self, priority: Priority) -> list[Task]:
        """Return all tasks matching the given priority level."""
        return [t for t in self.tasks if t.priority == priority]


@dataclass
class Owner:
    name: str
    address: str
    pets: list[Pet] = field(default_factory=list)

    def addPet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def editPet(self, name: str, updated_pet: Pet):
        """Replace the pet with the given name with updated_pet."""
        for i, pet in enumerate(self.pets):
            if pet.name == name:
                self.pets[i] = updated_pet
                return
        raise ValueError(f"No pet named '{name}' found.")

    def displayPets(self):
        """Print a summary of all pets owned."""
        print(f"\n--- Pets owned by {self.name} ---")
        if not self.pets:
            print("  No pets registered.")
            return
        for pet in self.pets:
            print(f"  {pet.name} ({pet.species}, {pet.breed}, age {pet.age})")

    def get_all_tasks(self) -> list[Task]:
        """Return a flat list of every task across all pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def schedule_task(self, pet_name: str, task: Task):
        """Add a task to the named pet's schedule."""
        for pet in self.owner.pets:
            if pet.name == pet_name:
                pet.addTask(task)
                return
        raise ValueError(f"No pet named '{pet_name}' found.")

    def remove_task(self, task_id: int):
        """Delete a task by id from whichever pet holds it."""
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.id == task_id:
                    pet.deleteTask(task)
                    return
        raise ValueError(f"No task with id {task_id} found.")

    def complete_task(self, task_id: int):
        """Mark a task as completed, looked up by id across all pets."""
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.id == task_id:
                    task.mark_complete()
                    return
        raise ValueError(f"No task with id {task_id} found.")

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all pets for this owner."""
        return self.owner.get_all_tasks()

    def get_pending_tasks(self) -> list[Task]:
        """Return all incomplete tasks across all pets."""
        return [t for t in self.get_all_tasks() if not t.completed]

    def get_tasks_by_priority(self, priority: Priority) -> list[Task]:
        """Return all tasks matching the given priority across all pets."""
        return [t for t in self.get_all_tasks() if t.priority == priority]

    def get_upcoming_tasks(self) -> list[Task]:
        """Return future tasks sorted by time ascending."""
        now = datetime.now()
        return sorted(
            [t for t in self.get_all_tasks() if t.time >= now],
            key=lambda t: t.time,
        )

    def get_tasks_for_pet(self, pet_name: str) -> list[Task]:
        """Return a copy of the task list for the named pet."""
        for pet in self.owner.pets:
            if pet.name == pet_name:
                return list(pet.tasks)
        raise ValueError(f"No pet named '{pet_name}' found.")

    def display_all_schedules(self):
        """Print the full schedule for every pet owned."""
        print(f"\n=== Full Schedule for {self.owner.name}'s pets ===")
        for pet in self.owner.pets:
            pet.displaySchedule()
