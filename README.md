# 🥤 Soda Machine API – AI-powered Vending System

Welcome to the **Soda Machine API**, a simple but intelligent vending machine powered by **FastAPI**, **SQLModel**, and AI via the **Instructor** library.

---

## 🚀 Overview

This API enables users to interact with a soda vending machine using **natural language** commands like:

> "I want to buy 2 sprites and a coke."

Through the power of **LLMs** (Language Models), the system interprets these messages, determines the user’s intent, and performs appropriate actions like selling soda, updating inventory, and logging transactions.

---

## 🧠 AI Flow Orchestrator (Inspired by CrewAI)
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

-   **Python 3.11+**
-   **FastAPI** – RESTful API framework
-   **SQLModel** – SQLite ORM (SQLAlchemy + Pydantic)
-   **Instructor** – OpenAI-based JSON validation using structured outputs
-   **Docker + docker-compose** – Containerized environment

---

## ⚙️ Features

-   🛒 Natural language purchase of soda
-   📦 Inventory tracking and persistence
-   💾 Transaction history stored in SQLite
-   🔍 Intent detection: Buy, Info, or Misc
-   📉 Stock depletion handling
-   📈 Built-in data models for analytics (most sold, low stock, etc.)

---

## 🚀 Getting Started

To get the Soda Machine API up and running, follow these steps:

1.  **Navigate to the project root:**
    Ensure you are in the `Soda-Machine-AI` directory where `docker-compose.yaml` is located.

    ```bash
    cd ~/Soda-Machine-AI
    ```

2.  **Ensure `docker-compose.yaml` is configured:**
    The `docker-compose.yaml` file should already contain the `LLM_MODEL` and `OPENAI_API_KEY` environment variables for the backend service. An example snippet for the backend service within your `docker-compose.yaml` would look like this:

    ```yaml
    services:
      backend:
        build: ./back-end
        ports:
          - "8000:8000"
        environment:
          - LLM_MODEL=llama3 # Or your preferred LLM model name, e.g., gpt-4o
          - OPENAI_API_KEY=your_openai_api_key_here # Replace with your actual OpenAI API key or a placeholder if using a local model
        # ... other backend configurations
    ```
    **Note:** If you are using a local LLM model via Ollama, `OPENAI_API_KEY` might not be strictly necessary for the API calls themselves, but `Instructor` often expects it, so a placeholder value can be used if you're not connecting to OpenAI directly.

3.  **Build and Run with Docker Compose:**
    Once your `docker-compose.yaml` is correctly configured, you can build and start the services using Docker Compose:

    ```bash
    docker-compose up --build
    ```

    This command will:
    * Build the Docker images for both the `back-end` and `frontend` services (if they haven't been built or if changes are detected).
    * Start the containers, making the Soda Machine API available.

4.  **Access the API and Frontend:**
    * The **frontend** will be available at `http://localhost:5173`.
    * The **FastAPI backend** will be accessible at `http://localhost:8000`.
    * The **FastAPI backend docs** will be accessible at `http://localhost:8000/docs`.

You can now interact with your AI-powered soda machine!