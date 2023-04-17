import mongoengine as me

class Game(me.Document):
    title = me.StringField(required=True)
    creator = me.StringField(required=True)
    description = me.StringField(required=True)
    image_url = me.StringField()