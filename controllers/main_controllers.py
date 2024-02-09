from typing import List

from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from models.main_models import CovidStatistic


class CovidStatistics:

    def get_statistics(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(CovidStatistic).offset(skip).limit(limit).all()

