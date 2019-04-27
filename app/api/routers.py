# -*- coding: utf-8 -*-

import json
from http import HTTPStatus

from flask import Blueprint, request, make_response, abort
from sqlalchemy import desc

from app import app, db
from app.models import Router, Location
from app.utils.checkers import is_integer
from config import LOWER_ROUTER_MODELS

api_routers = Blueprint('api_routers', __name__)


@api_routers.errorhandler(HTTPStatus.NOT_FOUND)
@api_routers.errorhandler(HTTPStatus.BAD_REQUEST)
def error_handler(error):
    return make_response(json.dumps({'error': error.description}), error.code)


@api_routers.route('/routers', methods=['GET'])
def get_routers():
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', app.config['DEFAULT_PAGE_LIMIT'])
    model = request.args.get('model', None)
    state = request.args.get('state', None)
    location_id = request.args.get('location_id', None)

    if not is_integer(offset):
        abort(HTTPStatus.BAD_REQUEST, 'Offset is not integer')
    if not is_integer(limit):
        abort(HTTPStatus.BAD_REQUEST, 'Limit is not integer')

    offset = int(offset)
    limit = int(limit)
    routers = Router.query

    if model is not None:
        routers = routers.filter(Router.model == model)
    if state is not None:
        routers = routers.filter(Router.state == state)
    if location_id is not None:
        routers = routers.filter(Router.location_id == location_id)

    routers = [
        x.data() for x in routers.order_by(
            desc(Router.time_updated)
        ).slice(offset, offset + limit).all()
    ]
    return make_response(json.dumps({'routers': routers}), HTTPStatus.OK)


@api_routers.route('/routers/<int:router_id>', methods=['GET'])
def get_router(router_id):
    router = Router.query.filter(Router.id == router_id).first()
    if router is None:
        abort(HTTPStatus.NOT_FOUND, 'Router not found')
    return make_response(json.dumps({'router': router.data()}), HTTPStatus.OK)


@api_routers.route('/routers', methods=['POST'])
def create_router():
    if not request.json:
        abort(HTTPStatus.BAD_REQUEST, 'Request should be json')
    if 'model' not in request.json:
        abort(HTTPStatus.BAD_REQUEST, 'Request should contain model')
    if request.json['model'].lower() not in LOWER_ROUTER_MODELS:
        abort(HTTPStatus.BAD_REQUEST, 'Model is not supported')
    if 'location_id' not in request.json:
        abort(HTTPStatus.BAD_REQUEST, 'Router needs location_id')

    new_router = Router(model=request.json['model'], location_id=request.json['location_id'])
    db.session.add(new_router)
    db.session.commit()
    return make_response(
        json.dumps({'router': new_router.data()}),
        HTTPStatus.CREATED,
        {'Location': f'api/routers/{new_router.id}'}
    )


@api_routers.route('/routers/<int:router_id>', methods=['PUT'])
def update_router(router_id):
    router = Router.query.filter(Router.id == router_id).first()
    if router is None:
        abort(HTTPStatus.NOT_FOUND, 'Router not found')
    if not request.json:
        abort(HTTPStatus.BAD_REQUEST, 'Request should be json')

    if 'model' in request.json:
        if request.json['model'].lower() not in LOWER_ROUTER_MODELS:
            abort(HTTPStatus.BAD_REQUEST, 'Model is not supported')
        else:
            router.model = request.json['model']

    if 'state' in request.json:
        state = request.json['state']
        if state not in Router.State.__members__:
            abort(HTTPStatus.BAD_REQUEST, f'State {state} is not supported')
        else:
            router.state = Router.State[state]

    if 'location_id' in request.json:
        location_id = request.json['location_id']
        if not Location.query.filter(Location.id == location_id).first():
            abort(HTTPStatus.BAD_REQUEST, 'Location does not exist')
        router.location_id = location_id

    db.session.add(router)
    db.session.commit()
    return make_response(json.dumps({'router': router.data()}), HTTPStatus.OK)


@api_routers.route('/routers/<int:router_id>', methods=['DELETE'])
def delete_router(router_id):
    router = Router.query.filter(Router.id == router_id).first()
    if router is None:
        abort(HTTPStatus.NOT_FOUND, 'Router not found')
    db.session.delete(router)
    db.session.commit()
    return make_response('', HTTPStatus.NO_CONTENT)
