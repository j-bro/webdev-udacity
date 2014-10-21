#!/usr/bin/env python
# 
# 
# 
#

import os
import webapp2
import jinja2
import cgi
import re

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class SignupHandler(Handler):
    def get(self):
        self.write_form()
    
    def post(self):
        u_username = self.request.get(cgi.escape('username'))
        u_password = self.request.get(cgi.escape('password'))
        u_verify = self.request.get(cgi.escape('verify'))
        u_email = self.request.get(cgi.escape('email'))
        
        # Blank error statements
        user_error=""
        pass_error=""
        veri_error=""
        email_error=""
        
        valid = True
        if not check_username(u_username):
            valid = False
            user_error="That's not a valid username"
        if not check_password(u_password):
            valid = False
            pass_error="That wasn't a valid password"
        if not match_passwords(u_password, u_verify):
            valid = False
            veri_error="The passwords didn't match"
        if not check_email(u_email):
            valid = False
            email_error="That's not a valid email"
            
        # Redirects the user if input is valid, or indicates the errors if not
        if valid:
            self.redirect("/signup/welcome?u=%s" % u_username)
        else:
            self.write_form(username=u_username, email=u_email, user_error=user_error, pass_error=pass_error, veri_error=veri_error, email_error=email_error)
    
    
    def write_form(self, username="", password="", verify="", email="", user_error="", pass_error="", veri_error="", email_error=""):
        self.render("signup.html", username=username,
                                    password=password,
                                    verify=verify,
                                    email=email,
                                    usernameerror=user_error,
                                    passworderror=pass_error,
                                    verifyerror=veri_error,
                                    emailerror=email_error)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
        
# Verifies the validity of the provided username
def check_username(username):
    return USER_RE.match(username)

# Verifies the validity of the provided password
def check_password(password):
    return PASS_RE.match(password)

# Verifies that both passwords match
def match_passwords(p1, p2):
    return p1 == p2

# Verifies the validity of the provided email
def check_email(email):
    if len(email) == 0:
        return True
    else:
        return EMAIL_RE.match(email)



# Welcome message handler
class WelcomeHandler(Handler):
    welcome_message = """
    <h1>Welcome, %s!</h1>
    """
    
    def get(self):
        username = self.request.get('u')
        if check_username(username):
            self.write(self.welcome_message % username)
        else:
            self.response.redirect("/signup")



# Webapp initializer
app = webapp2.WSGIApplication([
    ('/signup', SignupHandler),
    ('/signup/welcome', WelcomeHandler)
    ], debug=True)
