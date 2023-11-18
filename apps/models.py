# models.py
from pydantic import BaseModel

class UbeeEVWLoginInfo(BaseModel):
    username: str
    password: str
    url: str

# Add other shared models as needed
