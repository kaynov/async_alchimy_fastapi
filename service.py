from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from models3 import *
from async_alchimy_fastapi.schemas import *
from dateutil.relativedelta import relativedelta
from async_alchimy_fastapi.models import *


async def get_items(session: AsyncSession) -> list[Items]:
    result = await session.execute(select(Items).order_by(Items.name.asc()))
    return result.scalars().all()


def add_sale(session: AsyncSession, stores_id: int, items_id: int):
    new_sale = Sales(stores_id=stores_id, items_id=items_id)
    session.add(new_sale)
    return new_sale


async def get_stores(session: AsyncSession) -> list[Stores_list]:
    result = await session.execute(select(Stores).order_by(Stores.address.asc()))
    return result.scalars().all()


async def get_top_store(session: AsyncSession):
    result = await session.execute(select(Sales.stores_id \
                                          , Stores.address \
                                          , func.sum(Items.price).label('tottal_rev') \
                                          ) \
                                   .join(Stores).join(Items) \
                                   .where(Sales.create_date > date.today() + relativedelta(months=-1))
                                   .group_by(Sales.stores_id, Stores.address) \
                                   .order_by(desc('tottal_rev')) \
                                   .limit(10) \
                                   )
    return result


async def get_top_items(session: AsyncSession) -> list[Items]:
    result = await session.execute(select(Items.id, Items.name, func.count(Sales.items_id).label('count'))\
            .where(Items.id == Sales.items_id)\
            .group_by(Items.id)\
            .order_by(desc('count'))\
            .limit(10)\
            )
    return result


# async def get_list_top_stores(session: AsyncSession) -> list[Top_stores]:
#     result = await session.execute(select([Stores.id.label('id'),
#                     Stores.address.label('address'),
#                     func.sum(Items.price).label('tottal_rev1')
#                     ]).join(Sales, Stores.id == Sales.stores_id
#                        ).join(Items, Items.id == Sales.items_id
#                                    ).filter(Sales.create_date >= date.today() + relativedelta(months=-1)
#                                            ).group_by(Stores.id, Stores.address
#                                                       ).order_by(desc(literal_column('tottal_rev1'))).limit(10))
#     return result.scalars().all()