from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from module_17_1.app.backend.db_depends import get_db
from typing import Annotated
from module_17_1.app.models.task import Task
from module_17_1.app.models.user import User
from module_17_1.app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalars(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.get('/user_id_tasks')
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    else:
        task = db.scalar(select(Task).where(Task.user_id == user_id))
        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
        tasks = db.scalars(select(Task).where(Task.user_id == user_id))
        return list(tasks)


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    try:
        db.execute(insert(User).values(username=create_user.username,
                                       firstname=create_user.firstname,
                                       lastname=create_user.lastname,
                                       age=create_user.age,
                                       slug=slugify(create_user.username)))
        db.commit()
        return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
    except IntegrityError:
        return {'status_code': status.HTTP_304_NOT_MODIFIED, 'reason': 'UNIQUE constraint failed'}


@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], update_user: UpdateUser, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    db.execute(update(User).where(User.id == user_id).values(firstname=update_user.firstname,
                                                             lastname=update_user.lastname,
                                                             age=update_user.age))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    db.execute(delete(User).where(User.id == user_id))
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful'}
