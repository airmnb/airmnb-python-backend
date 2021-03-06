import os

from flask import request, session, jsonify

import db.model as m
from db.db import SS
from app.api import api, caps, MyForm, Field, validators
from app.i18n import get_text as _
from . import api_1_0 as bp, InvalidUsage

from . import _helper as helper

_name = '/' + __file__.split(os.sep)[-1].split('.')[0]


@bp.route(_name, methods=['POST'])
@api
@caps()
def create_new_booking():
	return jsonify(message=_('created booking {0} successfully'
		).format('newbooking'),
		booking=dict(name='stub'),
	)


@bp.route(_name + '/<bookingId>', methods=['GET'])
@api
@caps()
def get_booking(bookingId):
	return jsonify(booking=dict(name='tbd', bookingId=bookingId))


@bp.route(_name + '/<bookingId>', methods=['PUT'])
@api
@caps()
def update_booking():
	return jsonify(booking=dict(name='tbd', bookingId=bookingId))


@bp.route(_name + '/<bookingId>/feedback', methods=['POST'])
@api
@caps()
def create_booking_feedback():
	return jsonify(feedback=dict(bookingId=bookingId, comment='something'))

