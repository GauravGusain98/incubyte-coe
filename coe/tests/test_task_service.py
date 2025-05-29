import pytest
from datetime import date
from coe.services import task_service
from coe.services.user_service import create_user
from coe.models.task import Task, PriorityEnum
from coe.schemas.user import CreateUser
from faker import Faker
from coe.schemas.task import (
    CreateTaskRequestSchema,
    UpdateTaskRequestSchema,
    TaskFilters,
    TaskSort
)

fake = Faker()

@pytest.fixture
def sample_user(db):
    user_data = CreateUser(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.unique.email(),
        password="testpassword"
    )
    return create_user(user_data, db)


def test_create_task(db, sample_user):
    task_data = CreateTaskRequestSchema(
        name="Test Task",
        description="A test description",
        assignee_id=None,
        due_date=date(2025, 6, 1),
        start_date=date(2025, 5, 20),
        priority=PriorityEnum.high
    )

    task = task_service.create_task(task_data, db, sample_user)

    assert task.id is not None, "Task ID should not be None"
    assert task.name == "Test Task"
    assert db.query(Task).filter_by(name="Test Task").first() is not None


def test_find_task_by_id(db, sample_user):
    task = Task(
        name="Lookup Task",
        description="To find by ID",
        created_by_id=sample_user.id,
        due_date=date(2025, 6, 1),
        start_date=date(2025, 5, 20),
        priority=PriorityEnum.medium
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    found_task = task_service.find_task_by_id(task.id, db)

    assert found_task is not None
    assert found_task.id == task.id


def test_get_tasks_list(db, sample_user):
    db.add_all([
        Task(name="Task 1", description="Test", created_by_id=sample_user.id, due_date=date(2025, 6, 1), start_date=date(2025, 5, 20), priority=PriorityEnum.high),
        Task(name="Task 2", description="Test", created_by_id=sample_user.id, due_date=date(2025, 6, 2), start_date=date(2025, 5, 21), priority=PriorityEnum.low)
    ])
    db.commit()

    filters = TaskFilters()
    sort = TaskSort(sort_by="id", sort_order="asc")

    tasks, total = task_service.get_tasks_list(db, filters, sort)

    assert isinstance(tasks, list)
    assert total >= 2, f"Expected at least 2 tasks, got {total}"


def test_update_task_details(db, sample_user):
    task = Task(
        name="Old Name",
        description="Old desc",
        created_by_id=sample_user.id,
        due_date=date(2025, 6, 1),
        start_date=date(2025, 5, 20),
        priority=PriorityEnum.low
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    update_data = UpdateTaskRequestSchema(
        name="New Name",
        description="Updated desc",
        assignee_id=None,
        due_date=date(2025, 6, 3),
        start_date=date(2025, 5, 22),
        priority=PriorityEnum.high
    )

    updated = task_service.update_task_details(task.id, update_data, db)

    assert updated is True
    db.refresh(task)
    assert task.name == "New Name"
    assert task.priority == PriorityEnum.high


def test_update_task_details_not_found(db):
    update_data = UpdateTaskRequestSchema(
        name="Does not matter",
        description="N/A",
        assignee_id=None,
        due_date=date(2025, 6, 3),
        start_date=date(2025, 5, 22),
        priority=PriorityEnum.low
    )

    result = task_service.update_task_details(9999, update_data, db)

    assert result is False, "Updating non-existent task should return False"


def test_remove_task_found(db, sample_user):
    task = Task(
        name="To delete",
        description="Delete me",
        created_by_id=sample_user.id,
        due_date=date(2025, 6, 4),
        start_date=date(2025, 5, 23),
        priority=PriorityEnum.medium
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    result = task_service.remove_task(task.id, db)

    assert result is True
    assert db.query(Task).filter_by(id=task.id).first() is None


def test_remove_task_not_found(db):
    result = task_service.remove_task(99999, db)
    assert result is False, "Removing non-existent task should return False"
