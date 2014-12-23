import webapp2
import urllib

from models.models import *

# Handle bookings		
class AddGuest(webapp2.RequestHandler):
	def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
   
		guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)  
		
   
		booking = Booking()
		
		booking.guest = Guest(name = self.request.get('name'))

		booking.bed = Bed(room = self.request.get('room'), number = int(self.request.get('bed_number')))
		
		booking.price = int(self.request.get('price'))
		
		booking.put()
		
		query_params = {'guestbook_name': guestbook_name}
		
		self.redirect('/?' + urllib.urlencode(query_params))