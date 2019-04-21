# -*- coding: utf-8 -*-

import enum

from sqlalchemy import func

from app import db
from config import ROUTER_MODELS, LOWER_ROUTER_MODELS


class Router(db.Model):
    __tablename__ = "router"

    class State(enum.Enum):
        deactivated = 0
        shipping = 1
        activated = 2
        incapacitated = 3

    id = db.Column(db.Integer, primary_key=True)

    time_created = db.Column(
        db.DateTime,
        default=func.now(),
    )
    time_updated = db.Column(
        db.DateTime,
        default=func.now(),
        onupdate=func.now(),
    )

    model = db.Column(db.Enum(*ROUTER_MODELS))
    state = db.Column(db.Enum(State))

    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))

    def __init__(self, model, location_id):
        self.state = self.State.deactivated
        self.location_id = location_id
        if model.lower() in LOWER_ROUTER_MODELS:
            self.model = LOWER_ROUTER_MODELS[model.lower()]
        else:
            raise ValueError
