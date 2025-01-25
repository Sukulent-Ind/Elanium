#Действия над базами данных
#////////////////////////////////////////////////////
from models import Base, TaskBase
from conf import engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(engine)

def create_db_and_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def add_task(shrt, expl, deadl):
    with Session() as session:
        try:
            session.add(TaskBase(short_name=shrt, explain=expl, deadline=deadl, creation_date="-1"))
        except:
            session.rollback()
            raise
        else:
            session.commit()

