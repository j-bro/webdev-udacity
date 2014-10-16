import webapp2

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Main py")

app = webapp2.WSGIApplication([
        ('/', MainHandler)
    ])