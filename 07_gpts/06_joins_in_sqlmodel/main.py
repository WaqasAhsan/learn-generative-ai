from typing import Optional

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
# is it from online class 5 at 31 Jan 2024?
# now adding more features in it.
from dotenv import load_dotenv, find_dotenv
from os import getenv

_: bool = load_dotenv(find_dotenv())
app = FastAPI()


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")

# create a team table with fields id, name and headquarters.


class Team(SQLModel, table=True):
    '''
    created a team table with fields id, name and headquarters.
    '''
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(index=True)
    headquarters: str


# database_url = "postgresql://ziaukhan:oSLz91i@ep-little-frog-313391.us-east-2.aws.neon.tech/neondb?sslmode=require"
database_url = getenv("DATABASE_URL")

connect_args = {"check_same_thread": False}
engine = create_engine(database_url, echo=True)
# engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


# @app.post("/heroes/")
def create_heroes():
    with Session(engine) as session:
        team_avengers = Team(name="Avengers", headquarters="Avengers Tower")
        team_justice_league = Team(
            name="Justice League", headquarters="Justice League Tower")

        session.add(team_avengers)
        session.add(team_justice_league)
        session.commit()

        hero_superman = Hero(secret_name="Superman",
                             name="Clark Kent", age=35, team_id=team_justice_league.id)
        hero_batman = Hero(secret_name="Batman",
                           name="Bruce Wayne", age=30, team_id=team_justice_league.id)
        hero_spiderman = Hero(
            secret_name="Spiderman", name="Peter Parker", age=25, team_id=team_avengers.id)
        hero_ironman = Hero(secret_name="Ironman",
                            name="Tony Stark", age=40, team_id=team_avengers.id)
        session.add(hero_superman)
        session.add(hero_batman)
        session.add(hero_spiderman)
        session.add(hero_ironman)
        session.commit()


def select_heros_by_where():
    with Session(engine) as session:
        heroes = session.exec(select(Hero).where(Hero.team_id == 2)).all()
        print(heroes)
        return heroes


def selec_heros_by_join():
    with Session(engine) as session:
        heroes = session.exec(select(Hero).join(
            Team).where(Hero.team_id == 1)).all()
        print(heroes)
        return heroes


def select_heros_by_left():
    with Session(engine) as session:
        heroes = session.exec(select(Hero).join(Team, isouter=True)).all()
        print(heroes)
        return heroes


def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.secret_name ==
                                       "Batman")
        results = session.exec(statement)
        for result in results:
            result.team_id = 1
            session.commit()
            print(result)


def delete_heros():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.secret_name == "Batman")
        results = session.exec(statement)
        for result in results:
            session.delete(result)
            session.commit()
            print(result)


def remove_heros():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.secret_name == "Spiderman")
        result = session.exec(statement).one()
        result.team_id = None
        session.commit()


def main():
    # create_db_and_tables()
    # create_heroes()
    # select_heros_by_where()
    # selec_heros_by_join()
    # select_heros_by_left()
    # update_heroes()
    # delete_heros()
    remove_heros()


if __name__ == "__main__":
    main()
