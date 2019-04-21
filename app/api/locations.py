from flask import Blueprint, request, make_response, abort
from app import app, db
from app.models import Location
from sqlalchemy import desc
import json


api_locations = Blueprint('api_locations', __name__)


def is_integer(num):
    if isinstance(num, int):
        return True
    elif isinstance(num, str):
        try:
            num = int(num)
            return True
        except ValueError:
            return False
    else:
        return False

@api_locations.errorhandler(404)
@api_locations.errorhandler(400)
def error_handler(error):
    return make_response(json.dumps({'error': error.description}), error.code)


@api_locations.route('/locations', methods=['GET'])
def get_locations():
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', app.config['DEFAULT_PAGE_LIMIT'])
    if not is_integer(offset):
        abort(400, 'Offset is not integer')
    if not is_integer(limit):
        abort(400, 'Limit is not integer')
    offset = int(offset)
    limit = int(limit)
    locations = [
            x.data() for x in Location.query.order_by(
                    desc(Location.time_updated)
                ).slice(offset, offset + limit).all()
        ]
    return make_response(json.dumps({'locations': locations}), 200)


@api_locations.route('/locations/<int:location_id>', methods=['GET'])
def get_location(location_id):
    location = Location.query.filter(Location.id == location_id).first()
    if location is None:
        abort(404, 'Location not found')
    return make_response(json.dumps({'location': location.data()}), 200)
