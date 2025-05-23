from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    hashed_pw = get_password_hash(user_in.password)
    db_user = models.User(username=user_in.username, hashed_password=hashed_pw)
    print(db_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()

def create_task(db: Session, task_in: schemas.TaskCreate, user_id: int) -> models.Task:
    db_task = models.Task(**task_in.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all()

def get_task_by_id(db: Session, task_id: int, user_id: int) -> models.Task | None:
    return db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == user_id
    ).first()

def update_task(db: Session, task_id: int, user_id: int, task_in: schemas.TaskUpdate) -> models.Task | None:
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        return None
    if task_in.title is not None:
        task.title = task_in.title
    if task_in.description is not None:
        task.description = task_in.description
    if task_in.completed is not None:
        task.completed = task_in.completed
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int, user_id: int) -> bool:
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True