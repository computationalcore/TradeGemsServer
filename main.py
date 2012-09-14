import webapp2
from google.appengine.ext import db


class Player(db.Model):
    """Models an individual Guestbook entry with an author, content, and date."""
    nickname = db.StringProperty()
    email = db.StringProperty(required=True,name="key")
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


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Trade Gems!')



class Response(webapp2.RequestHandler):
    def get(self):
        players = db.GqlQuery("SELECT * "
                                "FROM Player "
                                "ORDER BY score DESC LIMIT 10")

        for player in players:
            self.response.out.write(
                '<b>%s</b> - Score: %s' % (player.nickname, player.score) )

class Publisher(webapp2.RequestHandler):
    def post(self):
        """
        Receive the data and store the entry into the datastore.
        """
        nickname = self.request.get('nickname')
        email = self.request.get('email')
        score = self.request.get('score')
        turn = self.request.get('turn')
        lat = self.request.get('lat')
        lon = self.request.get('lon')
        city = self.request.get('city')
        state = self.request.get('state')
        country = self.request.get('country')
        provider = self.request.get('provider')
        accuracy = self.request.get('accuracy')

        if (nickname and email and score and turn and lat and lon and provider
            and accuracy):
            player = Model.get(email)
            if (not player):
                player = Player(email=email)
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
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('1')
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('0')


app = webapp2.WSGIApplication([('/', MainPage), ('/publish', Publisher), ('/georanking', Response)], debug=True)

