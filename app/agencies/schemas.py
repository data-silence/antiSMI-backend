from pydantic import BaseModel


class SAgencies(BaseModel):
    telegram: str
    is_forbidden: bool
    media_type: str

    class Config:
        from_attributes = True
