from pydantic import BaseModel


class SAgencies(BaseModel):
    telegram: str
    is_forbidden: bool

    class Config:
        from_attributes = True
