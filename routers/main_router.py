from typing import List, Union


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from auth.database import get_db, User
from auth.schemas import UpdateUserData
from config_db.database__ITEM import get_sync_db


from fastapi.responses import JSONResponse

from controllers.main_controllers import CovidStatistics

from sqlalchemy.future import select

from models.main_models import Covid_Statistics_update
from routers.test_auth_router import current_user

covid_controller = CovidStatistics()

router = APIRouter()

def get_current_user(user: User = Depends(current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

def get_current_user_role(user: User = Depends(get_current_user)):
    # Предположим, что у вас есть поле "role" в модели User, которое определяет роль пользователя
    if user.role_id != 1:  # Замените "admin" на вашу роль
        raise HTTPException(status_code=403, detail="YOU DON'T ADMIN")
    return user

@router.get("/statistics/", response_class=JSONResponse)
def read_statistics(skip: int = 0, limit: int = 100, db: Session = Depends(get_sync_db)):
    covid = covid_controller.get_statistics(db, skip=skip, limit=limit)
    return covid

@router.put("/covid_Statistic/{CovidStatisticId}", response_model=Covid_Statistics_update)
async def update_author_route(CovidStatisticId: int, request: Covid_Statistics_update, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user_role)):
    CovidStatistic = await covid_controller.update_statistics(db, CovidStatisticId, request)
    return CovidStatistic
#
#

#
@router.put("/user/update", response_model=None)
def update_user_data(
        verify_account_name: str,
    updated_data: UpdateUserData,
    current_user: User = Depends(get_current_user)
):
    # Проверяем, что пользователь пытается обновить свой собственный профиль
    if verify_account_name != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You can only update your own profile data."
        )

    # Обновляем данные пользователя
    current_user.username = updated_data.username
    current_user.email = updated_data.email

    # Здесь вы можете сохранить обновленные данные в вашем хранилище, например, в базе данных

    # Возвращаем обновленные данные пользователя
    return current_user
