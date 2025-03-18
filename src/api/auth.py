from fastapi import Query, APIRouter, Body

from passlib.context import CryptContext

from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def create_user(data: UserRequestAdd):
    hashed_password = pwd_context.hash(data.password)
    new_user = UserAdd(
        email=data.email,
        hashed_password=hashed_password,
        first_name=data.first_name,
        last_name=data.last_name
    )
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user)
        await session.commit()

    return {"Success": "True"}