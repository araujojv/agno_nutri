from agno.models.message import Message
from agno.models.openai import OpenAIChat
from skills.meals import get_remaining_calories

def suggest_meal(daily_goal: int, meal_type: str = "Jantar") -> str:
    """
    Sugere uma refeição com base na meta calórica e no que já foi consumido.
    meal_type pode ser: 'Café da manhã', 'Almoço', 'Jantar', 'Lanche'.
    """
    remaining, consumed = get_remaining_calories(daily_goal)

    if remaining <= 0:
        return (
            f"⚠️ Você já atingiu ou ultrapassou sua meta diária de {daily_goal} kcal.\n"
            "Sugiro uma refeição leve e rica em fibras/vegetais, sem muitas calorias extras."
        )

    model = OpenAIChat(id="gpt-4.1-mini")
    response = model.response(
        messages=[
            Message(
                role="user",
                content=(
                    f"O usuário tem uma meta diária de {daily_goal} kcal, "
                    f"já consumiu {consumed} kcal e restam {remaining} kcal.\n\n"
                    f"Sugira opções de {meal_type} que se encaixem nesse valor de calorias, "
                    "equilibrando proteínas, carboidratos e gorduras saudáveis. "
                    "Responda com 2 a 3 sugestões práticas, incluindo os valores aproximados de kcal."
                )
            )
        ]
    )

    return response.content
