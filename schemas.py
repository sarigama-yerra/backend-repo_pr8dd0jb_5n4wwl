"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Congregation site schemas

class Congregationstats(BaseModel):
    """
    Congregation statistics
    Collection name: "congregationstats"
    """
    publishers: int = Field(..., ge=0, description="Number of publishers")
    pioneers: int = Field(..., ge=0, description="Number of pioneers")
    youngest_publisher: str = Field(..., description="Name of the youngest publisher")
    youngest_age: Optional[int] = Field(None, ge=0, le=120)
    oldest_publisher: str = Field(..., description="Name of the oldest publisher")
    oldest_age: Optional[int] = Field(None, ge=0, le=120)
    updated_by: Optional[str] = Field(None, description="Who updated this entry")

class Galleryimage(BaseModel):
    """
    Gallery images for the landing page
    Collection name: "galleryimage"
    """
    url: HttpUrl = Field(..., description="Image URL")
    caption: Optional[str] = Field(None, description="Short caption")
    order: int = Field(0, ge=0, description="Display order")

class Contactmessage(BaseModel):
    """
    Contact messages submitted from the website
    Collection name: "contactmessage"
    """
    name: str = Field(..., min_length=2)
    email: EmailStr
    subject: str = Field(..., min_length=2)
    message: str = Field(..., min_length=5, max_length=2000)
