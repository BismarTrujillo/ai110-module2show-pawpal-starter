from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    time: datetime
    duration: int
    priority: Priority


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

    def editPet(self, pet: Pet):
        pass

    def displayPets(self):
        pass
