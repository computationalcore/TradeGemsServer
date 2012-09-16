import webapp2
from google.appengine.ext import db
import hashlib

from model import User, Player, user_key

import utils


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Trade Gems!')


class Response(webapp2.RequestHandler):
    def get(self):
        

        query_string = "SELECT * FROM Player "
        limit = 10
        parent_key = self.request.get('p')

        try:
            type = unicode(self.request.get('t'))
            if type == 'geo':
            #Location data
                limit = 20
                query_string = query_string + ", Player.lat, Player.lon, Player.accuracy"
                try:
                    country = unicode(self.request.get('country'))
                    query_string = query_string + ", Player.country = %s" % country
                    try:
                        state = unicode(self.request.get('state'))
                        query_string = query_string + ", Player.state = %s" % state
                        try:
                            city = unicode(self.request.get('city'))
                            query_string = query_string + ", Player.city = %s" % city
                        except:
                            pass
                    except:
                        pass
                except:
                    pass
        except:
            pass

        try:
            lim = int(self.request.get('l'))
            if lim>=10 and lim<=100:
                limit = lim
        except:
            pass


        if parent_key:
            players = db.GqlQuery(query_string +
                                  "WHERE ANCESTOR IS :1 "
                                  "ORDER BY score DESC LIMIT %s" % limit,
                                  parent_key)

        else:
            players = db.GqlQuery(query_string +
                                  "ORDER BY score DESC LIMIT %s" % limit)

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
        -1 - Invalid Data (It have some wrong type data) or Missing field
        (Pass on the validation, but something is missing)

        """

        self.response.headers['Content-Type'] = 'text/plain'

        try:
            nickname = unicode(self.request.get('nickname'))
            email = self.request.get('email')
            score = int(self.request.get('score'))
            turn = int(self.request.get('turns'))
            lat = float(self.request.get('lat'))
            lon = float(self.request.get('lon'))
            city = unicode(self.request.get('city'))
            state = unicode(self.request.get('state'))
            country = unicode(self.request.get('country'))
            provider = unicode(self.request.get('provider'))
            accuracy = float(self.request.get('accuracy'))
        except:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('-1')
            return None

        #if nickname and email and score and turn and lat and lon and provider and accuracy
        if not (nickname and email and score and turn and lat and lon and city and state
                and country and provider and accuracy):
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('0')
            return None
        player_key = email
        parent_key = user_key(email)
        # Query interface constructs a query using instance methods
        q = Player.all()
        q.ancestor(parent_key)
        q.filter("email =", email)
        q.filter("city =", city)
        q.filter("state =", state)
        q.filter("country", country)
        # Query is not executed until results are accessed
        #This only get the first the result (if the use of database is limited to this
        #app, the first one is the only one possible)
        try:
            player = (q.run(limit=1)).next()
        #The player entry do not exists (limited by location and email)
        except:
            player =  Player(parent=parent_key)
            player.email = email
            player.city = city
            player.state = state
            player.country = country
        player.score = score
        player.turns = turn
        player.lat = lat
        player.lon = lon
        player.provider = provider
        player.accuracy = accuracy
        player.put()
        user = User(key=parent_key)
        user.nickname = nickname
        user.put()
        self.response.write(parent_key)


app = webapp2.WSGIApplication([('/', MainPage), ('/publish', Publisher), ('/ranking', Response)], debug=True)

