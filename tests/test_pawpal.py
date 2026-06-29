from datetime import datetime
from pawpal_system import Task, Pet, Priority


def test_mark_complete_changes_status():
    task = Task(
        title="Bath time",
        time=datetime(2026, 6, 28, 10, 0),
        duration_minutes=20,
        priority=Priority.LOW,
    )
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Luna", species="Dog", breed="Golden Retriever", age=3)
    assert len(pet.tasks) == 0

    pet.addTask(Task(
        title="Morning walk",
        time=datetime(2026, 6, 28, 7, 30),
        duration_minutes=30,
        priority=Priority.HIGH,
    ))
    assert len(pet.tasks) == 1

    pet.addTask(Task(
        title="Vet checkup",
        time=datetime(2026, 6, 28, 14, 0),
        duration_minutes=45,
        priority=Priority.HIGH,
    ))
    assert len(pet.tasks) == 2
