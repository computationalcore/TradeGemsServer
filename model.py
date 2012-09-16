from google.appengine.ext import db


def user_key(user_email=None):
    """Constructs a Datastore key for a User entity with player_email."""

    return db.Key.from_path('User', user_email)

class User(db.Model):
    """Models an individual Player entry with an author"""
    nickname = db.StringProperty()
    facebook = db.StringProperty()
    twitter = db.StringProperty()

class Player(db.Model):
    """Models an individual Player entry with an author"""
    email = db.StringProperty()
    score = db.IntegerProperty()
    turns = db.IntegerProperty()
    lat = db.FloatProperty()
    lon = db.FloatProperty()
    city = db.StringProperty()
    state = db.StringProperty()
    country = db.StringProperty()
    provider = db.StringProperty()
    accuracy = db.FloatProperty()
    date = db.DateTimeProperty(auto_now_add=True)

    def to_dict(self):
        return dict((p, unicode(getattr(self, p))) for p in self.properties()
            if getattr(self, p) is not None)