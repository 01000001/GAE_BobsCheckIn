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


# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

class MainPage(webapp2.RequestHandler):
	def get(self):
	
		DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
	
		guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)	
        
		greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)

###############			
 
		DEFAULT_DATE = datetime.datetime.strptime(urllib.quote_plus(guestbook_name), '%Y%m%d').date()
		EMTY_ROOM_DATE = date(1000,1,1)
		
##############
		#Queries
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

#######		
		#Logic to display guests for a given day
		for bed in beds:
			
			model = {}
			
			#if there is a booking for the given bed
			#since GAE does not allow me to include more 
			#than one in-equivalence queries on different 
			#properties, have to move part of the logic to the view
			#(that is checking the stays for a given day)
			
			#Display guests in their bed that has to check out later then "today"
			check_bed = bookings_query.filter(
			Booking.bed.number == bed.number, 
			Booking.bed.room == bed.room,
			Booking.check_out_date > DEFAULT_DATE,
			).fetch()
			
			
			#if there is a booking for the given bed for "today"
			if check_bed:
				
				for found in check_bed:
			
					nights = found.check_out_date - DEFAULT_DATE
				
					model['guest.name'] = found.guest.name
					model['bed.room'] = found.bed.room
					model['bed.number'] = found.bed.number
					model['nights'] = nights.days
					
					if found.check_in_date == DEFAULT_DATE:
						model['price'] = found.price
					else:
						model['price'] = "-"
					model['check_in_date'] = found.check_in_date
			
			#if there is no booking			
			else:
			
				model['guest.name']= "-"
				model['bed.room'] = bed.room
				model['bed.number'] = bed.number
				model['nights'] = "-"
				model['price'] = "-"
				model['check_in_date'] = EMTY_ROOM_DATE
				
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
			'DEFAULT_DATE': DEFAULT_DATE,
			'EMTY_ROOM_DATE' : EMTY_ROOM_DATE,
			
		}

		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

