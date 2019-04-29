# -*- coding: utf-8 -*-

from http import HTTPStatus
import json
from flask_babel import _

from flask import Blueprint, request, make_response, abort
from sqlalchemy import desc

from app import app, db
from app.models import Location
from app.utils.checkers import is_integer


api_locations = Blueprint('api_locations', __name__)


@api_locations.errorhandler(HTTPStatus.NOT_FOUND)
@api_locations.errorhandler(HTTPStatus.BAD_REQUEST)
def error_handler(error):
    return make_response(json.dumps({'error': error.description}), error.code)


@api_locations.route('/locations', methods=['GET'])
def get_locations():
    app.logger.info(_('All locations request'))
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', app.config['DEFAULT_PAGE_LIMIT'])
    if not is_integer(offset):
        abort(HTTPStatus.BAD_REQUEST, 'Offset is not integer')
    if not is_integer(limit):
        abort(HTTPStatus.BAD_REQUEST, 'Limit is not integer')
    offset = int(offset)
    limit = int(limit)
    locations = [
        x.data() for x in Location.query.order_by(
            desc(Location.time_updated)
        ).slice(offset, offset + limit).all()
    ]
    return make_response(json.dumps({'locations': locations}), HTTPStatus.OK)


@api_locations.route('/locations/<int:location_id>', methods=['GET'])
def get_location(location_id):
    app.logger.info(_('One location request: ') + str(location_id))
    location = Location.query.filter(Location.id == location_id).first()
    if location is None:
        abort(HTTPStatus.NOT_FOUND, 'Location not found')
    return make_response(json.dumps({'location': location.data()}), HTTPStatus.OK)


@api_locations.route('/locations', methods=['POST'])
def create_location():
    if not request.json:
        abort(HTTPStatus.BAD_REQUEST, 'Request should be json')
    if 'address' not in request.json.keys():
        abort(HTTPStatus.BAD_REQUEST, 'Request should contain address')
    app.logger.info(_('Create location, address: ') + str(request.json['address']))
    new_location = Location(address=request.json['address'])
    db.session.add(new_location)
    db.session.commit()
    return make_response(
        json.dumps({'location': new_location.data()}),
        HTTPStatus.CREATED,
        {'Location': f'api/locations/{new_location.id}'},
    )


@api_locations.route('/locations/<int:location_id>', methods=['PUT'])
def update_location(location_id):
    location = Location.query.filter(Location.id == location_id).first()
    if location is None:
        abort(HTTPStatus.NOT_FOUND, 'Location not found')
    if not request.json:
        abort(HTTPStatus.BAD_REQUEST, 'Request should be json')
    app.logger.info(_('Update location, address: ') + str(request.json['address']))
    location.address = request.json.get('address', location.address)
    db.session.add(location)
    db.session.commit()
    return make_response(json.dumps({'location': location.data()}), HTTPStatus.OK)


@api_locations.route('/locations/<int:location_id>', methods=['DELETE'])
def delete_location(location_id):
    location = Location.query.filter(Location.id == location_id).first()
    if location is None:
        abort(HTTPStatus.NOT_FOUND, 'Location not found')
    app.logger.info(_('Delete location, id: ') + str(location_id))
    db.session.delete(location)
    db.session.commit()
    return make_response('', HTTPStatus.NO_CONTENT)
