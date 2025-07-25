import json
from datetime import datetime, date
from typing import List, Dict

class FamilyAgent:
    def __init__(self, data_file="data/birthdays.json"):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self) -> Dict:
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"birthdays": [], "events": []}

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=2)

    def get_todays_birthdays(self) -> List[Dict]:
        today = date.today()
        birthdays_today = []
        for entry in self.data.get("birthdays", []):
            try:
                bday = datetime.strptime(entry["date"], "%Y-%m-%d").date()
                if bday.day == today.day and bday.month == today.month:
                    entry["age"] = today.year - bday.year
                    birthdays_today.append(entry)
            except ValueError:
                continue
        return birthdays_today

    def print_todays_birthdays(self):
        birthdays = self.get_todays_birthdays()
        if not birthdays:
            print("🎉 Aucun anniversaire aujourd'hui.")
        for b in birthdays:
            print(f"🎂 Aujourd'hui, c'est l'anniversaire de {b['name']} ({b['relationship']}) - {b['age']} ans!")

    def add_event(self, name: str, date_str: str, description: str):
        new_event = {
            "name": name,
            "date": date_str,
            "description": description
        }
        self.data.setdefault("events", []).append(new_event)
        self.save_data()
        print(f"✅ Rendez-vous '{name}' ajouté pour le {date_str}.")

    def list_upcoming_events(self):
        today = date.today()
        events = []
        for event in self.data.get("events", []):
            try:
                event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
                if event_date >= today:
                    events.append((event_date, event))
            except ValueError:
                continue
        events.sort()
        if not events:
            print("📅 Aucun rendez-vous à venir.")
        else:
            print("📅 Rendez-vous à venir :")
            for date_, e in events:
                print(f"- {e['name']} ({e['description']}) le {date_.strftime('%d/%m/%Y')}")

# Exemple d'utilisation
#if __name__ == "__main__":
#    agent = FamilyAgent()
#    agent.print_todays_birthdays()
#    agent.add_event("Dentiste", "2025-07-20", "Contrôle annuel")
#    agent.list_upcoming_events()
