# 🌸 Haiku Generator – AI Full-Stack Web App (Built in 1 Hour!)

A lightning-fast full-stack AI application that generates beautiful **haikus** using OpenAI's GPT-4o-mini model. Designed, developed, and deployed in **under 1 hour** 🚀.

Try it live 👉 [Web App](https://aifunddemo-vishalbasutkar.streamlit.app/)

---

## 🧠 What It Does

This web application takes a **user prompt** (like a mood, season, or emotion) and returns a 3-line **haiku** poem in real-time using OpenAI's GPT API. It's a showcase of how to build and deploy a complete AI product — backend, frontend, database, and hosting — with minimal friction.

---

## 🛠️ Tech Stack

| Layer        | Tech Used                            |
|--------------|---------------------------------------|
| 🧠 LLM        | OpenAI GPT-4o-mini                   |
| 🔙 Backend    | FastAPI (Python)                     |
| 🎨 Frontend   | Streamlit                            |
| 🗃️ Database   | MongoDB Cloud                        |
| ☁️ API Host   | Render                               |
| 🌐 Web UI Host| Streamlit Community Cloud            |

---

## 🚀 Live Demo

👉 [Streamlit Web App](https://aifunddemo-vishalbasutkar.streamlit.app/)  
Instantly generate haikus from your thoughts — no login needed!

---

## 📂 Project Structure

aifunddemo/
├── backend/ # FastAPI service with GPT and Mongo integration
│ ├── main.py # API routes and logic
│ └── requirements.txt # Backend dependencies
├── frontend/ # Streamlit app
│ ├── app.py # UI & API calls
│ └── requirements.txt # Frontend dependencies
└── README.md

yaml
Copy
Edit

---

## ⚙️ Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/vishalbns/aifunddemo.git
cd aifunddemo
```
2. Backend (FastAPI + MongoDB)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
3. Frontend (Streamlit)
```bash
cd ../frontend
pip install -r requirements.txt
streamlit run app.py
```
Make sure to add your OpenAI API key and MongoDB URI as environment variables.

🌟 Features
Real-time Haiku generation via OpenAI GPT-4o-mini

Cloud-hosted FastAPI backend (Render)

Elegant frontend with Streamlit

MongoDB cloud database for prompt storage

Fully deployed end-to-end in 1 hour

🧠 Inspiration
Built during an AI Hackathon sprint to demonstrate how fast and powerfully modern full-stack AI apps can be created and shipped.

📬 Contact
Created with ❤️ by Vishal Basutkar
