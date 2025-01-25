#Действия над базами данных
#////////////////////////////////////////////////////
from database.models import Base, TaskBase
from database.conf import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update

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


def get_task_by_id(id: int) -> dict:
    with Session() as session:
        stmt = select(TaskBase).where(TaskBase.id == id)
        db_object = session.scalars(stmt).one()

        res = {
            "id": db_object.id,
            "short_name": db_object.short_name,
            "explain": db_object.explain,
            "creation_date": db_object.creation_date,
            "deadline": db_object.deadline
        }

        return res


def delete_task(id: int) -> TaskBase:
    with Session() as session:
        try:
            stmt = select(TaskBase).where(TaskBase.id == id)
            db_object = session.scalars(stmt).one()

            session.delete(db_object)

        except:
            session.rollback()
            raise
        else:
            session.commit()


def get_all_tasks():
    with Session() as session:
        stmt = select(TaskBase)
        db_object = session.scalars(stmt).all()

        return [{"id": task.id, "short_name": task.short_name} for task in db_object]


# create_db_and_tables()
# add_task("re", "i d leave", "123")
# delete_task(1)
# print(get_all_tasks())