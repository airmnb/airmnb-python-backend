
from flask import request, session, jsonify, g

import datetime
import db.model as m
from db import database as db
from db.db import SS
from app.api import api, caps, MyForm, Field, validators
from app.i18n import get_text as _
from . import api_1_0 as bp, InvalidUsage

from . import _helper as helper

_name = '/' + __file__.split('/')[-1].split('.')[0]


@bp.route(_name, methods=['GET'])
@api
@caps()
def get_activities():
	user = g.current_user
	activities = m.Activity.query.filter(m.Activity.providerId == user.userId).order_by(m.Activity.name).all()
	return jsonify(activities=m.Activity.dump(activities))


@bp.route(_name + '/map', methods=['GET'])
@api
@caps()
def get_map_activities():
	center_latitude = request.args['clat']
	center_longitude = request.args['clng']
	radius_meters = request.args.get('radius', 2000)
	limit = request.args.get('limit', 10)
	user = g.current_user
	activities = m.Activity.query \
		.filter(
			db.func \
			.earth_box(db.func.ll_to_earth(center_latitude, center_longitude), radius_meters) \
    	.op('@>')(db.func.ll_to_earth(m.Venue.latitude, m.Venue.longitude)) \
		) \
		.filter(m.Activity.status == 0) \
		.order_by(m.Activity.name) \
		.limit(limit) \
		.all()
	activityJsons = m.Activity.dump(activities)
	return jsonify(activities=activityJsons)


@bp.route(_name + '/ongoing', methods=['GET'])
@api
@caps()
def get_ongoing_activities():
	user = g.current_user
	activities = m.Activity.query \
		.filter(m.Activity.providerId == user.userId) \
		.filter(m.Activity.status == 0) \
		.order_by(m.Activity.name) \
		.all()
	activityJsons = m.Activity.dump(activities)
	return jsonify(activities=activityJsons)


@bp.route(_name + '/closed', methods=['GET'])
@api
@caps()
def get_closed_activities():
	user = g.current_user
	activities = m.Activity.query \
		.filter(m.Activity.providerId == user.userId) \
		.filter(m.Activity.status != 0) \
		.order_by(m.Activity.name) \
		.all()
	return jsonify(activities=m.Activity.dump(activities))


@bp.route(_name + '/recommended', methods=['GET'])
@api
@caps()
def get_recommended_activities():
	user = g.current_user
	activities = m.Activity.query.filter(m.Activity.status == 0).order_by(m.Activity.name).limit(10).all()
	activityJsons = m.Activity.dump(activities)
	return jsonify(activities=activityJsons)


def check_uuid_availability(data, key, activityId):
	if m.Activity.query.get(activityId):
		raise ValueError(_('activityId \'{0}\' is already in use').format(activityId))

def check_venue_existence(data, key, venueId):
	if not m.Venue.query.get(venueId):
		raise ValueError(_('venue \'{0}\' is not found').format(venueId))

def check_image_ids(data, key, imageIds):
	for i in imageIds:
		if not m.Image.query.get(i):
			raise ValueError(_('image \'{0}\' is not found').format(i))

