import sys
from datetime import date, timedelta
import random

from faker import Faker

from flask import current_app
from meep import create_app
from meep.models import db
from meep.models import Owner, Project
from config import DevelopmentConfig


def clear_db():
    app = create_app(DevelopmentConfig)
    with app.app_context():
        db.drop_all()
        db.session.commit()


def random_address(fake):
    states = ('KS', 'MO')
    state = random.choice(states)
    return Address(
        address=fake.street_address(),
        city=fake.city_name(),
        state=state,
        zip=fake.zipcode_in_state(state_abbr=state)
    )


def random_coordinate(fake):
    return Coordinate(
        lat=fake.lat(),
        long=fake.lng()
    )



def random_fuel_type():
    fuel_types=['PROPANE', 'ELECTRIC', 'CNG', 'BIODIESEL05', 'BIODIESEL20']
    return FuelType(
        fuel=random.choice(fuel_types)
    )


def random_owner(fake):
    return Owner(
        name=fake.name()
    )


def random_project(fake):
    project_types = ['Fleet', 'Fuel Station', 'Building']
    return Project(
        name=fake.company(),
        start_date=fake.date_between(
            start_date="-8y",
            end_date="-1y"
        ),
        duration=fake.time_delta(end_datetime=date.today()),
        project_type=random.choice(project_types),
        summary=fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None)
    )


def random_radius():
    return Radius(
        radius=20*random.random() + 1
    )


def random_site():
    return Site(
        GGE_reduced=2000*random.random(),
        GHG_reduced=100*random.random()
    )


def seed_db():


    app = create_app(DevelopmentConfig)
    print(app)
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    fake = Faker()
    fake.seed(42)


    clear_db()

    with app.app_context():
        db.create_all()
        
        addresses = [random_address(fake) for i in range(5)]
        coordinates = [random_coordinate(fake) for i in range(10)]
        fuels = [random_fuel_type(fake) for i in range(5)]
        owners = [random_owner(fake) for i in range(5)]
        rads = [random_radius() for i in range(5)]
        sites = [random_site() for i in range(5)]
        projects = [random_project(fake) for i in range(5)]




        for objects in [addresses, coordinates, fuels, owners, rads,
                        sites, projects]:
                        db.session.bulk_save_objects(objects)

        db.session.commit()






if __name__ == '__main__':
    if 'drop' in sys.argv and sys.argv[1] == 'drop':
        clear_db()
    else:
        seed_db()
