from datetime import datetime
from typing import Optional, Union, List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class CovidStatistic(Base):

    __tablename__ = "covid_statistic"


    id = Column(Integer, primary_key=True, autoincrement=True)
    continent_id = Column(Integer, ForeignKey('continent.continent_id'))
    location_id = Column(Integer, ForeignKey('location.location_id'))
    date = Column(Date)
    total_cases = Column(Float)
    new_cases = Column(Float)
    total_deaths = Column(Float)
    new_deaths = Column(Float)
    new_deaths_smoothed = Column(Float)
    total_cases_per_million = Column(Float)
    new_cases_per_million = Column(Float)
    new_cases_smoothed_per_million = Column(Float)
    total_deaths_per_million = Column(Float)
    new_deaths_per_million = Column(Float)
    new_deaths_smoothed_per_million = Column(Float)
    reproduction_rate = Column(Float)
    icu_patients = Column(Float)
    icu_patients_per_million = Column(Float)
    hosp_patients = Column(Float)
    hosp_patients_per_million = Column(Float)
    weekly_icu_admissions = Column(Float)
    weekly_icu_admissions_per_million = Column(Float)
    weekly_hosp_admissions = Column(Float)
    weekly_hosp_admissions_per_million = Column(Float)
    total_tests = Column(Float)
    new_tests = Column(Float)
    total_tests_per_thousand = Column(Float)
    new_tests_per_thousand = Column(Float)
    new_tests_smoothed = Column(Float)
    new_tests_smoothed_per_thousand = Column(Float)
    positive_rate = Column(Float)
    tests_per_case = Column(Float)
    tests_units = Column(String(255))
    total_vaccinations = Column(Float)
    people_vaccinated = Column(Float)
    people_fully_vaccinated = Column(Float)
    total_boosters = Column(Float)
    new_vaccinations = Column(Float)
    new_vaccinations_smoothed = Column(Float)
    total_vaccinations_per_hundred = Column(Float)
    people_vaccinated_per_hundred = Column(Float)
    people_fully_vaccinated_per_hundred = Column(Float)
    total_boosters_per_hundred = Column(Float)
    new_vaccinations_smoothed_per_million = Column(Float)
    new_people_vaccinated_smoothed = Column(Float)
    new_people_vaccinated_smoothed_per_hundred = Column(Float)
    stringency_index = Column(Float)
    population_density = Column(Float)
    median_age = Column(Float)
    aged_65_older = Column(Float)
    aged_70_older = Column(Float)
    gdp_per_capita = Column(Float)
    extreme_poverty = Column(Float)
    cardiovasc_death_rate = Column(Float)
    diabetes_prevalence = Column(Float)
    female_smokers = Column(Float)
    male_smokers = Column(Float)
    handwashing_facilities = Column(Float)
    hospital_beds_per_thousand = Column(Float)
    life_expectancy = Column(Float)
    human_development_index = Column(Float)
    population = Column(Float)
    excess_mortality_cumulative_absolute = Column(Float)
    excess_mortality_cumulative = Column(String(255))
    excess_mortality = Column(String(255))
    excess_mortality_cumulative_per_million = Column(Float)

class Location(Base):

    __tablename__ = "location"


    location_id = Column(Integer, primary_key=True, autoincrement=True)
    location_name = Column(String(255))
    iso_code = Column(String(255))
    continent_id = Column(Integer, ForeignKey('continent.continent_id'))  # Foreign key referencing Continent
    covid_statistics = relationship('CovidStatistic',backref='location')  # One-to-many relationship with CovidStatistic

class Continent(Base):

    __tablename__ = "continent"

    continent_id = Column(Integer, primary_key=True, autoincrement=True)
    continent = Column(String(255))
    locations = relationship('Location', backref='continent')  # Establishing the one-to-many relationship


class Covid_Statistics_update(BaseModel):

    new_cases: float
    new_deaths: float
    population: float
    people_vaccinated: float