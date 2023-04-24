import mongoengine as me
from datetime import datetime

class Subscription(me.EmbeddedDocument):
    plan = me.StringField(required=True, choices=("Monthly", "Annually"), default="Monthly")
    price = me.FloatField(required=True, default=9.99)
    start_date = me.DateTimeField(default=datetime.utcnow)
    end_date = me.DateTimeField()
    reinstate_date = me.DateTimeField()
