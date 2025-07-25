# app_flask.py
from flask import Flask, render_template, redirect, url_for, flash
import os
import asyncio
from main import FamilyConnectionOrchestrator

app = Flask(__name__)
<<<<<<< HEAD
app.secret_key = "TOKEN_API_FLASK"
=======
app.secret_key = "replace-with-a-secure-secret"
>>>>>>> 105f2ca28f2c8d5cc20dc1224055068bb84f1d54

# Initialize orchestrator
orchestrator = FamilyConnectionOrchestrator(os.getenv("TOKEN_API_OPENAI"))
memory_agent = orchestrator.agents["memory"]
elderly_agent = orchestrator.agents["elderly"]
master_agent = orchestrator.agents["master"]
younger_agent = orchestrator.agents["younger_relative"]

@app.route("/")
def dashboard():
    birthdays = asyncio.run(memory_agent.analyze_todays_birthdays())
    master_log = master_agent.get_conversation_log()
    elderly_responses = elderly_agent.get_user_responses()
    notifications = younger_agent.get_notifications()
    
    return render_template("dashboard.html",
                           birthdays=birthdays,
                           master_log=master_log,
                           elderly_responses=elderly_responses,
                           notifications=notifications)

@app.route("/trigger")
def trigger_reminders():
    asyncio.run(memory_agent.check_and_alert())
    flash("🎉 Rappels d’anniversaire déclenchés !")
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(debug=True)
