import mongoengine as me

class History(me.Document):
    search_history = me.ListField()
