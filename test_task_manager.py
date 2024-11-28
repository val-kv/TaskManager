import pytest
from task_manager import Task, TaskManager

@pytest.fixture
def manager():
    return TaskManager("test_tasks.json")

def test_add_task(manager):
    task = Task("Test Task", "Description", "Work", "2024-12-01", "Высокий")
    manager.add_task(task)
    assert len(manager.tasks) == 1

def test_edit_task(manager):
    task = Task("Test Task", "Description", "Work", "2024-12-01", "Высокий")
    manager.add_task(task)
    manager.edit_task(1, title="Updated Task")
    assert manager.tasks[0].title == "Updated Task"

def test_mark_as_done(manager):
    task = Task("Test Task", "Description", "Work", "2024-12-01", "Высокий")
    manager.add_task(task)
    manager.mark_as_done(1)
    assert manager.tasks[0].status == "Выполнена"

def test_delete_task(manager):
    task = Task("Test Task", "Description", "Work", "2024-12-01", "Высокий")
    manager.add_task(task)
    manager.delete_task(task_id=1)
    assert len(manager.tasks) == 0
