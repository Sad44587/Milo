from google import genai
import os

# Il est préférable d'utiliser une variable d'environnement
# api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key="AIzaSyCbw88MBs6PBjMr9gXwiCSMTtDDDGtExD8")

print("Tapez 'quitter' pour arrêter la discussion.\n")

while True:
    user_message = input("Vous : ")
    if user_message.lower() in ["quitter", "exit", "stop"]:
        break

    try:
        # Utilisation de gemini-2.0-flash pour la rapidité
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=user_message,
        )
        # On accède au texte via .text
        print(f"Chatbot : {response.text}")

    except Exception as e:
        print(f"\n[Erreur] : {e}")
