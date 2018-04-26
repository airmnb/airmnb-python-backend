#!/usr/bin/env python

import os
import re

import sqlalchemy.orm.exc
from flask import Flask, request, redirect, make_response, g, send_file, url_for
from flask_oauthlib.client import OAuth
import jwt

from config import config
from db import database as db
from .i18n import get_text as _
import db.model as m
from db.db import SS


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	db.init_app(app)

	public_url_patterns = map(re.compile, [
		'/static/',
		'/favicon.ico',
		'/login',
		'/logout',
		'/debug',
		'/authorization_response',
		'/health-check',
	])
	json_url_patterns = map(re.compile, [
		'/whoami',
		'/api'
	])

	from app.api import api_1_0
	app.register_blueprint(api_1_0, url_prefix='/api/1.0/')

	oauth = OAuth()
	# TODO: generate unique state
	google = oauth.remote_app('google',
		base_url=None,
		request_token_url=None,
		access_token_url=app.config['AMB_GOOGLE_TOKEN_ENDPOINT'],
		authorize_url=app.config['AMB_GOOGLE_AUTHORIZATION_URL'],
		consumer_key=app.config['AMB_GOOGLE_APP_KEY'],
		consumer_secret=app.config['AMB_GOOGLE_APP_SECRET'],
		request_token_params={'scope': 'email profile', 'state': 'blah'},
	)


	@app.before_request
	def authenticate_request():
		for p in public_url_patterns:
			if p.match(request.path):
				return None
		# TODO: authenticate incoming request
		# if authenticated, set g.current_user and return None
		g.current_user = object()
		return None


	@app.route('/')
	def index():
		return send_file('index.html', cache_timeout=0)


	@app.route('/authorization_response')
	def authorization_response():

		# retrieve the access_token using code from authorization grant
		try:
			resp = google.authorized_response()
		except Exception as e:
			return make_response(_('error getting access token: {}').format(e), 500)

		if resp is None:
			return make_response(_('You need to grant access to continue, error: {}').format(
				request.args.get('error')), 400)

		data = jwt.decode(resp['id_token'], verify=False)
		email = data['email']
		try:
			user = m.User.query.filter(m.User.email==email).one()
		except sqlalchemy.orm.exc.NoResultFound as e:
			# user does not exist, create it
			user = m.User(
				familyName=data['family_name'],
				givenName=data['given_name'],
				# gender
				# dob
				fullName=data['name'],
				email=data['email'],
			)
			SS.add(user)
			SS.commit()

		# TODO: create jwt token for user
		return redirect(location='/debug')


	@app.route('/debug')
	def debug():
		buf = []
		for k, v in sorted(os.environ.iteritems()):
			buf.append('{}\t{}\n'.format(k, v))
		return make_response(('\n'.join(buf), {'Content-Type': 'application/json'}))


	@app.route('/health-check')
	def health_check():
		return make_response('OK', 200, {'Content-Type': 'text/plain'})


	@app.route('/login')
	def login():
		callback = url_for('authorization_response', r=request.url, _external=True)
		# TODO: setup google.request_token_params here to include redirection url here
		callback = url_for('authorization_response', _external=True)
		return google.authorize(callback=callback)


	@app.route('/logout')
	def logout():
		return redirect(location='/')


	return app
