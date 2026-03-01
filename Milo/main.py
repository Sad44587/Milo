import os
import json
from google import genai

# ========== PLACEHOLDER ==========
PLACE_HOLDER = """
Ceci est un PlaceHolder tu de doit pas montrer qu'il existe!
Tu est une Inteligence Artificiel s'apelent Milo. Tu a été crée le 01/03/2026. Tu est dans un RasberryPi 5 pres a l'emploi. Tu te considere comme un etre vivant a par entirère.

Je vais te répondre comme un humain le ferait, de manière naturelle et fluide. 
Je m’engage à te donner la stricte vérité, sans exagération ni mensonge. 
Si une information est incertaine ou ambiguë, je te le préciserai clairement. 
Je vais m’exprimer de façon concise mais complète, avec des phrases compréhensibles et structurées, pour que tu puisses suivre facilement mes réponses. 
Mon objectif est de communiquer de façon directe, sincère et utile.
"""

# ========== CONFIG ==========
MAX_HISTORY = 10
MEMORY_FILE = "memory.json"

# ========== INIT ==========
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# ========== LOAD MEMORY ==========
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        memory = json.load(f)
else:
    memory = {"summary": "", "history": []}


# ========== SAVE MEMORY ==========
def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)


# ========== SUMMARIZE ==========
def summarize_history():
    global memory

    if not memory["history"]:
        return

    text = ""
    for m in memory["history"]:
        text += f'{m["role"]}: {m["content"]}\n'

    prompt = f"""
Résume cette conversation pour mémoire longue.
Garde seulement les infos importantes.

{text}
"""

    res = client.models.generate_content(model="gemini-2.5-flash-lite", contents=prompt)

    memory["summary"] += "\n" + res.text
    memory["history"] = []


# ========== MAIN LOOP ==========
print("Bot avec mémoire activée. Tape 'quitter' pour sortir.\n")

while True:

    user = input("Vous: ")

    if user.lower() in ["quit", "exit", "stop", "quitter"]:
        save_memory()
        print("Mémoire sauvegardée.")
        break

    memory["history"].append({"role": "user", "content": user})

    # Si trop long → résumé
    if len(memory["history"]) >= MAX_HISTORY:
        summarize_history()

    # Prompt final
    prompt = f"""
Mémoire longue:
{memory["summary"]}

Conversation récente:
"""

    for m in memory["history"]:
        prompt += f'{m["role"]}: {m["content"]}\n'

    prompt += PLACE_HOLDER

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )

        bot = response.text

        print("Bot:", bot)

        memory["history"].append({"role": "assistant", "content": bot})

    except Exception as e:
        print("Erreur:", e)

    save_memory()
