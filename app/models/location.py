# -*- coding: utf-8 -*-

from sqlalchemy import func
from sqlalchemy.orm import relationship

from app import db


class Location(db.Model):
    __tablename__ = 'location'

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

    routers = relationship('Router')

    def __init__(self, address):
        self.address = address

    def data(self):
        return {
            'id': self.id,
            'address': self.address,
            'time_created': str(self.time_created),
            'time_updated': str(self.time_updated),
            'routers': [router.id for router in self.routers]
        }
