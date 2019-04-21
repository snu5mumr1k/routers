# -*- coding: utf-8 -*-

from sqlalchemy import func
from sqlalchemy.orm import relationship

from app import db


class Location(db.Model):
    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)

    address = db.Column(db.Text)

    time_created = db.Column(
        db.DateTime,
        default=func.now()
    )
    time_updated = db.Column(
        db.DateTime,
        default=func.now(),
        onupdate=func.now(),
    )

    routers = relationship("Router")

    def __init__(self, address):
        self.address = address
