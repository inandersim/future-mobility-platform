from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4
from sqlalchemy import DateTime, ForeignKey, String, Boolean, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class VehicleStatus(StrEnum):
    REGISTERED = "registered"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    RETIRED = "retired"

class CertificationStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    EXPIRED = "expired"
    REVOKED = "revoked"

class Manufacturer(Base):
    __tablename__ = "manufacturers"
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    country_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False, index=True)
    organization_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False, index=True)
    legal_name: Mapped[str] = mapped_column(String(300), nullable=False)
    registration_number: Mapped[str] = mapped_column(String(120), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    __table_args__ = (UniqueConstraint("country_id", "registration_number", name="uq_manufacturer_country_registration"),)

class VehicleType(Base):
    __tablename__ = "vehicle_types"
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

class VehicleModel(Base):
    __tablename__ = "vehicle_models"
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    manufacturer_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("manufacturers.id", ondelete="RESTRICT"), index=True)
    vehicle_type_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("vehicle_types.id", ondelete="RESTRICT"), index=True)
    model_code: Mapped[str] = mapped_column(String(100), nullable=False)
    model_name: Mapped[str] = mapped_column(String(200), nullable=False)
    certification_status: Mapped[CertificationStatus] = mapped_column(String(20), default=CertificationStatus.PENDING, nullable=False)
    __table_args__ = (UniqueConstraint("manufacturer_id", "model_code", name="uq_vehicle_model_manufacturer_code"),)

class Vehicle(Base):
    __tablename__ = "vehicles"
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    country_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False, index=True)
    manufacturer_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("manufacturers.id", ondelete="RESTRICT"), index=True)
    model_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("vehicle_models.id", ondelete="RESTRICT"), index=True)
    registration_number: Mapped[str] = mapped_column(String(120), nullable=False)
    serial_number: Mapped[str] = mapped_column(String(160), nullable=False)
    status: Mapped[VehicleStatus] = mapped_column(String(20), default=VehicleStatus.REGISTERED, nullable=False)
    digital_identity_subject: Mapped[str | None] = mapped_column(String(300), nullable=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    __table_args__ = (UniqueConstraint("country_id", "registration_number", name="uq_vehicle_country_registration"), UniqueConstraint("manufacturer_id", "serial_number", name="uq_vehicle_manufacturer_serial"))
