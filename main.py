from fastapi import FastAPI, Depends, Request, Query
from fastapi.params import Body, Path
from sqlalchemy.orm import Session
from db import SessionLocal, engine, Base, Result, get_db
from fill_db import make_db
from models import ResultModel, ResultAll, AddItem, GetByItemId, TextAnswer, MathAnswer, MathAnswerAll

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from enum_models import SortField, SortOrder, SortFieldNumbers
from sqlalchemy import asc, desc, func


Base.metadata.create_all(bind=engine)
app = FastAPI(title="ТУСУР. ЛР2 Вариант 18. FastAPI", description="Работа с базой данных спортивных соревнований")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



@app.get("/",
         tags=["Информация"],
         summary="Стартовая страница для фронтенда",
         response_class=HTMLResponse)
async def root(request: Request):
    """Информация о БД и АПИ и основной функционал работы с ними."""
    db = next(get_db())
    context = db.query(Result).all()
    context = [str(result) for result in context]
    print(context)
    return templates.TemplateResponse(request=request, name="index.html", context={"data": context})


@app.get("/clear/",
         tags=["Информация"],
         summary="Очистка БД",
         response_model=TextAnswer)
def clear_database():
    """Очистка базы данных и генерация новых данных."""
    make_db()
    return {"message": "Database cleared"}

#CRUD

@app.get("/items/all/", tags=["Предметы из БД"],
         summary="Список всех записей в БД",
         response_model=ResultAll)
async def read_items(mybd: Session = Depends(get_db),
                     sort_by: SortField = Query(None,
                                                title="Сортировка по полю таблицы",
                                                description="Сортировка по полю, по умолчанию - None"),
                     order: SortOrder = Query("asc",
                                              title="Порядок сортировки",
                                              description="Порядок сортировки")):
    """
    Вывод всех позиций из базы данных. Есть возможность отсртировать по полю, если указать его в запросе.
    Также возможно добавить сортировку по возрастанию или убыванию.
    """
    if sort_by:
        if order.value == "asc":
            data = mybd.query(Result).order_by(asc(sort_by.value)).all()
        else:
            data = mybd.query(Result).order_by(desc(sort_by.value)).all()
        print(data)
    else:
        data = mybd.query(Result).all()
    return {"message": "Read all items",
            "totall": len(data),
            "items": [*data]}

@app.post("/items/add/", tags=["Предметы из БД"],
          summary="Добавить обьект в БД",
          description="Добавить обьект в БД")
async def add_item(data: AddItem, mybd: Session = Depends(get_db)):
    data = Result(**data.model_dump())
    mybd.add(data)
    mybd.commit()
    return {"message": f"Done {data}"}

@app.get("/items/del/{item_id}/",
         tags=["Предметы из БД"],
         summary="Удалить обьект из БД по ID",
         response_model=GetByItemId)
async def remove_item(item_id: int = Path(..., title="ID записи", description="ID записи для удаления"),
                      mydb: Session = Depends(get_db)):
    """Удалить обьект из БД по ID"""
    answer = mydb.query(Result).filter(Result.id == item_id).first()
    if answer:
        mydb.query(Result).filter(Result.id == item_id).delete()
        mydb.commit()
        return {"message": f"Deleted item {item_id}",
                "item_id": item_id,
                "item": answer}
    return {"message": f"Not found {item_id}",
                "item_id": item_id,
                "item": answer}

@app.get("/items/{item_id}/",
         tags=["Предметы из БД"],
         summary="Получить обьект по ID",
         response_model=GetByItemId)
async def read_item(item_id: int = Path(..., title="ID записи", description="ID записи для поиска"),
                    mybd: Session = Depends(get_db)):
    """Получить обьект из БД по ID"""
    answer = mybd.query(Result).filter(Result.id == item_id).first()
    if not answer:
        return {"message": "Item not found",
                "item_id": item_id,
                "item": None}
    return {"message": "Read item",
            "item_id": item_id,
            "item": answer}

@app.put("/items/{item_id}/",
         tags=["Предметы из БД"],
         summary="Изменить обьект в БД",
         response_model=GetByItemId)
async def update_item(data: AddItem,
                      item_id: int = Path(..., title="ID записи", description="ID записи для изменения"),
                      mybd: Session = Depends(get_db)):
    """Изменить обьект в БД по ID"""
    answer = mybd.query(Result).filter(Result.id == item_id).first()

    if not answer:
        return {"message": "Item not found",
                "item_id": item_id,
                "item": None}
    for key, value in data.model_dump().items():
        setattr(answer, key, value)
    mybd.commit()

    return {"message": f"Updated item {item_id}",
            "item_id": item_id,
            "item": answer}




# math func
@app.get("/math/max/",
         tags=["Математические функции"],
         summary="Получить максимальное значение",
         response_model=MathAnswer)
async def get_max_value(value: SortFieldNumbers = Query("participants",
                                                        title="Значение для поиска максимального значения",
                                                        description="Значение для поиска максимального значения"),
                        mybd: Session = Depends(get_db)):
    """Получить максимальное значение из поля таблицы. По умолчанию - participants"""
    data = mybd.query(Result).order_by(desc(value)).first()
    return {"message": f"Get MAX value from {value.value} found in ID {data.id}",
            "value": getattr(data, value)}

@app.get("/math/min/",
         tags=["Математические функции"],
         summary="Получить минимальное значение",
         response_model=MathAnswer)
async def get_min_value(value: SortFieldNumbers = Query("participants",
                                                        title="Значение для поиска минимального значения",
                                                        description="Значение для поиска минимального значения"),
                        mybd: Session = Depends(get_db)):
    """Получить минимального значение из поля таблицы. По умолчанию - participants"""
    data = mybd.query(Result).order_by(asc(value)).first()
    return {"message": f"Get MIN value from {value.value} found in ID {data.id}",
            "value": getattr(data, value)}

@app.get("/math/avg/",
         tags=["Математические функции"],
         summary="Получить среднее значение",
         response_model=MathAnswer)
async def get_avg_value(value: SortFieldNumbers = Query("participants",
                                                        title="Значение для поиска среднего значения",
                                                        description="Значение для поиска среднего значения"),
                        mybd: Session = Depends(get_db)):
    """Получить среднее значение из поля таблицы. По умолчанию - participants"""
    data = mybd.query(func.avg(getattr(Result, value.value))).scalar()
    return {"message": f"Get AVG value from {value.value}",
            "value": data}

@app.get("/math/all/",
         tags=["Математические функции"],
         summary="Получить все значения - МИН МАКС СРЕДНЕЕ",
         response_model=MathAnswerAll)
async def get_math_all(mydb: Session = Depends(get_db)):
    """Получить все значения - МИН МАКС СРЕДНЕЕ"""
    attr = [getattr(Result, x.value) for x in SortFieldNumbers]
    num_values = mydb.query(*attr).all()
    rez = list()
    for el in zip([x.value for x in SortFieldNumbers], zip(*num_values)):
        rez.append({"name": el[0],
                   "values": el[1],
                   "min": min(el[1]),
                   "max": max(el[1]),
                   "avg": sum(el[1]) / len(el[1])})
    return {"message": "Get all values",
            "result": rez}