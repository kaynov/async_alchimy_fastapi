from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import func
from async_alchimy_fastapi.base import Base


class Sales(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True)
    stores_id = Column(ForeignKey("stores.id"))
    items_id = Column(ForeignKey("items.id"))
    create_date = Column(DateTime, server_default=func.now())


class Items(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)


class Stores(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True)
    address = Column(String)
