import os
from typing import List
from dotenv import load_dotenv
import instructor
from openai import OpenAI
from pydantic import BaseModel

from src.agent.models import UserIntent, FreeChat, QualityCheck
from src.agent.utils.agent_flow_logging import FlowLogger
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

    def send(
        self, response_model: BaseModel, message: str, quality_agent: bool = False
    ):
        qa_context = ""
        if quality_agent:
            logger.info("Checking Quality")
            qa_context = """ 
            You are a validation agent responsible for checking if a user intent action and its corresponding JSON payload are semantically valid.

                                Given:

                                An intent action (such as "buy", "info", or "chat").

                                A JSON payload with fields expected to match that intent.

                                Return False if:
                                Intent is "buy" and the JSON:

                                Does not contain a non-empty list in orders (e.g., orders=[] or missing).

                                Intent is "info" and the JSON:

                                Does not contain a non-empty list in info (e.g., info=[] or missing).

                                Intent is "chat" and the JSON:

                                Does not contain a non-empty string in message (e.g., message="" or missing).

                                Return True only if:
                                The intent matches the action type in the JSON, and

                                The expected data structure for that intent is present and non-empty.

                                Examples:
                                1. intent="buy" with orders=[] → False
                                { "action": "buy", "orders": [] }

                                2. intent="buy" with orders=[{ "soda": "coke", "qty": 2 }] → True
                                { "action": "buy", "orders": [{ "soda": "coke", "qty": 2 }] }

                                3. intent="info" with info=[] → False

                                4. intent="chat" with no message or an empty string → False
                            """
            command = self.client.chat.completions.create(
                    model="llama3",
                    messages=[{"role": "user", "content": f"{qa_context}\n\n{message}"}],
                    response_model=response_model,
                    max_retries=2,
                    timeout=60.0,

                )
            return command


        try:
            command = self.client.chat.completions.create(
                model="llama3",
                messages=[{"role": "user", "content": message}],
                response_model=response_model,
                max_retries=2,
                timeout=60.0,

            )
            return command
        except Exception as e:
            raise Exception(f"Failed to parse user command: {str(e)}")


class AIAgent:
    def __init__(self):
        self.llm = LLM()

    def handle_message(
        self, message: str, attempts: int = 0, max_attempts: int = 5
    ) -> str:
        if attempts == 0:
            logger.success("Starting Agent Flow Execution", message)

        if attempts >= max_attempts:
            logger.error("Failed to Execute Flow With:", message)
            return "Sorry, I did not understand your question"

        intent = self.identify_intent(message)
        logger.info("Analysing Intent", intent)

        response_ok = self.quality_check(intent, message)
        if not response_ok:
            return self.handle_message(message, attempts + 1, max_attempts)
        else:
            return self.flow_continue(intent, message)

    def identify_intent(self, message: str) -> UserIntent:
        response = self.llm.send(UserIntent, message)
        if response.orders and response.message is None:
            response = self.llm.send(UserIntent, message)
        return response

    def quality_check(self, intent: BaseModel, message: str):
        verify = f""" Question: {message} 
                    JSON: \n
                    {intent}
                    """
        if intent.action=="buy" and intent.orders==[]:
            logger.warn("Intent Not Indentified", "Trying Again")
            return False
        if intent.action=="chat" and intent.message==None:
            logger.warn("Intent Not Indentified", "Trying Again")
            return False
        response = self.llm.send(QualityCheck, message, quality_agent=True)
        if response.valid == False:
            logger.warn("Intent Not Indentified", "Trying Again")
        if response.valid:
            logger.success("Intent Validated by Quality Checker")

        return response.valid

    def flow_continue(self, command: UserIntent, message: str):
        if command.action == "buy":
            response = "Order received: " + ", ".join(
                f"{o.quantity}x {o.soda_name}" for o in command.orders
            )
            logger.success("Flow Completed",{"input":message,"response":response })

            return response

        elif command.action == "info":
            return "We offer: Coca-Cola, Fanta, Sprite, and Pepsi. What would you like?"
        #TODO
        elif command.action in ("chat", "misc"):
            try:
                response:FreeChat = self.llm.send(FreeChat, command.message)
            except:
                response = "Sorry, i cant answer your question right now, try again later"
                logger.error("Flow Failed", response)
            finally:
                logger.success("Flow Completed",{"input":message,"response":response.message })
            return response

        return "Sorry, I couldn't understand your request."
