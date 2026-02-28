from gradio_client import Client

client = Client("TirthGaikwad/gemini-elevenlabs-chatbot")

print("Chatbot prêt. Tapez 'quitter' pour arrêter la conversation.")

while True:
    user_message = input("Vous: ")

    if user_message.lower() == "quitter":
        print("Chatbot: Au revoir !")
        break

    try:
        # Envoie le message de l'utilisateur à l'IA
        # Le résultat attendu est la réponse textuelle de l'IA
        ai_response = client.predict(
            message=user_message, api_name="/chat_bot_response"
        )
        print(f"Chatbot: {ai_response}")
    except Exception as e:
        print(f"Une erreur est survenue lors de la communication avec l'IA : {e}")
        print("Veuillez vérifier votre connexion internet ou l'état du service.")
