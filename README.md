# Soda AI Backend API

A FastAPI-based CRUD application using SQLModel and SQLite for managing products and sales, with integrated Gemini AI chat functionality.

## Setup

1. Create a `.env` file in the root directory with your Gemini API key:
```bash
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

The API will be available at `http://127.0.0.1:8000`

## API Endpoints

### Chat (Gemini AI)

- `POST /chat/` - Chat with Gemini AI (with conversation history)
- `POST /chat/simple/` - Simple chat with Gemini AI (message only)

### Products

- `POST /products/` - Create a new product
- `GET /products/` - Get all products (with pagination: skip, limit)
- `GET /products/{product_id}` - Get a specific product
- `PUT /products/{product_id}` - Update a product
- `DELETE /products/{product_id}` - Delete a product

### Sales

- `POST /sales/` - Create a new sale (automatically reduces product stock)
- `GET /sales/` - Get all sales (with pagination: skip, limit)
- `GET /sales/{sale_id}` - Get a specific sale
- `DELETE /sales/{sale_id}` - Delete a sale (automatically restores product stock)

### Health Check

- `GET /ping` - Health check endpoint

## Example Usage

### Chat with Gemini AI
```bash
# Simple chat
curl -X POST "http://127.0.0.1:8000/chat/simple/" \
     -H "Content-Type: application/json" \
     -d '"Hello, how are you?"'

# Chat with conversation history
curl -X POST "http://127.0.0.1:8000/chat/" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "What did I just ask you?",
       "conversation_history": [
         {"role": "user", "content": "Hello, how are you?"},
         {"role": "assistant", "content": "I am doing well, thank you for asking!"}
       ]
     }'
```

### Create a Product
```bash
curl -X POST "http://127.0.0.1:8000/products/" \
     -H "Content-Type: application/json" \
     -d '{"name": "Coca Cola", "stock": 100, "price": 150}'
```

### Get All Products
```bash
curl "http://127.0.0.1:8000/products/"
```

### Create a Sale
```bash
curl -X POST "http://127.0.0.1:8000/sales/" \
     -H "Content-Type: application/json" \
     -d '{"product_id": 1}'
```

## Environment Variables

Create a `.env` file in the root directory with:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

You can get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

## Database

The application uses SQLite with a database file `soda_ai.db` that will be created automatically when you first run the application.

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc` 