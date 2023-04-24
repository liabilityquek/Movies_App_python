import mongoengine as me
from .subscriptionModel import Subscription

class User(me.Document):
    name = me.StringField(required=True, lowercase=True, unique=True)
    email = me.StringField(required=True, lowercase=True, unique=True, max_length=255, min_length=1)
    password = me.StringField(required=True, trim=True, min_length=3)
    role = me.StringField(required=True, choices=("Customer", "Admin"), default="Customer")
    subscription = me.EmbeddedDocumentField(Subscription)
    trial_end = me.DateTimeField()
