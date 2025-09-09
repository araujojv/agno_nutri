import os
from nutri_agent import nutri_agent
from skills.food_analysis import analyze_food_image
from skills.meals import get_meals_today
from skills.suggestions import suggest_meal
from dotenv import load_dotenv
load_dotenv()

def run_cli():
    print("🤖 Nutrólogo Supremo iniciado. Digite 'sair' para encerrar.")
    print("Você pode mandar texto normal ou o caminho de uma imagem (ex: prato.jpg).")

    while True:
        user_input = input("👤 Você: ")
        if user_input.lower() in ["sair", "exit", "quit"]:
            break

        # se for imagem (ex: almoco.jpg na mesma pasta)
        if os.path.exists(user_input):
            response = analyze_food_image(user_input)
        elif "comi hoje" in user_input.lower():
            response = get_meals_today()
        elif "jantar" in user_input.lower():
            response = suggest_meal(daily_goal=2500, meal_type="Jantar")  # valor fixo só pra testar
        else:
           response = nutri_agent.run(user_input)

        print(f"\n🤖 Nutrólogo Supremo: {response.content}\n")

if __name__ == "__main__":
    run_cli()
