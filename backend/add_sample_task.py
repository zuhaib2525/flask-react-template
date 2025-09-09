from app import app, db
from models import Task

with app.app_context():
    task = Task(title="Sample Task for Testing")
    db.session.add(task)
    db.session.commit()
    print(f"Added task with id: {task.id}")
