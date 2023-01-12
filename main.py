# import typer
import service
from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from async_alchimy_fastapi.base import get_session
from fastapi import HTTPException
from schemas import *


class DuplicatedEntryError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=422, detail=message)


app = FastAPI()
# cli = typer.Typer()


# @cli.command()
# def db_init_models():
#     asyncio.run(init_models())
#     print("Done")


@app.get("/items", response_model=list[Items_in_store])
async def get_items(session: AsyncSession = Depends(get_session)):
    items = await service.get_items(session)
    return [Items_in_store(id=c.id, name=c.name) for c in items]


@app.post("/sales/")
async def add_sale(sale: SalesIn, session: AsyncSession = Depends(get_session)):
    sale = service.add_sale(session, sale.stores_id, sale.items_id)
    try:
        await session.commit()
        return sale
    except IntegrityError as ex:
        await session.rollback()
        raise DuplicatedEntryError("The sale is already stored")


@app.get("/stores", response_model=list[Stores_list])
async def get_stores(session: AsyncSession = Depends(get_session)):
    store = await service.get_stores(session)
    return [Stores_list(id=c.id, address=c.address) for c in store]


@app.get("/stores/top/", response_model=list[Top_stores])
async def get_top_store(session: AsyncSession = Depends(get_session)):
    try:
        top_stores = await service.get_top_store(session)
        return [Top_stores(id=i, address=a, tottal_rev=s) for i, a, s in top_stores]
    except IntegrityError as ex:
        await session.rollback()
        raise ForeignKeyViolationError("Не корректный запрос")


@app.get("/items/top/", response_model=list[Top_items])
async def get_top_items(session: AsyncSession = Depends(get_session)):
    try:
        top_items = await service.get_top_items(session)
        return [Top_items(id=id, name=name, count=count) for id, name, count in top_items]
    except IntegrityError as ex:
        await session.rollback()
        raise ForeignKeyViolationError("Не корректный запрос")
    finally:
        await session_destroy()


# @app.get("/topstores", response_model=list[Top_stores])
# async def get_list_top_stores(session: AsyncSession = Depends(get_session)):
#     top_store = await service.get_list_top_stores(session)
#     return [Top_stores(id=a.id, address=b.address, tottal_rev=c.tottal_rev) for a, b, c in top_store]

# sl = sales.alias("sl")
# query = select([stores.c.id.label('id'),  # <== рамки вывода
#                 stores.c.address.label('address'),  # <== рамки вывода
#                 func.sum(items.c.price).label('tottal_rev')]  # <== сумирование через func

#                ).join(sl, stores.c.id == sl.c.stores_id
#                       ).join(items, items.c.id == sl.c.items_id  # <== джойны

#                              ).filter(sl.c.create_date >= date.today() + relativedelta(months=-1)
#                                       ).group_by(stores.c.id, stores.c.address
#                                                  ).order_by(desc(literal_column('tottal_rev'))).limit(10)


# if __name__ == "__main__":
#     cli()