#!/usr/bin/env python

# Importing the controllers for handling
# the generation of the pages:
from controllers import mainh
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
		
class AddGuest(webapp2.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
   
        booking = Booking()
		
	booking.guest = Guest(name = self.request.get('name'))

	booking.bed = Bed(room = self.request.get('room'), number = int(self.request.get('bed_number')))
	
        booking.put()

        self.redirect('/')

class InitBeds(webapp2.RequestHandler):
	def get(self):
	
		i = 0
		while i <=10:
			bed = Bed()
			bed.number = i
			bed.room = "B"
			
			bed.put()
			i = i+1
	

# This is the main method that maps the URLs
# of your application with controller classes.
# If a URL is requested that is not listed here,
# a 404 error is displayed.

application = webapp2.WSGIApplication([
		('/', mainh.MainPage),
		('/sign', Guestbook),
		('/initBeds', InitBeds),
		('/addGuest', AddGuest),
	],debug=True)