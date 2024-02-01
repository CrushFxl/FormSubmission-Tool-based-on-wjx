from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    __tablename__ = 'tasks'
    oid = db.Column('oid', db.TEXT, primary_key=True, unique=True, index=True, nullable=False)
    type = db.Column('type', db.TEXT, nullable=False)
    status = db.Column('status', db.INTEGER, default=400, nullable=False)
    config = db.Column('config', db.JSON, nullable=False)
    unique = db.Column('unique', db.TEXT)


# 保存任务
def save(oid, type, config, unique):
    task = Task(oid=oid, type=type, config=config, unique=unique)
    db.session.add(task)
    db.session.commit()


# 更新任务状态
def update(oid, status):
    task = Task.query.filter(Task.oid == oid).first()
    task.status = status
    db.session.commit()
