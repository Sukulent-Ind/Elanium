#Настройки баз данных
#////////////////////////////////////////////////////
from sqlalchemy import create_engine

engine = create_engine(
    url="sqlite:///database/db_elanium.db",
    echo=True
)

