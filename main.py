from datetime import datetime
from pawpal_system import Task, Pet, Owner, Scheduler, Priority

owner = Owner(name="Maria", address="123 Maple St")

luna = Pet(name="Luna", species="Dog", breed="Golden Retriever", age=3)
mochi = Pet(name="Mochi", species="Cat", breed="Siamese", age=5)

owner.addPet(luna)
owner.addPet(mochi)

scheduler = Scheduler(owner)

# Tasks are added out of chronological order on purpose, to prove sort_by_time works.
vet_checkup = Task(
    title="Vet checkup",
    time=datetime(2026, 7, 2, 14, 0),
    duration_minutes=45,
    priority=Priority.HIGH,
)
scheduler.schedule_task("Mochi", vet_checkup)

morning_walk = Task(
    title="Morning walk",
    time=datetime(2026, 7, 2, 7, 30),
    duration_minutes=30,
    priority=Priority.HIGH,
)
scheduler.schedule_task("Luna", morning_walk)

evening_feeding = Task(
    title="Evening feeding",
    time=datetime(2026, 7, 2, 18, 0),
    duration_minutes=10,
    priority=Priority.LOW,
)
scheduler.schedule_task("Mochi", evening_feeding)

flea_treatment = Task(
    title="Flea treatment",
    time=datetime(2026, 7, 2, 11, 0),
    duration_minutes=15,
    priority=Priority.MEDIUM,
)
scheduler.schedule_task("Luna", flea_treatment)

# Mark one task complete so filtering by status has something to show.
scheduler.complete_task(flea_treatment.id)

# Two tasks scheduled at the exact same time, on purpose, to exercise conflict detection.
brushing = Task(
    title="Brushing",
    time=datetime(2026, 7, 2, 7, 30),  # same time as Luna's own "Morning walk" -> same-pet conflict
    duration_minutes=15,
    priority=Priority.LOW,
)
schedule_warnings = scheduler.schedule_task("Luna", brushing)
for warning in schedule_warnings:
    print(warning)

photo_session = Task(
    title="Photo session",
    time=datetime(2026, 7, 2, 7, 30),  # same time again, but for Mochi -> cross-pet conflict
    duration_minutes=20,
    priority=Priority.LOW,
)
schedule_warnings = scheduler.schedule_task("Mochi", photo_session)
for warning in schedule_warnings:
    print(warning)

print("=" * 40)
print("        TODAY'S SCHEDULE")
print("=" * 40)
scheduler.display_all_schedules()

print("\n" + "=" * 40)
print("   ALL TASKS SORTED BY TIME")
print("=" * 40)
for task in scheduler.sort_by_time():
    print(f"  {task}")

print("\n" + "=" * 40)
print("   PENDING TASKS (filter by status)")
print("=" * 40)
for task in scheduler.filter_tasks(completed=False):
    print(f"  {task}")

print("\n" + "=" * 40)
print("   COMPLETED TASKS (filter by status)")
print("=" * 40)
for task in scheduler.filter_tasks(completed=True):
    print(f"  {task}")

print("\n" + "=" * 40)
print("   LUNA'S TASKS (filter by pet)")
print("=" * 40)
for task in scheduler.filter_tasks(pet_name="Luna"):
    print(f"  {task}")

print("\n" + "=" * 40)
print("   LUNA'S PENDING TASKS (filter by pet + status)")
print("=" * 40)
for task in scheduler.filter_tasks(pet_name="Luna", completed=False):
    print(f"  {task}")

print("\n" + "=" * 40)
print("   SCHEDULE CONFLICTS (full audit)")
print("=" * 40)
conflicts = scheduler.find_conflicts()
if not conflicts:
    print("  No conflicts found.")
else:
    for warning in conflicts:
        print(f"  {warning}")
