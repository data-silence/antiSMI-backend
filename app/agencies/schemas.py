from pydantic import BaseModel


class SAgencies(BaseModel):
    telegram: str | None
    is_forbidden: bool
    media_type: str | None

    class Config:
        from_attributes = True


class SAllAgencies(SAgencies):
    name: str
    # url: str
    # is_parsing: bool
    # priority: str
    # mono_category: str
    # ya_link: str
    # email: str
    type: str | None
    # address: str
    # zip_code: str
    country: str | None
    region: str | None
    rf_feds_subj: str | None
    settlement_type: str | None
    settlement_name: str | None
    # phone: str
    # chief_name: str
    # description: str
    last: str | None
    first: str | None
    # middle: str
    street: str | None
    street_type: str | None
    # language: str
    # prior_country: str
    # benef_country: str


    class Config:
        from_attributes = True