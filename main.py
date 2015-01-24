#!/usr/bin/env python

# Importing the controllers for handling
# the generation of the pages:
from controllers import main_page, add_guest
from models.models import *
from models.guests_model import *

# Importing some of Google's AppEngine modules:
import os
import urllib

from google.appengine.ext import ndb

import jinja2
import webapp2

class Guestbook(webapp2.RequestHandler):
	def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        
		guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)        
		greeting = Greeting(parent=guestbook_key(guestbook_name))
        
		greeting.content = self.request.get('content')
		greeting.put()

		query_params = {'guestbook_name': guestbook_name}
        
		self.redirect('/?' + urllib.urlencode(query_params))

		
		
## Generate Beds
class InitBeds(webapp2.RequestHandler):
	def get(self):
	
		i = 0
		while i <=10:
			bed = Bed()
			bed.number = i
			bed.room = "C"
			
			bed.put()
			i = i+1
	

# Maps the URLsof the plication with controller classes
application = webapp2.WSGIApplication([
		('/', main_page.MainPage),
		('/sign', Guestbook),
		('/initBeds', InitBeds),
		('/addGuest', add_guest.AddGuest), #method to add a guest
		('/new_guest', add_guest.NewGuestPage) #display add guest page
	],debug=True)