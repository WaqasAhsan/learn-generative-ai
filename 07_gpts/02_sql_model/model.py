from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select, delete

# https://sqlmodel.tiangolo.com/tutorial/delete/


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


engine = create_engine(
    "postgresql://hawkhere:8cxCnEDsYj1q@ep-dark-math-37799263.us-east-2.aws.neon.tech/neondb?sslmode=require", echo=True)


def create_database_and_tables():
    """
    Creates a database by creating all tables defined in the SQLModel metadata using the provided engine.
    """
    SQLModel.metadata.create_all(engine)


def add_data():
    """
    A function to add data to the database using a session object.
    """
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.commit()

# get data from the database


def get_all_data():
    """
    A function to retrieve all data from the database using the Hero table.
    """
    with Session(engine) as session:
        statement = select(Hero)
        results = session.exec(statement)
        for result in results:
            print(result)


def get_data():
    """
    This function retrieves data using a database session and prints the results.
    """
    with Session(engine) as session:
        statement = select(Hero).where(Hero.age == None)
        results = session.exec(statement)
        for result in results:
            print(result)

#  update data


def update_data():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.age == 6)
        results = session.exec(statement)
        for result in results:
            result.age = 7
            session.commit()
            print(result)

#  delete data


def delete_data():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.age == None)
        result = session.exec(statement)
        result = result.one()
        session.delete(result)
        session.commit()
        print(f"Delete Object : {result}")


if __name__ == "__main__":
    # get_all_data()
    # get_data()
    # update_data()
    delete_data()
