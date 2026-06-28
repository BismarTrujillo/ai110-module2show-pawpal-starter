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
    id: int = field(default_factory=lambda: next(_task_id_counter))


@dataclass
class Pet:
    name: str
    breed: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def addTask(self, task: Task):
        pass

    def deleteTask(self, task: Task):
        pass

    def displaySchedule(self):
        pass


@dataclass
class Owner:
    name: str
    address: str
    pets: list[Pet] = field(default_factory=list)

    def addPet(self, pet: Pet):
        pass

    def editPet(self, name: str, updated_pet: Pet):
        pass

    def displayPets(self):
        pass
