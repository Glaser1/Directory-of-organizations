from sqlalchemy import String, CheckConstraint, ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr, relationship


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr.directive
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"


organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", ForeignKey("activities.id"), primary_key=True),
)


class Organization(Base):
    title: Mapped[str] = mapped_column(unique=True)
    phones: Mapped[list["PhoneNumber"]] = relationship(back_populates="organization")
    building: Mapped[list["Building"]] = relationship(back_populates="organization")
    activities: Mapped[list["Activity"]] = relationship(
        secondary="organization_activity", back_populates="organizations"
    )
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))


class PhoneNumber(Base):
    __tablename__ = "phone_numbers"
    __table_args__ = (CheckConstraint("phone ~ '^\\+?\\d{10,15}$'", name="check_phone_format"),)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    organization: Mapped["Organization"] = relationship("Organization", back_populates="phones")


class Activity(Base):
    __tablename__ = "activities"

    title: Mapped[str]
    parent_id: Mapped[int]
    organizations: Mapped[list["Organization"]] = relationship(
        secondary="organization_activity", back_populates="activities"
    )
    children: Mapped[list["Activity"]] = relationship("Activity", back_populates="parent")
    parent = relationship("Node", back_populates="children", remote_side=[id])


class Building(Base):
    address: Mapped[str] = mapped_column(String(200), unique=True)
    latitude: Mapped[float]
    longitude: Mapped[float]

    organizations: Mapped[list["Organization"]] = relationship("Organization", back_populates="building")
