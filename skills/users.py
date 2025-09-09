import sqlite3

DB_PATH = "tmp/nutritionist.db"

def init_user_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY,
            age INTEGER,
            height REAL,
            weight REAL,
            daily_goal INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_user_profile(age: int, height: float, weight: float, daily_goal: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_profile")  # mantém só 1 usuário
    cursor.execute("INSERT INTO user_profile (id, age, height, weight, daily_goal) VALUES (1, ?, ?, ?, ?)", 
                   (age, height, weight, daily_goal))
    conn.commit()
    conn.close()

def get_user_profile():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT age, height, weight, daily_goal FROM user_profile WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    return row if row else None



def calculate_tmb(age: int, height: float, weight: float, gender: str = "male") -> int:
    """
    Fórmula de Mifflin-St Jeor para TMB.
    height em cm, weight em kg, age em anos.
    """
    if gender == "male":
        tmb = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        tmb = 10 * weight + 6.25 * height - 5 * age - 161
    
    # Multiplicador de atividade leve (1.2)
    return int(tmb * 1.2)
