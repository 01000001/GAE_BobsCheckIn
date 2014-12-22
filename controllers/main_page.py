#!/usr/bin/env python
import webapp2
import os
import urllib
import jinja2

# to sort dictionary
import collections
from datetime import date

from google.appengine.ext import ndb
from models.models import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_DATE = date(2012,12,29)
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

###############			
 
		greetings = greetings_query.fetch(10)
		
		bookings_query = Booking.query()
		bookings = bookings_query.fetch()
	
		beds_query = Bed.query().order(Bed.room).order(Bed.number)
		beds = beds_query.fetch()
		
		
		####
		# Build a dictionary that will collect all the necessary data to be displayed
		display = {}
		
		#make unique key per bed for the dictionary
		i = 0
		
		for bed in beds:
			
			model = {}
			
			#if there is a booking for the given bed
			check_bed = bookings_query.filter(
			Booking.bed.number == bed.number, 
			Booking.bed.room == bed.room
			).fetch()
			
			
			#if there is a booking for the given bed
			if check_bed:
				booking = bookings_query.filter(Booking.bed.number == bed.number, Booking.bed.room == bed.room).fetch()
				
				for found in booking:
			
					nights = found.check_out_date - found.check_in_date
				
					model['guest.name'] = found.guest.name
					model['bed.room'] = found.bed.room
					model['bed.number'] = found.bed.number
					model['nights'] = nights.days
					model['check_in_date'] = found.check_in_date
			
			#if there is no booking			
			else:
			
				model['guest.name']= "Empty"
				model['bed.room'] = bed.room
				model['bed.number'] = bed.number
				model['nights'] = "Empty"
				model['check_in_date'] = date(1000,1,1)
				
			display[i] = model
			
			#increase unique key per bed for the dictionary
			i = i+1
		
#		sorted_display = collections.OrderedDict(sorted(display.items()))
		
		template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'bookings': bookings,
			'beds' : beds,
			'display': display,
			'DEFAULT_DATE' : DEFAULT_DATE
			
		}

		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

