#!/usr/bin/env python
import webapp2
import os
import urllib
import jinja2

from google.appengine.ext import ndb
from models.models import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

class MainPage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)
		
	bookings_query = Booking.query()
	bookings = bookings_query.fetch()
	
	beds = Bed.query().fetch()

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'bookings': bookings,
			'beds' : beds,
			
		}

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

