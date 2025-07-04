import os
from typing import List
from dotenv import load_dotenv
import instructor
from openai import OpenAI
from pydantic import BaseModel
from src.models import Product, engine
from sqlmodel import Session, select
from src.agent.models import UserIntent, FreeChat, QualityCheck
from src.agent.utils.agent_flow_logging import FlowLogger
import httpx

logger = FlowLogger()
load_dotenv()


class LLM:
    def __init__(self):
        self.client = instructor.from_openai(
            OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama",
            ),
            mode=instructor.Mode.JSON,
        )

    def send(self, response_model: BaseModel, message: str, context: str = None):

        try:
            command = self.client.chat.completions.create(
                model="llama3",
                messages=[{"role": "user", "content": message}],
                response_model=response_model,
                max_retries=5,
                timeout=60.0,
                context={"context":context},
            )
            return command
        except Exception as e:
            raise Exception(f"Failed to parse user command: {str(e)}")


class AIAgent:
    def __init__(self):
        self.llm = LLM()

    def handle_message(
        self, message: str, attempts: int = 0, max_attempts: int = 10
    ) -> str:
        if attempts == 0:
            logger.success("Starting Agent Flow Execution", message)

        if attempts >= max_attempts:
            logger.error("Failed to Execute Flow With:", message)
            return "Sorry, I did not understand your question"

        intent = self.identify_intent(message)
        logger.info("Analysing Intent", intent)

        response_ok = self.intent_verify(intent, message)
        if not response_ok:
            return self.handle_message(message, attempts + 1, max_attempts)
        else:
            return self.flow_continue(intent, message)

    def identify_intent(self, message: str) -> UserIntent:
        response = self.llm.send(UserIntent, message)
        if response.orders and response.message is None:
            response = self.llm.send(UserIntent, message)
        return response

    def intent_verify(self, intent: BaseModel, message: str):
        qa_context = """ 
            You are a validation agent responsible for checking if a user intent action and its corresponding JSON payload are semantically valid.
            Given:
            An intent action (such as "buy", "info", or "chat").
            A JSON payload with fields expected to match that intent.
            Return False if:
            Intent is "buy" and the JSON:
            Does not contain a non-empty list in orders (e.g., orders=[] or missing).
            Intent is "info" or "most_sold" and the JSON:
            Must have orders empty and also message empty to be true.
            Intent is "chat" and the JSON:
            Does not contain a non-empty string in message (e.g., message="" or missing).
            Return True only if:
            The intent matches the action type in the JSON, and
            The expected data structure for that intent is present and non-empty.
            """
        verify = f""" Question: {message} 
                    JSON: \n
                    {intent}
                    """

        if intent.action == "info":
            logger.success("Info about Stock Intent Validated by Intent Checker")
            return True
        if intent.action == "most_sold":
            logger.success("Most Sold Information Intent Validated by Intent Checker")
            return True

        if intent.action == "buy" and intent.orders == []:
            logger.warn("Intent Not Indentified", "Trying Again")
            return False
        if intent.action == "chat" and intent.message == None:
            logger.warn("Intent Not Indentified", "Trying Again")
            return False

        response = self.llm.send(QualityCheck, verify, context=qa_context)
        if response.valid == False:
            logger.warn("Intent Not Indentified", "Trying Again")
        if response.valid:
            logger.success("Intent Validated by Intent Checker")

        return response.valid

    def flow_continue(self, command: UserIntent, message: str):
        if command.action == "buy":
            sales_results = []
            for order in command.orders:
                payload = {
                    "product_name": order.soda_name.lower(),
                    "quantity": order.quantity
                }
                try:
                    response = httpx.post("http://localhost:8000/sales/", json=payload)
                    if response.status_code == 200:
                        sales = response.json()
                        sales_results.append(f"Ordered {order.quantity}x {order.soda_name}: Success")
                    else:
                        sales_results.append(f"Ordered {order.quantity}x {order.soda_name}: Failed ({response.json().get('detail', 'Unknown error')})")
                except Exception as e:
                    sales_results.append(f"Ordered {order.quantity}x {order.soda_name}: Failed ({str(e)})")
            final_response = " \n ".join(sales_results)
            logger.info("Buying", command.orders)
            logger.success("Flow Completed", {"input": message, "response": final_response})
            return final_response

        elif command.action == "info":
            info_context = "You are a working with Drink Sales Return the Stock Information Bellow in a user Friendly way"
            try:
                resp = httpx.get("http://localhost:8000/products/?skip=0&limit=100")
                resp.raise_for_status()
                products = resp.json()
            except Exception as e:
                logger.error("Failed to fetch products", str(e))
                return "Sorry, I couldn't retrieve product information right now."

            if not products:
                return "No products available."
            stock = "Stock available:\n" + "\n".join(
                f"{p['name'].title()}: {p['stock']} in stock, ${p['price']} \n" for p in products
            )
            response = self.llm.send(FreeChat, message=stock, context=info_context)

            return response.message
        
        elif command.action == "most_sold":
            try:
                resp = httpx.get("http://localhost:8000/sales/most_sold/")
                resp.raise_for_status()
                most_sold = resp.json()
            except Exception as e:
                logger.error("Failed to fetch most sold products", str(e))
                return "Sorry, I couldn't retrieve most sold product information right now."

            if not most_sold:
                return "No sales data available."
            # Format the response as needed; assuming most_sold is a list of dicts
            result = "Most Sold Products:\n" + "\n".join(
                f"{item['product_name'].title()}: {item['total_sold']} sold in total" for item in most_sold
            )
            return result

        elif command.action in ("chat", "misc"):
            try:
                response: FreeChat = self.llm.send(FreeChat, command.message)
            except:
                response = (
                    "Sorry, i cant answer your question right now, try again later"
                )
                logger.error("Flow Failed", response)
            finally:
                logger.success(
                    "Flow Completed", {"input": message, "response": response.message}
                )
            return response.message

        return "Sorry, I couldn't understand your request."
