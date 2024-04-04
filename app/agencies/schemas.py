from pydantic import BaseModel


class SAgencies(BaseModel):
    telegram: str | None
    is_forbidden: bool
    media_type: str | None

    class Config:
        from_attributes = True


class SAllAgencies(SAgencies):
    name: str
    type: str | None
    country: str | None
    region: str | None
    rf_feds_subj: str | None
    settlement_type: str | None
    settlement_name: str | None
    last: str | None
    first: str | None
    street: str | None
    street_type: str | None

    class Config:
        from_attributes = True
