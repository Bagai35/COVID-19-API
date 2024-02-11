from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from models.main_models import CovidStatistic, Covid_Statistics_update


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
