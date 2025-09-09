from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from storage.models import Base, AgentSession, Meal
from datetime import datetime

class SqliteStorage:
    def __init__(self, db_path="tmp/nutritionist.db"):
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False, future=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)

    # -------- Conversas --------
    def save_message(self, role: str, content: str):
        session = self.Session()
        try:
            msg = AgentSession(role=role, content=content)
            session.add(msg)
            session.commit()
        finally:
            session.close()

    def get_history(self, limit=10):
        session = self.Session()
        try:
            msgs = session.query(AgentSession).order_by(AgentSession.timestamp.desc()).limit(limit).all()
            return [(m.role, m.content) for m in reversed(msgs)]
        finally:
            session.close()

    # -------- Refeições --------
    def add_meal(self, description: str, calories: int):
        session = self.Session()
        try:
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            time = now.strftime("%H:%M")
            period = self.classify_meal_period(now.hour)

            meal = Meal(date=date, time=time, period=period,
                        description=description, calories=calories)
            session.add(meal)
            session.commit()
        finally:
            session.close()

    def get_meals_today(self):
        session = self.Session()
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            meals = session.query(Meal).filter(Meal.date == today).order_by(Meal.time.asc()).all()

            if not meals:
                return "🍽️ Você ainda não registrou refeições hoje."

            total = sum(m.calories for m in meals)
            resumo = [f"- {m.time} | {m.period}: {m.description} (~{m.calories} kcal)" for m in meals]
            return "🍽️ Refeições de hoje:\n" + "\n".join(resumo) + f"\n\n🔥 Total acumulado: {total} kcal"
        finally:
            session.close()

    def get_total_today(self):
        session = self.Session()
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            total = session.query(Meal).filter(Meal.date == today).with_entities(Meal.calories).all()
            return sum([c[0] for c in total]) if total else 0
        finally:
            session.close()

    # -------- Auxiliar --------
    def classify_meal_period(self, hour: int) -> str:
        if 5 <= hour <= 10:
            return "Café da manhã ☀️"
        elif 11 <= hour <= 14:
            return "Almoço 🍲"
        elif 15 <= hour <= 17:
            return "Lanche da tarde 🍪"
        elif 18 <= hour <= 21:
            return "Jantar 🌙"
        else:
            return "Lanche da noite 🌙🥛"
