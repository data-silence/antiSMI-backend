from sqlalchemy.orm import mapped_column, Mapped

from app.db import Base


class Agencies(Base):
    __tablename__ = 'agencies'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()
    telegram: Mapped[str] = mapped_column()
    is_parsing: Mapped[bool] = mapped_column()
    priority: Mapped[str] = mapped_column()
    mono_category: Mapped[str] = mapped_column()
    ya_link: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    zip_code: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column()
    region: Mapped[str] = mapped_column()
    rf_feds_subj: Mapped[str] = mapped_column()
    settlement_type: Mapped[str] = mapped_column()
    settlement_name: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    chief_name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    last: Mapped[str] = mapped_column()
    first: Mapped[str] = mapped_column()
    middle: Mapped[str] = mapped_column()
    street: Mapped[str] = mapped_column()
    street_type: Mapped[str] = mapped_column()
    language: Mapped[str] = mapped_column()
    prior_country: Mapped[str] = mapped_column()
    benef_country: Mapped[str] = mapped_column()
    is_forbidden: Mapped[bool] = mapped_column(nullable=False)
    media_type: Mapped[str] = mapped_column()

    def __str__(self):
        return f"Agencie {self.name, self.url}"
