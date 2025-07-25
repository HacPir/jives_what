import openai
import os

# Configurez votre clé API OpenAI
openai.api_key = 'TOKEN_API_OPENAI'

def query_chatgpt(prompt):
    """
    Effectue une requête simple à ChatGPT.

    :param prompt: La phrase ou la question à poser à ChatGPT.
    :return: La réponse de ChatGPT.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # ou un autre modèle selon disponibilité
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Une erreur est survenue : {e}"

def query_file_chatgpt(user_query):
    """
    Récupère des fichiers dans les dossiers spécifiés et utilise leur contenu
    pour contextualiser la conversation avec ChatGPT.
    """
    context = ""

    # Chemins vers les dossiers
    folders = ["data", "script", "docs"]

    # Lire les fichiers dans les dossiers spécifiés
    for folder in folders:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                filepath = os.path.join(folder, filename)
                if os.path.isfile(filepath):
                    try:
                        with open(filepath, 'r', encoding='utf-8') as file:
                            context += f"\nContenu du fichier {filename}:\n{file.read()}\n"
                    except Exception as e:
                        context += f"\nErreur lors de la lecture du fichier {filename}: {e}\n"

    # Demander à l'utilisateur ce qu'il souhaite faire
    #user_query = input("Que souhaitez-vous faire avec ces fichiers ? ")

    # Envoyer la requête avec le contexte des fichiers
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Contexte: " + context},
                {"role": "user", "content": user_query}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Une erreur est survenue : {e}"

# Exemple d'utilisation
#print(simple_chat_request("Bonjour, comment ça va ?"))
#print(chat_with_context())
