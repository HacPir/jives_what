from agents.translation_agent import translate_text
from agents.summary_agent import summarize_text
import agents.calendar_agent
from agents.weather_agent import get_weather
from agents.music_agent import create_music
from agents.gpt_agent import query_file_chatgpt, query_chatgpt
import re

def main_agent(query):
    if "traduit" in query or "traduire" in query or "traduction" in query:
        sentence = None
        # Recherche des différentes formes
        match = re.search(r"traduit (.+)", query)
        if match:
            sentence = match.group(1)
        else:
            match = re.search(r"traduire (.+)", query)
            if match:
                sentence = match.group(1)
            else:
                match = re.search(r"traduction de (.+)", query)
                if match:
                    sentence = match.group(1)
        
        if sentence:  # Si une phrase a été trouvée
            return translate_text(sentence)
        else:
            return "Aucune phrase à traduire trouvée."
    elif "résumer" in query:
        match = re.search(r"résumer de (\w+)", query)
        return summarize_text(query)
    elif "dates anniversaires" in query:
        return query_file_chatgpt(query)
    elif "rendez-vous" in query:
        return query_file_chatgpt(query)
    elif "météo" in query or "le temps à" in query or "il fait à" in query:
        city = None
        # Recherche des différentes formes
        match = re.search(r"météo de (\w+)", query)
        if match:
            city = match.group(1)
            #city = "paris"  # Vous pouvez extraire la ville de la requête si nécessaire
        else:
            match = re.search(r"le temps à (.+)", query)
            if match:
                city = match.group(1)
            else:
                match = re.search(r"il fait à (.+)", query)
                if match:
                    city = match.group(1)
        return get_weather(city)
    elif "musique" in query:
        return create_music(query)
    elif "fichier" in query or "document" in query or "documentation" in query:
        query_file_chatgpt(query)
    else:
        return query_chatgpt(query)