# jives_what
GenAI Hackathon July 2025

JIVES TEAM - W.H.A.T. (We Have Another Time)

# 🧠 Multi-Agent Interface

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Flask](https://img.shields.io/badge/Framework-Flask-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🎬 Video
Clic to play :)
<p align="center">
  <a href="https://www.youtube.com/watch?v=cpmVossJ_bA">
    <img src="https://img.youtube.com/vi/cpmVossJ_bA/hqdefault.jpg" alt="Promotion">
  </a>
</p>

---

## 📌 Description

**Multi-Agent Interface** is a modular platform for intelligent agents that can collaborate through a centralized orchestrator. Each agent has a specific role — whether it's interacting with GPT, managing calendar events, generating summaries, or producing music — and can be easily integrated or replaced thanks to a flexible architecture.

<p align="center">
  <a href="https://docs.google.com/presentation/d/1mZTO5XHFmZJze0PI5hq0PF29B2UMDPq5">
    Project Presentation
  </a>
</p>

---

## 🚀 Key Features

- 🧠 **Specialized AI Agents**:
  - `GPTAgent`: Generates text using GPT (OpenIA API is used)
  - `CalendarAgent`: Manages calendar events (Google Cloud API can be used)
  - `BirthdayAgent`: Handles birthday reminders
  - `MusicAgent`: Generates music
  - `SummaryAgent`: Summarizes content
  - `TranslateAgent`: Tranlates content
  - `WeatherAgent`: Give weather from city
- ⚙️ **Central orchestration** via `MainAgent`
- 🧱 **Extensible model** based on a `BaseAgent` class
- 🌐 **Web API** built with Flask for frontend or system integration

---

## 🗂️ Project Structure

```
📦 project-root/
├── main.py                     # Project entry point
├── requirements.txt            # Project dependencies
│
├── templates/                  # Web interface templates (HTML/CSS)
│   ├── dashboard.html
│   ├── index.html
│
├── scripts/                    # Custom scripts used by the AI agents
│   ├── calendar_agent.py
│
├── docs/                       # Context documents to support AI prompts
│
├── data/                       # Files the AI can read/write to (e.g. inputs, logs)
│   ├── birthdays.json      
│   ├── calendar.json
│
├── agents/                     # Main AI agents used in the project
│   ├── base_agent.py
│   ├── calendar_agent.py
│   ├── elderly_agent.py
│   ├── gpt_agent.py
│   ├── main_agent.py
│   ├── master_agent.py
│   ├── memory_agent.py
│   ├── music_agent.py        # Prototype
│   ├── summary_agent.py
│   ├── translation_agent.py
│   ├── weather_agent.py
│   ├── younger_relative_agent.py
│
├── familyconnect-agents/      # Prototype of a family-focused agent interface
│
├── genai-agentos/             # Work on a graphical interface and GenIA API integration
│
├── app.py                     # Main Flask server
├── app_agent.py               # Flask endpoints for agents
└── app_birthday.py            # Flask endpoint for birthday reminders
└── project_presentation.pdf   # Slides of the project
```
---

## ⚙️ Installation

**Clone the repository**

```bash
git clone https://github.com/https://github.com/HacPir/jives_what.git
cd jives_what
```
**Install dependencies
```bash
pip install -r requirements.txt
pip install flask
```

## ⚙️ Setup

**Change API Keys**
```bash
modify TOKEN_API_OPENAI to your API KEY on line 8 in app_birthday.py
modify TOKEN_API_OPENAI to your API KEY on line 11 in app_birthday.py

modify TOKEN_API_OPENAI to your API KEY on line 7 in app.py
modify TOKEN_API_OPENAI to your API KEY on line 25 in app.py

modify TOKEN_API_OPENAI to your API KEY on line 12 in main.py

modify TOKEN_API_OPENAI to your API KEY on line 5 in gpt_agent.py

modify OPEN_WEATHER_API to your API KEY on line 10 in weather_agent.py
```

**Setup context folders**
Create "docs" folder and add documents to it to help your agent give answer based on context.

## ⚙️ Use

**Lauch the server from our terminal**
```bash
python main.py
```

## 🔧 Adding a New Agent
To create a new agent:

Inherit from BaseAgent

Implement required methods (handle, describe, etc.)

Register the agent in MainAgent

## 📄 License

Built for LeadWithAI Hackathon 2025. All rights reserved.

---

**W.H.A.T. (We Have Another Time)** - *Connecting families through intelligent AI conversation*
