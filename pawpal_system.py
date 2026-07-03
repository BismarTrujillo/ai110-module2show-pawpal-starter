from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from itertools import combinations, count

_task_id_counter = count(1)


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Recurrence(Enum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"


_RECURRENCE_INTERVALS = {
    Recurrence.DAILY: timedelta(days=1),
    Recurrence.WEEKLY: timedelta(weeks=1),
}


@dataclass
class Task:
    title: str
    time: datetime
    duration_minutes: int
    priority: Priority
    completed: bool = False
    recurrence: Recurrence = Recurrence.NONE
    id: int = field(default_factory=lambda: next(_task_id_counter))

    @property
    def end_time(self) -> datetime:
        """The moment this task finishes."""
        return self.time + timedelta(minutes=self.duration_minutes)

    def overlaps(self, other: "Task") -> bool:
        """Return True if this task's [time, end_time) window overlaps another's.

        Back-to-back tasks (one ends exactly when the other starts) do not count
        as overlapping.
        """
        return self.time < other.end_time and other.time < self.end_time

    def mark_complete(self) -> "Task | None":
        """Mark this task as completed. Returns the next occurrence if this task recurs, else None."""
        self.completed = True
        return self.next_occurrence()

    def next_occurrence(self) -> "Task | None":
        """Build the next occurrence of this task based on its recurrence, or None if it doesn't recur."""
        interval = _RECURRENCE_INTERVALS.get(self.recurrence)
        if interval is None:
            return None
        return Task(
            title=self.title,
            time=self.time + interval,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            recurrence=self.recurrence,
        )

    def __str__(self):
        status = "[x]" if self.completed else "[ ]"
        recurs = f" (repeats {self.recurrence.value})" if self.recurrence != Recurrence.NONE else ""
        return (
            f"{status} #{self.id} {self.title} | "
            f"{self.time.strftime('%Y-%m-%d %H:%M')} | "
            f"{self.duration_minutes}min | {self.priority.value}{recurs}"
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

    def schedule_task(self, pet_name: str, task: Task) -> list[str]:
        """Add a task to the named pet's schedule.

        Returns a list of conflict warning messages (empty if none). Conflicts
        never block scheduling -- the task is always added.
        """
        for pet in self.owner.pets:
            if pet.name == pet_name:
                pet.addTask(task)
                return self.check_conflicts_for_task(task)
        raise ValueError(f"No pet named '{pet_name}' found.")

    @staticmethod
    def _describe(pet_name: str, task: Task) -> str:
        window = f"{task.time.strftime('%H:%M')}-{task.end_time.strftime('%H:%M')}"
        return f"{pet_name}'s '{task.title}' (#{task.id}, {window})"

    def check_conflicts_for_task(self, task: Task) -> list[str]:
        """Check a single task against every other task for an overlapping time window.

        Lightweight strategy: instead of comparing every pair of tasks (O(n^2)),
        this scans the existing schedule once (O(n)), comparing each other task's
        [time, end_time) window against this task's via Task.overlaps(). Returns
        human-readable warning strings; never raises.
        """
        return [
            f"WARNING: {self._describe(pet.name, task)} overlaps {self._describe(pet.name, other)}"
            for pet in self.owner.pets
            for other in pet.tasks
            if other.id != task.id and task.overlaps(other)
        ]

    def find_conflicts(self) -> list[str]:
        """Audit the full schedule and return a warning for every pair of tasks
        whose time windows overlap, across all pets. Never raises.

        Unlike check_conflicts_for_task, overlap can't be found with a simple
        group-by-time lookup, so this compares every pair of tasks (O(n^2)) --
        acceptable for a single owner's schedule, which stays small.
        """
        entries = [(pet.name, task) for pet in self.owner.pets for task in pet.tasks]
        return [
            f"WARNING: {self._describe(pet_a, a)} overlaps {self._describe(pet_b, b)}"
            for (pet_a, a), (pet_b, b) in combinations(entries, 2)
            if a.overlaps(b)
        ]

    def remove_task(self, task_id: int):
        """Delete a task by id from whichever pet holds it."""
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.id == task_id:
                    pet.deleteTask(task)
                    return
        raise ValueError(f"No task with id {task_id} found.")

    def complete_task(self, task_id: int):
        """Mark a task as completed, looked up by id across all pets.

        If the task recurs (daily/weekly), its next occurrence is automatically
        scheduled for the same pet.
        """
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.id == task_id:
                    next_task = task.mark_complete()
                    if next_task is not None:
                        pet.addTask(next_task)
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

    def sort_by_time(self, tasks: list[Task] | None = None) -> list[Task]:
        """Return the given tasks (default: all tasks) sorted by time ascending."""
        if tasks is None:
            tasks = self.get_all_tasks()
        return sorted(tasks, key=lambda t: t.time)

    def filter_tasks(
        self,
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[Task]:
        """Return tasks matching the given pet name and/or completion status."""
        tasks = self.get_tasks_for_pet(pet_name) if pet_name is not None else self.get_all_tasks()
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        return tasks

    def display_all_schedules(self):
        """Print the full schedule for every pet owned."""
        print(f"\n=== Full Schedule for {self.owner.name}'s pets ===")
        for pet in self.owner.pets:
            pet.displaySchedule()
