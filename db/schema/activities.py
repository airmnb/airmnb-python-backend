
from .. import pg, sa, metadata

t_activities = sa.Table('activities', metadata,
	sa.Column('activity_id', pg.UUID, primary_key=True, autoincrement=False, server_default=sa.text('uuid_generate_v4()'), key=u'activityId', doc=''),
	sa.Column('name', pg.TEXT, nullable=False, key=u'name', doc=''),
	sa.Column('info', pg.TEXT, key=u'info', doc=''),
	sa.Column('category', pg.INTEGER, nullable=True, key=u'category', doc=''),
	sa.Column('days_of_week', pg.SMALLINT, nullable=True, key=u'daysOfWeek', doc=''),
	sa.Column('capacity', pg.INTEGER, key=u'capacity', doc=''),
	sa.Column('min_age', pg.SMALLINT, key=u'minAge', doc=''),
	sa.Column('max_age', pg.SMALLINT, key=u'maxAge', doc=''),
	sa.Column('days_of_week', pg.SMALLINT, key=u'daysOfWeek', doc=''),
	sa.Column('status', pg.SMALLINT, nullable=True, server_default=sa.text('0'), key=u'status', doc=''),
	sa.Column('gender', pg.SMALLINT, server_default=sa.text('0'), key=u'gender', doc=''),
	sa.Column('venue_id', pg.UUID, nullable=False, key=u'venueId', doc=''),
	sa.Column('provider_id', pg.UUID, nullable=False, key=u'providerId', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
	sa.Column('price', pg.DOUBLE_PRECISION, nullable=True, key=u'price', doc=''),
	sa.Column('currency', pg.TEXT, nullable=True, key=u'currency', doc='iso 4217 currency code'),
	sa.ForeignKeyConstraint([u'venueId'], [u'venues.venueId']),
	sa.ForeignKeyConstraint([u'providerId'], [u'users.userId']),
)
