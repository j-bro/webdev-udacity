#
# #PIGS
#

import webapp2

class PigsHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Get ready for some pork!')

app = webapp2.WSGIApplication([
    ('/pigs', PigsHandler),
], debug=True)