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


