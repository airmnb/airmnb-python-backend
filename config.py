
import logging
import os

class Config:
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
	SQLALCHEMY_DATABASE_URI = 'postgres://qstqzkzu:wIRQ-yASKMaE7hEdABZCD7cSKUuC40DA@stampy.db.elephantsql.com:5432/qstqzkzu'
	LOG_LEVEL = logging.INFO

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	LOG_LEVEL = logging.DEBUG


class StageConfig(Config):
	pass


class ProductionConfig(Config):
	pass


config = {
	'development': DevelopmentConfig,
	'stage': StageConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig,
}
