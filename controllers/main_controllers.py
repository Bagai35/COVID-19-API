from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from models.main_models import CovidStatistic, Covid_Statistics_update, Location, Continent


class CovidStatistics:

    def get_statistics(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(CovidStatistic).offset(skip).limit(limit).all()

    async def update_statistics(self, db: AsyncSession, CovidStatisticId: int, request: Covid_Statistics_update):
            async with db as session:
                covidStatistic = await session.execute(select(CovidStatistic).filter(CovidStatistic.id == CovidStatisticId))
                covidStatistic = covidStatistic.scalars().first()
                if not covidStatistic:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Covid Statistic not found")

                covidStatistic.new_cases = request.new_cases
                covidStatistic.new_deaths = request.new_deaths
                covidStatistic.population = request.population
                covidStatistic.people_vaccinated = request.people_vaccinated

                await session.commit()
                await session.refresh(covidStatistic)

                return {
                    "id": covidStatistic.id,
                    "new_cases": covidStatistic.new_cases,
                    "new_deaths": covidStatistic.new_deaths,
                    "population": covidStatistic.population,
                    "people_vaccinated": covidStatistic.people_vaccinated
                    # Добавьте другие поля, если они есть
                }

    def get_country_summary_stats(self, db: Session, location_id: int):
        country_summary_stats = db.query(
            func.sum(CovidStatistic.total_cases),
            func.sum(CovidStatistic.total_vaccinations),
            func.sum(CovidStatistic.total_deaths)
        ).filter(CovidStatistic.location_id == location_id).first()
        return country_summary_stats


    async def delete_statistics(self, db: AsyncSession, CovidStatisticId: int):
        async with db as session:
            # Попытка найти запись по id
            covid_statistic = await session.execute(select(CovidStatistic).filter(CovidStatistic.id == CovidStatisticId))
            covid_statistic = covid_statistic.scalars().first()

            # Если запись не найдена, вызываем исключение HTTP 404 Not Found
            if not covid_statistic:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Covid Statistic not found")

            # Удаляем запись
            await session.delete(covid_statistic)
            await session.commit()

            return {"message": "Covid Statistic deleted successfully"}


class ContinentController:
    async def create_continent(self, db: Session, continent_name: str):
        db_continent = Continent(continent=continent_name)
        db.add(db_continent)
        db.commit()
        db.refresh(db_continent)
        return db_continent

    def get_continent_by_name(self, db: Session, continent_name: str):
        continent = db.query(Continent).filter(Continent.continent == continent_name).first()
        return continent.continent_id
    def get_locations_by_continent(self, db: Session, continent_id: int):
        return db.query(Location).filter(Location.continent_id == continent_id).all()

    def get_covid_stats_by_location(self, db: Session, continent_id: int):
        return db.query(CovidStatistic).filter(CovidStatistic.continent_id == continent_id).first()


class LocationController:
    def get_location_by_name(self, db: Session, location_name: str):
        return db.query(Location).filter(Location.location_name == location_name).first()

    def get_location_by_name_id(self, db: Session, location_name: str):
        location = db.query(Location).filter(Location.location_name == location_name).first()
        return location.location_id

    def get_location_by_id(self, db: Session, location_id: int):
        location = db.query(Location).filter(Location.location_id == location_id).first()
        return location.location_id

    def get_covid_stats_by_location(self, db: Session, location_id: int):
        return db.query(CovidStatistic).filter(CovidStatistic.location_id == location_id).first()

    async def create_location(self, db: AsyncSession, location_name: str, iso_code: str, continent_id: int):
        location = Location(location_name=location_name, iso_code=iso_code, continent_id=continent_id)
        db.add(location)
        await db.commit()
        await db.refresh(location)
        return location



class CovidStatisticController:

    def get_country_summary_stats(self, db: Session, location_id: int):
        country_summary_stats = db.query(
            func.sum(CovidStatistic.total_cases),
            func.sum(CovidStatistic.total_vaccinations),
            func.sum(CovidStatistic.total_deaths)
        ).filter(CovidStatistic.location_id == location_id).first()

        total_cases, total_vaccinations, total_deaths = country_summary_stats

        return {
            "total_cases": total_cases,
            "total_vaccinations": total_vaccinations,
            "total_deaths": total_deaths
        }