# 🥤 Soda Machine API – AI-powered Vending System

Welcome to the **Soda Machine API**, a simple but intelligent vending machine powered by **FastAPI**, **SQLModel**, and AI via the **Instructor** library. 

---

## 🚀 Overview

This API enables users to interact with a soda vending machine using **natural language** commands like:

> "I want to buy 2 sprites and a coke."

Through the power of **LLMs** (Language Models), the system interprets these messages, determines the user’s intent, and performs appropriate actions like selling soda, updating inventory, and logging transactions.

---

## 🧠 AI Agent Orchestration

This backend features a lightweight **AI agent orchestrator** which i called flow, inspired by crewai, developed by me with:

- 🔁 Recursive validation logic to ensure coherent agent responses  
- ✅ JSON schema validation via [Instructor](https://github.com/jxnl/instructor)  
Manages how the AI interprets and validates natural language inputs.

✅ Flow Highlights
LLM Client: Powered by instructor + OpenAI, configured to run locally via ollama.

Structured Output: Uses Pydantic response models to constrain and validate AI responses (e.g., UserIntent, FreeChat).

Recursive Retry Logic: If the LLM returns an incoherent structure (e.g., action=buy but orders=[]), the orchestrator retries up to 5 times with feedback.

Quality Agent Layer: For semantic validation of the structured intent before continuing to the business logic.


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
