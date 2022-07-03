from sqlalchemy import Column, func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Session

from database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    session_key = Column(String)


def create_organization(db: Session, title: str, session_key: str):
    organization = Organization(title=title, session_key=session_key)
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization


def get_organization(db: Session, item_id: int):
    return db.query(Organization).filter(Organization.id == item_id).first()


def update_organization(db: Session, item_id: int, title: str):
    organization = get_organization(db, item_id)
    organization.title = title
    db.commit()
    db.refresh(organization)
    return organization


def get_organizations(db: Session, session_key: str, skip: int = 0, limit: int = 100):
    return (
        db.query(Organization)
        .filter(Organization.session_key == session_key)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_organizations_count(db: Session) -> int:
    return db.query(func.count(Organization.id)).scalar()


def delete_organization(db: Session, item_id: int):
    organization = get_organization(db, item_id)
    db.delete(organization)
    db.commit()
