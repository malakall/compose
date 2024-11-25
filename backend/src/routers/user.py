from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from schemas.user import UserInfo, CreateUser, UpdateUser

from db import Database
from models.user import User

router = APIRouter()


@router.get("", response_model=UserInfo)
async def get_user(user_id: int):
    q = select(User).where(User.id == user_id)
    
    with Database() as db:
        user = db.scalars(q).first()
        if user is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return UserInfo(
            id=user.id,
            name=user.name,
            age=user.age,
            male=user.male
        )
    

@router.get("/all", response_model=List[UserInfo])
async def get_user():
    q = select(User)
    
    users = []
    with Database() as db:
        for user in db.scalars(q).all():
            users.append(UserInfo(
                id=user.id,
                name=user.name,
                age=user.age,
                male=user.male
            )
        )
            
    return users


@router.post("", status_code=status.HTTP_201_CREATED, response_model=int)
async def create_user(data: CreateUser):
    user = User()
    user.name = data.name
    user.age = data.age
    user.male = data.male

    with Database() as db:
        db.add(user)
        db.flush()
        user_id = user.id
        db.commit()

    return user_id


@router.put("", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(user_id: int, data: UpdateUser):
    q = select(User).where(User.id == user_id)
    
    with Database() as db:
        user = db.scalars(q).first()
        if user is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if data.name is not None:
            user.name = data.name
        if data.age is not None:
            user.age = data.age
        if data.male is not None:
            user.male = data.male

        db.commit()

    return user_id


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    q = select(User).where(User.id == user_id)
    
    with Database() as db:
        user = db.scalars(q).first()
        if user is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        db.delete(user)
        db.commit()
