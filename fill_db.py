from datetime import date
from db import SessionLocal, Result, Base, engine
from random import choice, randint, shuffle, uniform

Base.metadata.create_all(bind=engine)

def make_db():
    competitions = ["Чемпионат России по футболу",
                    "Кубок России по баскетболу",
                    "Всероссийская Спартакиада школьников",
                    "Лыжня России",
                    "Чемпионат России по фигурному катанию",
                    "Турнир имени Ивана Ярыгина (борьба)",
                    "Кубок Кремля (теннис)",
                    "Московский международный марафон",
                    "Чемпионат России по шахматам",
                    "Чемпионат России по волейболу"]

    places = ["Москва",
            "Санкт-Петербург",
            "Казань",
            "Екатеринбург",
            "Новосибирск",
            "Краснодар",
            "Нижний Новгород",
            "Самара",
            "Ростов-на-Дону",
            "Пермь"]

    db = SessionLocal()

    db.query(Result).delete()

    shuffle(competitions)

    for i in range(10):
        result = Result(competition_name=competitions[i], place=choice(places),
                        date=date(randint(2020, 2025), randint(1, 12), randint(1, 28)),
                        participants=randint(100, 2000),
                        ticket_price=round(uniform(100, 4000), 2),
                        prize_pool=randint(10000, 1000000),
                        best_result=round(uniform(10, 100), 3))
        db.add(result)

    db.commit()
    db.close()

if __name__ == "__main__":
    make_db()
    print("Database filled")