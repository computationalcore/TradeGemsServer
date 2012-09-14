import webapp2
from google.appengine.ext import db

import utils

def player_key(player_email=None):
    """Constructs a Datastore key for a {layer entity with player_email."""

    return db.Key.from_path('Player', player_email)



class Player(db.Model):
    """Models an individual Player entry with an author"""
    nickname = db.StringProperty()
    email = db.StringProperty(required=True)
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


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Trade Gems!')



class Response(webapp2.RequestHandler):
    def get(self):
        players = db.GqlQuery("SELECT * "
                                "FROM Player "
                                "ORDER BY score DESC LIMIT 10")

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(utils.encode(players))


class Publisher(webapp2.RequestHandler):

    def get(self):
        self.response.out.write('1')

    def post(self):
        """
        Receive the data and store the entry into the datastore.
        It returns a code error or the id of the user
        return a code error.
        Code Error
        -1 - Invalid Data (It have some wrong type data)
        0 - Missing field (Pass on the validation, but something is missing)

        """

        self.response.headers['Content-Type'] = 'text/plain'

        try:
            nickname = self.request.get('nickname')
            email = self.request.get('email')
            score = int(self.request.get('score'))
            turn = int(self.request.get('turns'))
            lat = float(self.request.get('lat'))
            lon = float(self.request.get('lon'))
            city = self.request.get('city')
            state = self.request.get('state')
            country = self.request.get('country')
            provider = self.request.get('provider')
            accuracy = float(self.request.get('accuracy'))
        except:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('-1')
            return None

        #if nickname and email and score and turn and lat and lon and provider and accuracy

        player =  Player(email=email)
        player.nickname = nickname
        player.score = score
        player.turns = turn
        player.lat = lat
        player.lon = lon
        player.city = city
        player.state = state
        player.country = country
        player.provider = provider
        player.accuracy = accuracy
        player.put()
        self.response.write(player.key())
        #else:
        #    self.response.headers['Content-Type'] = 'text/plain'
        #    self.response.write('0')


app = webapp2.WSGIApplication([('/', MainPage), ('/publish', Publisher), ('/ranking', Response)], debug=True)

