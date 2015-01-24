#!/usr/bin/env python
import webapp2
import os
import urllib
import jinja2

# to sort dictionary
import collections
import datetime
from datetime import date

from google.appengine.ext import ndb
from models.models import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# Handle bookings		
class AddGuest(webapp2.RequestHandler):
	def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
   
		guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)  
		
   
		booking = Booking()
		
		booking.guest = Guest(name = self.request.get('name'))

		booking.bed = Bed(room = self.request.get('room'), number = int(self.request.get('bed_number')))
		
		booking.price = int(self.request.get('price'))
		
		
		#convert check in date with datetime 
		booking.check_in_date = datetime.datetime.strptime(self.request.get('check_in_date'), '%d/%m/%Y').date()
		
		booking.check_out_date = datetime.datetime.strptime(self.request.get('check_out_date'), '%d/%m/%Y').date()
		
		booking.put()
		
		query_params = {'guestbook_name': guestbook_name}
		
		self.redirect('/?' + urllib.urlencode(query_params))
		
class NewGuestPage(webapp2.RequestHandler):
	def get(self):
	
		DEFAULT_GUESTBOOK_NAME = '20001010'
	
		guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
	
		template_values = {
				'guestbook_name': urllib.quote_plus(guestbook_name)
				
			}
	
		template = JINJA_ENVIRONMENT.get_template('new_guest_page.html')
		self.response.write(template.render(template_values))