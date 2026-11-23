from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class FieldDef(BaseModel):
    name: str = Field(min_length=1, max_length=50, pattern=r"^[a-z][a-z0-9_]*$")
    label: str = Field(min_length=1, max_length=100)
    type: Literal["text", "email", "textarea"] = "text"
    required: bool = False


class WidgetIn(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    type: Literal["signup_form", "contact_form", "cta"]
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=500)
    fields: list[FieldDef] = Field(default_factory=list, max_length=20)
    button_text: str = Field(default="Submit", min_length=1, max_length=40)
    display_options: dict = Field(default_factory=dict)