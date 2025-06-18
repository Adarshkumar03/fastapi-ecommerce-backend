from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int
    category: str
    description: str
    image_url: str
    
class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    stock: Optional[int]
    category: Optional[str]
    image_url: Optional[str]    
