from datetime import datetime
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = "tmp/nutritionist.db"

# --- Configuração ORM ---
Base = declarative_base()
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

# --- Modelo ORM ---
class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(20))
    time = Column(String(10))
    description = Column(String(255))
    calories = Column(Integer)

# --- Inicializa banco ---
def init_db():
    Base.metadata.create_all(engine)

# --- Adiciona refeição ---
def add_meal(description: str, calories: int):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M")

    session = SessionLocal()
    try:
        meal = Meal(date=date, time=time, description=description, calories=calories)
        session.add(meal)
        session.commit()
    finally:
        session.close()

# --- Refeições do dia ---
def get_meals_today():
    session = SessionLocal()
    try:
        date = datetime.now().strftime("%Y-%m-%d")
        meals = session.query(Meal).filter(Meal.date == date).order_by(Meal.time.asc()).all()

        if not meals:
            return "🍽️ Você ainda não registrou refeições hoje."

        total = sum(m.calories for m in meals)
        resumo = [f"- {m.time} | {m.description} (~{m.calories} kcal)" for m in meals]

        return "🍽️ Refeições de hoje:\n" + "\n".join(resumo) + f"\n\n🔥 Total acumulado: {total} kcal"
    finally:
        session.close()

# --- Total de calorias do dia ---
def get_total_today():
    session = SessionLocal()
    try:
        date = datetime.now().strftime("%Y-%m-%d")
        total = session.query(Meal).filter(Meal.date == date).with_entities(Meal.calories).all()
        return sum([c[0] for c in total]) if total else 0
    finally:
        session.close()

# --- Calorias restantes ---
def get_remaining_calories(daily_goal: int):
    consumed = get_total_today()
    remaining = daily_goal - consumed
    if remaining <= 0:
        return 0, consumed
    return remaining, consumed
