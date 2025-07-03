# 🥤 Soda Machine API – AI-powered Vending System

Welcome to the **Soda Machine API**, a simple but intelligent vending machine powered by **FastAPI**, **SQLModel**, and AI via the **Instructor** library. 

---

## 🚀 Overview

This API enables users to interact with a soda vending machine using **natural language** commands like:

> "I want to buy 2 sprites and a coke."

Through the power of **LLMs** (Language Models), the system interprets these messages, determines the user’s intent, and performs appropriate actions like selling soda, updating inventory, and logging transactions.

---

🧠 AI Flow Orchestrator (Inspired by CrewAI)
This backend features a lightweight AI agent orchestrator, which I call flow, inspired by CrewAI and fully developed by me.

It is responsible for managing how the AI interprets and validates natural language inputs in a reliable and structured way.

🔧 Key Features
🔁 Recursive Validation Logic
Automatically retries up to 5 times when the LLM produces structurally or semantically invalid responses.

✅ Structured JSON Schema Validation
Uses Instructor to enforce that LLM outputs follow precise Pydantic models like UserIntent, FreeChat, etc.

⚙️ LLM Client Integration
Powered by Instructor + OpenAI, running locally via Ollama with the llama3 model.

🧪 Quality Agent Layer
A second AI agent is used to semantically validate whether the parsed intent actually makes sense:

buy must contain a non-empty list of orders

chat must contain a message string

info must return a meaningful payload




---

## 📦 Tech Stack

- **Python 3.11+**
- **FastAPI** – RESTful API framework  
- **SQLModel** – SQLite ORM (SQLAlchemy + Pydantic)  
- **Instructor** – OpenAI-based JSON validation using structured outputs  
- **Docker + docker-compose** – Containerized environment  

---

## ⚙️ Features

- 🛒 Natural language purchase of soda
- 📦 Inventory tracking and persistence
- 💾 Transaction history stored in SQLite
- 🔍 Intent detection: Buy, Info, or Misc
- 📉 Stock depletion handling
- 📈 Built-in data models for analytics (most sold, low stock, etc.)

---
