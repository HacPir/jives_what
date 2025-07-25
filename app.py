from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import asyncio
import os

# App principale
app = Flask(__name__)
<<<<<<< HEAD
app.secret_key = "TOKEN_API_FLASK"
=======
app.secret_key = "super-secret-key"
>>>>>>> 105f2ca28f2c8d5cc20dc1224055068bb84f1d54

from agents.main_agent import main_agent

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    user_query = data.get('query')
    response = main_agent(user_query)
    return jsonify({'response': response})

# === Family Connection AI ===
from main import FamilyConnectionOrchestrator

<<<<<<< HEAD
orchestrator = FamilyConnectionOrchestrator(os.getenv("TOKEN_API_OPENAI"))
=======
orchestrator = FamilyConnectionOrchestrator(os.getenv("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"))
>>>>>>> 105f2ca28f2c8d5cc20dc1224055068bb84f1d54
memory_agent = orchestrator.agents["memory"]
elderly_agent = orchestrator.agents["elderly"]
master_agent = orchestrator.agents["master"]
younger_agent = orchestrator.agents["younger_relative"]

@app.route('/dashboard')
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

@app.route('/trigger_reminders')
def trigger_reminders():
    asyncio.run(memory_agent.check_and_alert())
    flash("🎉 Rappels d’anniversaire déclenchés !")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
