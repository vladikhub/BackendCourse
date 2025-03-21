from os import access

from fastapi import Query, APIRouter, Body, HTTPException, Depends
from fastapi import Response, Request

from src.api.dependencies import UserIdDep
from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestRegister, UserLogin, UserRegister
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post("/register")
async def register_user(data: UserRequestRegister):
    hashed_password = AuthService().hash_password(data.password)
    new_user = UserRegister(
        email=data.email,
        hashed_password=hashed_password,
        first_name=data.first_name,
        last_name=data.last_name
    )
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user)
        await session.commit()
    return {"Success": "True"}

@router.post("/login")
async def login_user(
        data: UserLogin,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        await session.commit()
    return {"access_token": access_token}

# jwt.exceptions.ExpiredSignatureError: Signature has expired


@router.get("/me")
async def get_me(user_id: UserIdDep):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}