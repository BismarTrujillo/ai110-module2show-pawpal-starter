from datetime import datetime
from pawpal_system import Task, Pet, Owner, Scheduler, Priority

owner = Owner(name="Maria", address="123 Maple St")

luna = Pet(name="Luna", species="Dog", breed="Golden Retriever", age=3)
mochi = Pet(name="Mochi", species="Cat", breed="Siamese", age=5)

owner.addPet(luna)
owner.addPet(mochi)

scheduler = Scheduler(owner)

scheduler.schedule_task("Luna", Task(
    title="Morning walk",
    time=datetime(2026, 6, 28, 7, 30),
    duration_minutes=30,
    priority=Priority.HIGH,
))

scheduler.schedule_task("Luna", Task(
    title="Flea treatment",
    time=datetime(2026, 6, 28, 11, 0),
    duration_minutes=15,
    priority=Priority.MEDIUM,
))

scheduler.schedule_task("Mochi", Task(
    title="Vet checkup",
    time=datetime(2026, 6, 28, 14, 0),
    duration_minutes=45,
    priority=Priority.HIGH,
))

scheduler.schedule_task("Mochi", Task(
    title="Evening feeding",
    time=datetime(2026, 6, 28, 18, 0),
    duration_minutes=10,
    priority=Priority.LOW,
))

print("=" * 40)
print("        TODAY'S SCHEDULE")
print("=" * 40)
scheduler.display_all_schedules()
