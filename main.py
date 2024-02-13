import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy import create_engine, Column
from sqlalchemy import inspect


main =Flask(__name__)
main.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/covid'
main.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db_uri = 'mysql+pymysql://root@localhost/covid'
db.init_app(main)
if not database_exists(db_uri):
    create_database(db_uri)
engine = create_engine(db_uri)
Base = declarative_base()
Base.metadata.create_all(engine)





class CovidStatistic(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    continent_id = db.Column(db.Integer, db.ForeignKey('continent.continent_id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'))
    date = db.Column(db.Date)
    new_cases = db.Column(db.Float)
    new_deaths = db.Column(db.Float)
    reproduction_rate = db.Column(db.Float)
    icu_patients = db.Column(db.Float)
    hosp_patients = db.Column(db.Float)
    weekly_icu_admissions = db.Column(db.Float)
    weekly_icu_admissions_per_million = db.Column(db.Float)
    weekly_hosp_admissions = db.Column(db.Float)
    weekly_hosp_admissions_per_million = db.Column(db.Float)
    new_tests = db.Column(db.Float)
    positive_rate = db.Column(db.Float)
    tests_per_case = db.Column(db.Float)
    tests_units = db.Column(db.String(255))
    people_vaccinated = db.Column(db.Float)
    people_fully_vaccinated = db.Column(db.Float)
    total_boosters = db.Column(db.Float)
    new_vaccinations = db.Column(db.Float)
    new_vaccinations_smoothed = db.Column(db.Float)
    people_vaccinated_per_hundred = db.Column(db.Float)
    people_fully_vaccinated_per_hundred = db.Column(db.Float)
    new_vaccinations_smoothed_per_million = db.Column(db.Float)
    stringency_index = db.Column(db.Float)
    population_density = db.Column(db.Float)
    median_age = db.Column(db.Float)
    aged_65_older = db.Column(db.Float)
    aged_70_older = db.Column(db.Float)
    gdp_per_capita = db.Column(db.Float)
    extreme_poverty = db.Column(db.Float)
    cardiovasc_death_rate = db.Column(db.Float)
    diabetes_prevalence = db.Column(db.Float)
    female_smokers = db.Column(db.Float)
    male_smokers = db.Column(db.Float)
    handwashing_facilities = db.Column(db.Float)
    hospital_beds_per_thousand = db.Column(db.Float)
    life_expectancy = db.Column(db.Float)
    human_development_index = db.Column(db.Float)
    population = db.Column(db.Float)
    excess_mortality_cumulative_absolute = db.Column(db.Float)
    excess_mortality_cumulative = db.Column(db.String(255))
    excess_mortality = db.Column(db.String(255))
    excess_mortality_cumulative_per_million = db.Column(db.Float)


class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_name = db.Column(db.String(255))
    iso_code = db.Column(db.String(255))
    continent_id = db.Column(db.Integer, db.ForeignKey('continent.continent_id'))  # Foreign key referencing Continent
    covid_statistics = db.relationship('CovidStatistic',backref='location')  # One-to-many relationship with CovidStatistic

class Continent(db.Model):
    continent_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    continent = db.Column(db.String(255))
    locations = db.relationship('Location', backref='continent')  # Establishing the one-to-many relationship









def insert_data_from_json(file_name):
    Session = sessionmaker(bind=engine)
    session = Session()
    with open(file_name, 'r') as json_file:
        data = json.load(json_file)

        # Изменяем способ обработки данных JSON
        records = data[0]

        for record_data in records.values():
            # Создаем новый объект CovidStatistic и заполняем его данными
            covid_statistic = CovidStatistic()

            # Устанавливаем значения атрибутов CovidStatistic из данных JSON
            covid_statistic.date = datetime.strptime(record_data.get('date'), '%Y-%m-%d')
            covid_statistic.new_cases = record_data.get('new_cases')
            covid_statistic.new_deaths = record_data.get('new_deaths')
            covid_statistic.reproduction_rate = record_data.get('reproduction_rate')
            covid_statistic.icu_patients = record_data.get('icu_patients')
            covid_statistic.hosp_patients = record_data.get('hosp_patients')
            covid_statistic.weekly_icu_admissions = record_data.get('weekly_icu_admissions')
            covid_statistic.weekly_hosp_admissions = record_data.get('weekly_hosp_admissions')
            covid_statistic.new_tests = record_data.get('new_tests')
            covid_statistic.positive_rate = record_data.get('positive_rate')
            covid_statistic.tests_units = record_data.get('tests_units')
            covid_statistic.people_vaccinated = record_data.get('people_vaccinated')
            covid_statistic.people_fully_vaccinated = record_data.get('people_fully_vaccinated')
            covid_statistic.new_vaccinations = record_data.get('new_vaccinations')
            covid_statistic.stringency_index = record_data.get('stringency_index')
            covid_statistic.population_density = record_data.get('population_density')
            covid_statistic.aged_65_older = record_data.get('aged_65_older')
            covid_statistic.aged_70_older = record_data.get('aged_70_older')
            covid_statistic.gdp_per_capita = record_data.get('gdp_per_capita')
            covid_statistic.extreme_poverty = record_data.get('extreme_poverty')
            covid_statistic.cardiovasc_death_rate = record_data.get('cardiovasc_death_rate')
            covid_statistic.diabetes_prevalence = record_data.get('diabetes_prevalence')
            covid_statistic.female_smokers = record_data.get('female_smokers')
            covid_statistic.male_smokers = record_data.get('male_smokers')
            covid_statistic.handwashing_facilities = record_data.get('handwashing_facilities')
            covid_statistic.life_expectancy = record_data.get('life_expectancy')
            covid_statistic.human_development_index = record_data.get('human_development_index')
            covid_statistic.population = record_data.get('population')
            covid_statistic.excess_mortality_cumulative_absolute = record_data.get(
                'excess_mortality_cumulative_absolute')
            covid_statistic.excess_mortality_cumulative = record_data.get('excess_mortality_cumulative')
            covid_statistic.excess_mortality = record_data.get('excess_mortality')

            # Получаем данные о местоположении и континенте из записи
            location_name = record_data.get('location')
            continent_name = record_data.get('continent')

            # Поиск или создание местоположения
            if location_name:
                existing_location = session.query(Location).filter_by(location_name=location_name).first()
                if existing_location is None:
                    # Создаем новое местоположение
                    location = Location(location_name=location_name, iso_code=record_data.get('iso_code'))
                    if continent_name:
                        # Поиск или создание континента и связывание с местоположением
                        existing_continent = session.query(Continent).filter_by(continent=continent_name).first()
                        if existing_continent is None:
                            continent = Continent(continent=continent_name)
                            session.add(continent)
                            session.flush()  # Сбрасываем изменения для получения ID
                            location.continent_id = continent.continent_id
                        else:
                            location.continent_id = existing_continent.continent_id
                    session.add(location)
                    session.flush()  # Сбрасываем изменения для получения ID
                    covid_statistic.location_id = location.location_id
                else:
                    covid_statistic.location_id = existing_location.location_id
                    existing_location.iso_code = record_data.get('iso_code')  # Обновление iso_code
            else:
                covid_statistic.location_id = None

            # Поиск или создание континента
            if continent_name and not covid_statistic.continent_id:
                existing_continent = session.query(Continent).filter_by(continent=continent_name).first()
                if existing_continent is None:
                    continent = Continent(continent=continent_name)
                    session.add(continent)
                    session.flush()  # Сбрасываем изменения для получения ID
                    covid_statistic.continent_id = continent.continent_id
                else:
                    covid_statistic.continent_id = existing_continent.continent_id

            # Добавляем объект CovidStatistic в сессию
            session.add(covid_statistic)

        # Фиксируем изменения и закрываем сессию
        session.commit()
        session.close()







if __name__ == '__main__':
    with main.app_context():
        db.create_all()
        insert_data_from_json('Covid1.json')

    main.run(debug=False)







