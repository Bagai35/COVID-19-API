from typing import List, Union


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from auth.database import get_db, User
from auth.schemas import UpdateUserData
from config_db.database__ITEM import get_sync_db


from fastapi.responses import JSONResponse

from controllers.main_controllers import CovidStatistics, LocationController, ContinentController

from sqlalchemy.future import select

from models.main_models import Covid_Statistics_update, Location, Location_post
from routers.test_auth_router import current_user

covid_controller = CovidStatistics()
location_controller = LocationController()
continent_controller = ContinentController()



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

@router.get("/statistics/", response_class=JSONResponse, tags=["covid"])
def read_statistics(skip: int = 0, limit: int = 100, db: Session = Depends(get_sync_db)):
    covid = covid_controller.get_statistics(db, skip=skip, limit=limit)
    return covid

@router.put("/covid/statistic/{CovidStatisticId}", response_model=dict, tags=["admin"])
async def Update_Statistics(CovidStatisticId: int, request: Covid_Statistics_update, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user_role)):
    CovidStatistic = await covid_controller.update_statistics(db, CovidStatisticId, request)
    return CovidStatistic

@router.delete("/covid/statistics/delete/{CovidStatisticId}", response_model=dict, tags=["admin"])
async def delete_statistics(
    CovidStatisticId: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_role)
):
    try:
        result = await covid_controller.delete_statistics(db, CovidStatisticId)
        return result
    except HTTPException as e:
        return e



@router.put("/user/update", response_model=None, tags=["admin"])
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


@router.get("/stats/summry/location/{location_id}", response_model=dict, tags=["statistic"])
def read_country_summary_stats(location_id: int, db: Session = Depends(get_sync_db)):
    location = location_controller.get_location_by_id(db, location_id)

    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    stat = covid_controller.get_country_summary_stats(db, location)

    total_cases, total_vaccinations, total_deaths = stat

    return {
        "total_cases": total_cases,
        "total_vaccinations": total_vaccinations,
        "total_deaths": total_deaths
    }

@router.get("/continent/stats/{country_name}", response_model=dict, tags=["continents & locations"])
def get_continent_stats(continent_name: str, db: Session = Depends(get_sync_db)):
    continent = continent_controller.get_continent_by_name(db, continent_name)
    if not continent:
        raise HTTPException(status_code=404, detail="Country not found")

    covid_stats = continent_controller.get_covid_stats_by_location(db, continent)

    return {"country": continent_name, "covid_stats": covid_stats}


@router.get("/location/stats/{location_name}", response_model=dict, tags=["continents & locations"])
def get_location_stats(location_name: str, db: Session = Depends(get_sync_db)):
    location = location_controller.get_location_by_name_id(db, location_name)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    covid_stats = location_controller.get_covid_stats_by_location(db, location)

    return {"location": location_name, "covid_stats": covid_stats}


@router.get("/continent/locations/{continent_name}", response_model=dict, tags=["continents & locations"])
def get_locations_by_continent(continent_name: str, db: Session = Depends(get_sync_db)):
    continent_id = continent_controller.get_continent_by_name(db, continent_name)
    if not continent_id:
        raise HTTPException(status_code=404, detail="Continent not found")

    locations = continent_controller.get_locations_by_continent(db, continent_id)
    return {"continent": continent_id, "locations": locations}


@router.post("/location/create", response_model=dict, tags=["admin"])
async def create_location(location_name: str, iso_code: str, continent_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user_role)):
    location = await location_controller.create_location(db, location_name, iso_code, continent_id)
    location_name = location.location_name
    location_iso = location.iso_code
    location_continent = location.continent_id
    return {"Locataion: ": location_name, "Continent: ": location_continent, "ISO: ": location_iso}

@router.delete("/location/delete/{location_id}", response_model=dict, tags=["admin"])
async def delete_location(
    location_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_role)
):
    try:
        result = await covid_controller.delete_statistics(db, location_id)
        return result
    except HTTPException as e:
        return e