#Действия над базами данных
#////////////////////////////////////////////////////
from database.models import Base, TaskBase, InfoBase
from database.conf import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

Session = sessionmaker(engine)

def create_db_and_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with Session() as session:
        session.add(InfoBase(data="Current_tasks", val=0))
        session.add(InfoBase(data="Solved_tasks", val=0))
        session.add(InfoBase(data="Failed_tasks", val=0))
        session.commit()


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

            stmt = select(TaskBase)
            db_object = session.scalars(stmt).all()

            cur_id = 1
            for task in db_object:
                if cur_id != task.id:
                    task.id = cur_id
                    session.merge(task)
                cur_id += 1

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


def update_cur_value(n: int):
    with Session() as session:
        try:
            stmt = select(InfoBase).where(InfoBase.data == "Current_tasks")
            db_object = session.scalars(stmt).one()

            db_object.val += n
            session.merge(db_object)

        except:
            session.rollback()
            raise

        else:
            session.commit()


def update_solv_value():
    with Session() as session:
        try:
            stmt = select(InfoBase).where(InfoBase.data == "Solved_tasks")
            db_object = session.scalars(stmt).one()

            db_object.val += 1
            session.merge(db_object)

        except:
            session.rollback()
            raise

        else:
            session.commit()

def update_fail_value():
    with Session() as session:
        try:
            stmt = select(InfoBase).where(InfoBase.data == "Failed_tasks")
            db_object = session.scalars(stmt).one()

            db_object.val += 1
            session.merge(db_object)

        except:
            session.rollback()
            raise

        else:
            session.commit()

def get_cur():
    with Session() as session:
        stmt = select(InfoBase).where(InfoBase.data == "Current_tasks")
        db_object = session.scalars(stmt).one()
        return db_object.val

def get_solv():
    with Session() as session:
        stmt = select(InfoBase).where(InfoBase.data == "Solved_tasks")
        db_object = session.scalars(stmt).one()
        return db_object.val

def get_fail():
    with Session() as session:
        stmt = select(InfoBase).where(InfoBase.data == "Failed_tasks")
        db_object = session.scalars(stmt).one()
        return db_object.val

def work_with_info(data: str, operation: str, n=0):
    if data == "cur":
        if operation == "upd":
            update_cur_value(n)

        if operation == "get":
            return get_cur()

    if data == "solv":
        if operation == "upd":
            update_solv_value()

        if operation == "get":
            return get_solv()

    if data == "fail":
        if operation == "upd":
            update_fail_value()

        if operation == "get":
            return get_fail()



# create_db_and_tables()
# add_task("re", "i d leave", "123")
# delete_task(3)

#
# print(get_all_tasks())
# work_with_info("cur", "upd", 2)
# print(work_with_info("cur", "get"))