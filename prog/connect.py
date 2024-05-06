from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine("postgresql://user:mysecret@localhost:5432/user")
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.drop_all(engine)
# Створюємо знову всі таблиці
Base.metadata.create_all(engine)


if __name__== "seed" :
# Видаляємо всі таблиці, які визначені у моделях
    Base.metadata.drop_all(engine)
# Створюємо знову всі таблиці
    Base.metadata.create_all(engine)