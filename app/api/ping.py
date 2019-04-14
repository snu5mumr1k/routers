# -*- coding: utf-8 -*-

from http import HTTPStatus

from flask import Blueprint, make_response


api_ping = Blueprint('api_ping', __name__)


@api_ping.route('/ping', methods=['GET'])
def ping():
    return make_response("", HTTPStatus.OK)
