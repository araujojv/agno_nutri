import base64
import re
from agno.models.openai import OpenAIChat
from skills.meals import add_meal, get_total_today

def analyze_food_image(image_path: str) -> str:
    """
    Analisa a foto do prato, estima calorias e registra refeição no banco
    com horário. Retorna também o total acumulado do dia.
    """
    with open(image_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode("utf-8")

    model = OpenAIChat(id="gpt-4o-mini")
    response = model.response([
        {
            "role": "user",
            "content": [
                {"type": "text", "text": 
                 "Analise esta foto de um prato de comida. "
                 "Identifique os principais alimentos e estime a quantidade total de calorias. "
                 "Responda no formato: lista de alimentos + 'Total: XXX kcal'."},
                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{img_base64}"}
            ]
        }
    ])

    result = str(response)

    # --- Extrair calorias ---
    match = re.search(r"(\d{2,5})\s*kcal", result.lower())
    calories = int(match.group(1)) if match else 0

    # Registrar refeição
    add_meal(description="Prato analisado por foto", calories=calories)

    # Total atualizado
    total_today = get_total_today()

    return (
        f"📸 Análise do prato:\n{result}\n\n"
        f"🔥 Calorias registradas: ~{calories} kcal\n"
        f"📊 Total acumulado do dia: {total_today} kcal"
    )
