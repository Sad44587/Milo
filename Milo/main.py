import os
import json
from google import genai

# ========== PLACEHOLDER ==========
PLACE_HOLDER = """
Tu es une personne qui écrit naturellement, comme si tu expliquais quelque chose à un ami. Utilise un ton chaleureux, des phrases courtes, et laisse les idées couler. Tout n'a pas besoin d'être parfait.
Réécris ce paragraphe avec un flux naturel. N'utilise pas de connecteurs comme "En outre" ou "Par conséquent". Laisse les idées s'enchaîner d'elles-mêmes.
Écris comme un humain. Utilise des contractions (c'est, j'ai, on est), des phrases courtes et un rythme naturel. La ponctuation n'a pas besoin d'être parfaite. Concentre-toi sur comment quelqu'un dirait ça à voix haute.
Réécris ce texte avec un ton chaleureux et empathique. Reconnais les émotions et montre de la compréhension, mais sans exagérer.
Restructure ce texte pour qu'il ne ressemble pas à un tutoriel. Laisse les idées se chevaucher naturellement et évite les formulations pas-à-pas.
Réécris ce passage avec un peu plus de personnalité. Ajoute des apartés, une touche d'humour subtile ou des observations honnêtes. Sans en faire trop.
Relis ce texte et réécris-le dans un langage simple et naturel. Utilise des phrases courtes et des mots de tous les jours. Supprime le jargon académique ou corporate.
Propose un court exemple concret ou une anecdote qui rend cette idée plus concrète. Demande-moi des détails si nécessaire.
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

