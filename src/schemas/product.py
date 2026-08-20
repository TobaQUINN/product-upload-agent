# Structure of the product draft

from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel, Field


class ProductDraft(BaseModel):
    """
    Product information prepared by the Product Upload Agent.

    AI-generated fields are populated by the agent.
    Business fields are completed manually by an admin.
    """

    # AI-generated information
    product_name: str = Field(
        description="The verified name of the product."
    )

    short_description: str = Field(
        description="A concise description suitable for the product listing."
    )

    full_description: str = Field(
        description="A detailed product description based on verified information."
    )

    # Information about the research
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Agent confidence in the product identification."
    )

    sources: list[str] = Field(
        default_factory=list,
        description="Sources used to identify and research the product."
    )

    # Admin/business fields
    category: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    availability: Optional[bool] = None
    featured: Optional[bool] = None

    # Image
    image_path: Optional[str] = None


class ProductIdentification(BaseModel):
    brand: str
    product_name: str
    model_number: str
    product_type: str
    color_variant: str
    visible_text: list[str]
    visible_specifications: list[str]
