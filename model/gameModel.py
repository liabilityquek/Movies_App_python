import mongoengine as me
from .userModel import User

class Game(me.Document):
    title = me.StringField(required=True)
    creator = me.StringField(required=True)
    description = me.StringField(required=True)
    image_url = me.StringField()
    likes = me.ListField(me.ReferenceField(User))
    site = me.StringField(required=True)