@bp.route(_name, methods=['POST'])
@api
@caps()
def create_new_activity():
	
	data = MyForm(
		Field('name', is_mandatory=True, validators=[
			validators.non_blank,
			]),
		Field('info'),
		Field('venueId', is_mandatory=False,
			validators=[
				# helper.check_uuid_is_valid,
				# check_venue_existence,
			]),
		Field('providerId', is_mandatory=True, default=lambda: g.current_user.userId),
		Field('gender', is_mandatory=True, default=lambda: 3),
		Field('price', is_mandatory=True, default=lambda: 0),
		Field('currency'),
		Field('category', is_mandatory=False, default=lambda: 0, validators=[
		]),
		Field('minAge', is_mandatory=False, validators=[]),
		Field('maxAge', is_mandatory=False, validators=[]),
		Field('capacity', is_mandatory=True,
			default=lambda: 1,
			validators=[
				# validators.is_number, (), dict(min_value=1)
			],
			),
		Field('startDate', is_mandatory=False,
			normalizer=helper.normalize_date,
			),
		Field('endDate', is_mandatory=False,
			normalizer=helper.normalize_date,
			),
		Field('startTime', is_mandatory=True,
			normalizer=helper.normalize_time,
			),
		Field('endTime', is_mandatory=True,
			normalizer=helper.normalize_time,
			),
		Field('imageIds', is_mandatory=False, validators=[
			# check_image_ids,
			]),
		Field('daysOfWeek', is_mandatory=True, default=lambda: 127), # 127 = all weekdays
			# normalizer=[
			# 	helper.normalize_week_day_mask
			# ]),
		Field('status', is_mandatory=True, default=lambda: 0),
		Field('location', is_mandatory=False,)
	).get_data(copy=True)
	print('data is', data)
	daysOfWeek = data.get('daysOfWeek')
	try:
		location = data.pop('location')
	except :
		location = None

	if location:
		venue = m.Venue(name=location.get('name'), \
			longitude=location['longitude'], latitude=location['latitude'], \
			addr1=location.get('addr1'), city=location.get('city'), state=location.get('state'), \
			country=location.get('country'), providerId = data['providerId'])
		SS.add(venue)
		SS.flush()
		data['venueId'] = venue.venueId

	activity = m.Activity(**data)
	SS.add(activity)
	SS.flush()

	# add images
	imageIds = data.get('imageIds', [])
	for imageId in imageIds:
		SS.add(m.ActivityImage(activityId=activity.activityId, imageId=imageId))

	# add time slots
	st = datetime.datetime.strptime(startTime, '%H:%M').time()
	et = datetime.datetime.strptime(endTime, '%H:%M').time()
	for d in helper.enumerate_dates(startDate, endDate, daysOfWeek):
		start = datetime.datetime(d.year, d.month, d.day, st.hour, st.minute, st.second)
		end = datetime.datetime(d.year, d.month, d.day, et.hour, et.minute, et.second)
		# add vacancies
		timeslot = m.Timeslot(activityId=activity.activityId, start=start, end=end)
		SS.add(timeslot)
		SS.flush()
		for i in range(data['capacity']):
			vacancy = m.Vacancy(activityId=activity.activityId, timeslotId=timeslot.timeslotId)
			# timeslot.vacancies.add(vacancy)
			SS.add(vacancy)
	SS.flush()


	return jsonify(message=_('created activity {0} successfully'
		).format(activity.activityId),
		activity=m.Activity.dump(activity),
	)


@bp.route(_name + '/<activityId>', methods=['PUT'])
@api
@caps()
def update_new_activity(activityId):
	activity = m.Activity.query.get(activityId)
	if not activityId:
		raise InvalidUsage(_('activity {} not found').format(activityId))

	data = MyForm(
		Field('name', is_mandatory=True, validators=[
			validators.non_blank,
			]),
		Field('info'),
		Field('venueId', is_mandatory=True,
			validators=[
				helper.check_uuid_is_valid,
				check_venue_existence,
			]),
		Field('imageIds', is_mandatory=False, validators=[
			check_image_ids,
			]),
	).get_data(copy=True)

	for key in ['name', 'info']:
		if data[key] != getattr(activity, key):
			setattr(activity, key, data[key])

	if 'imageIds' in data:
		for i in activity.images:
			SS.delete(i)
		for imageId in data['imageIds']:
			SS.add(m.ActivityImage(activityId=activity.activityId, imageId=imageId))
		SS.flush()

	return jsonify(message=_('updated activity {0} successfully'
		).format(activity.activityId),
		activity=m.Activity.dump(activity),
	)


@bp.route(_name + '/<activityId>', methods=['GET'])
@api
@caps()
def get_activity(activityId):
	activity = m.Activity.query.get(activityId)
	if not activity:
		raise InvalidUsage(_('activity {0} not found').format(activityId), 404)
	return jsonify(activity=m.Activity.dump(activity))


@bp.route(_name + '/<activityId>', methods=['DELETE'])
@api
@caps()
def delete_activity(activityId):
	activity = m.Activity.query.get(activityId)
	if not activity:
		raise InvalidUsage(_('activity {0} not found').format(activityId), 404)

	# TODO: check other dependencies
	SS.delete(activity)
	return jsonify(message=_('activity {0} was deleted successfully'
		).format(activityId))

