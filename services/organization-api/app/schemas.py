from uuid import UUID
from pydantic import BaseModel, Field

class CountryCreate(BaseModel):
    iso2: str = Field(min_length=2, max_length=2)
    iso3: str = Field(min_length=3, max_length=3)
    name: str = Field(min_length=2, max_length=200)
    default_locale: str = "en-US"
    default_timezone: str = "UTC"

class CountryResponse(CountryCreate):
    id: UUID
    sovereign: bool
    active: bool

class OrganizationCreate(BaseModel):
    country_id: UUID
    parent_id: UUID | None = None
    legal_name: str = Field(min_length=2, max_length=300)
    display_name: str = Field(min_length=2, max_length=200)
    organization_type: str = Field(min_length=2, max_length=60)
    registration_number: str | None = Field(default=None, max_length=120)

class OrganizationResponse(OrganizationCreate):
    id: UUID
    active: bool

class ScopeDecision(BaseModel):
    allowed: bool
    reason: str
