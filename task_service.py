from sqlalchemy.orm import Session
from model import Task
from schema import TaskCreate, TaskUpdate


def get_all_tasks(db: Session):
    return db.query(Task).all()

def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def search_tasks_by_status(db: Session, status: str):
    return db.query(Task).filter(Task.status.contains(status)).all()

def create_task(db: Session, task_data: TaskCreate) -> Task:
    db_task = Task(
        title=task_data.title,
        assignee_name=task_data.assignee_name,
        priority=task_data.priority,
        status=task_data.status
    )
    db.add(db_task)
    return db_task

def update_task(db: Session, db_task: Task, task_data: TaskUpdate) -> Task:
    db_task.title = task_data.title
    db_task.assignee_name = task_data.assignee_name
    db_task.priority = task_data.priority
    db_task.status = task_data.status
    return db_task

def delete_task(db: Session, db_task: Task):
    db.delete(db_task)
