import json
import os
from datetime import datetime
from typing import List, Optional


class Task:
    def __init__(self, title: str, description: str, category: str, due_date: str, priority: str):
        self.id = None
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = "Не выполнена"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data):
        task = Task(data["title"], data["description"], data["category"], data["due_date"], data["priority"])
        task.id = data["id"]
        task.status = data["status"]
        return task


class TaskManager:
    def __init__(self, storage_file="tasks.json"):
        self.storage_file = storage_file
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.tasks = [Task.from_dict(task) for task in data]

    def save_tasks(self):
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False, indent=4)

    def add_task(self, task: Task):
        task.id = self.get_next_id()
        self.tasks.append(task)
        self.save_tasks()

    def get_next_id(self):
        return max((task.id for task in self.tasks), default=0) + 1

    def view_tasks(self, category: Optional[str] = None, status: Optional[str] = None):
        tasks = self.tasks
        if category:
            tasks = [task for task in tasks if task.category == category]
        if status:
            tasks = [task for task in tasks if task.status == status]
        return tasks

    def edit_task(self, task_id: int, **kwargs):
        task = self.find_task(task_id)
        if not task:
            return False
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        self.save_tasks()
        return True

    def mark_as_done(self, task_id: int):
        task = self.find_task(task_id)
        if task:
            task.status = "Выполнена"
            self.save_tasks()
            return True
        return False

    def delete_task(self, task_id: Optional[int] = None, category: Optional[str] = None):
        if task_id:
            self.tasks = [task for task in self.tasks if task.id != task_id]
        elif category:
            self.tasks = [task for task in self.tasks if task.category != category]
        self.save_tasks()

    def find_task(self, task_id: int):
        return next((task for task in self.tasks if task.id == task_id), None)


def main():
    manager = TaskManager()

    while True:
        print("\nМенеджер задач")
        print("1. Просмотреть задачи")
        print("2. Добавить задачу")
        print("3. Изменить задачу")
        print("4. Отметить задачу как выполненную")
        print("5. Удалить задачу")
        print("6. Поиск задач")
        print("0. Выход")

        choice = input("Выберите действие: ")
        if choice == "1":
            category = input("Введите категорию (или оставьте пустым): ")
            status = input("Введите статус (Не выполнена/Выполнена, или оставьте пустым): ")
            tasks = manager.view_tasks(category or None, status or None)
            for task in tasks:
                print(task.to_dict())
        elif choice == "2":
            title = input("Название задачи: ")
            description = input("Описание задачи: ")
            category = input("Категория задачи: ")
            due_date = input("Срок выполнения (ГГГГ-ММ-ДД): ")
            priority = input("Приоритет (Низкий/Средний/Высокий): ")
            manager.add_task(Task(title, description, category, due_date, priority))
        elif choice == "3":
            task_id = int(input("Введите ID задачи: "))
            field = input("Введите поле для изменения (title/description/category/due_date/priority): ")
            value = input(f"Новое значение для {field}: ")
            if manager.edit_task(task_id, **{field: value}):
                print("Задача успешно обновлена.")
            else:
                print("Задача не найдена.")
        elif choice == "4":
            task_id = int(input("Введите ID задачи: "))
            if manager.mark_as_done(task_id):
                print("Задача отмечена как выполненная.")
            else:
                print("Задача не найдена.")
        elif choice == "5":
            task_id = input("Введите ID задачи (или оставьте пустым для удаления по категории): ")
            category = None if task_id else input("Введите категорию: ")
            manager.delete_task(int(task_id) if task_id else None, category)
        elif choice == "6":
            keyword = input("Введите ключевое слово: ")
            tasks = [task for task in manager.tasks if keyword.lower() in task.title.lower()]
            for task in tasks:
                print(task.to_dict())
        elif choice == "0":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
