# #!/usr/bin/env python
# 
# This script encrypts a string of text using the ROT13 algorithm.
# The user enters text in the text area and the encrypted text is shown once the submit button is pressed.
# 
# Author: Jeremy Brown
# 

import webapp2
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                              autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class ROTHandler(Handler):
    def fill_form(self, t=""):
        self.render("rot13.html",t=t)
    
    def get(self):
        self.fill_form()
    def post(self):
        user_input = self.request.get('text')
        encrypted_text = encrypt(user_input)
        self.fill_form(encrypted_text)

def encrypt(s):
    lowers = "abcdefghijklmnopqrstuvwxyz"
    uppers = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(0, len(s)):
        char = s[i]
        if char.isalpha():
            if char.islower():
                alpha_pos = lowers.find(char)
                new_char = lowers[(alpha_pos + 13) % 26]
                s = s[:i] + new_char + s[(i + 1):]
            elif char.isupper():
                alpha_pos = uppers.find(char)
                new_char = uppers[(alpha_pos + 13) % 26]
                s = s[:i] + new_char + s[(i + 1):]
    return s
    
app = webapp2.WSGIApplication([
    ('/rot13', ROTHandler)
], debug=True)