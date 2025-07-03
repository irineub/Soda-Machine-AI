from typing import List, Literal, Optional

from pydantic import BaseModel, Field




class SodaOrder(BaseModel):
    soda_name: str = Field(..., description="Name of the soda (e.g. coke, sprite, fanta) always in english")
    quantity: int = Field(..., description="Quantity of that soda to purchase")

class UserIntent(BaseModel):
    action: Literal["buy", "chat","info","most_sold"] = Field(
        default="chat", 
        description="The user’s intent: buy soda, get soda stock info, or chat freely"
    )
    orders: Optional[List[SodaOrder]] = Field(
        default=None,
        description="List of soda orders if the action is 'buy'"
    )
    message: Optional[str] = Field(
        default=None,
        description="Freeform user message if the action is 'chat'"
    )


class FreeChat(BaseModel):
    message:str

class QualityCheck(BaseModel):
    context:str
    valid:bool = Field(...,description="Check if the JSON matches the intent returning true or false , if its a buy action it must have a order list, if its is a chat it must have message, if its info or most_sold it doesnt have orders or message.")