from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Appointment:
    time: datetime
    duration: int
    priority: Priority


@dataclass
class Pet:
    name: str
    breed: str
    species: str
    age: int
    appointments: list[Appointment] = field(default_factory=list)

    def addAppointment(self, appointment: Appointment):
        pass

    def deleteAppointment(self, appointment: Appointment):
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
