import mongoengine as me
from .userModel import User

class Favourite(me.Document):
    name= me.ReferenceField(User, required=True)
    title = me.StringField(required=True)
    year = me.StringField()
    rating = me.FloatField()
    casts = me.ListField()
    description = me.StringField()
    image_url = me.StringField()