#!/usr/bin/env python
# 
# 
# 
#

import webapp2
import cgi
import re

form = """
<form method="post">
	<h1>Signup</h1>
	<br>
	<label>Username<input type="text" name="username" value="%(username)s" required></label>
    <div style="color: red">%(usernameerror)s</div>
    <br>
	<label>Password<input type="password" name="password" value="%(password)s" required></label>
    <div style="color: red">%(passworderror)s</div>
    <br>
	<label>Verify Password<input type="password" name="verify" value="%(verify)s" required></label>
    <div style="color: red">%(verifyerror)s</div>
    <br>
    <label>Email (optional) <input type="text" name="email" value="%(email)s"></label>
    <div style="color: red">%(emailerror)s</div>
	<br>
	<br>
	<br>
	<input type="submit">
</form>
"""

class SignupHandler(webapp2.RequestHandler):
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
            self.redirect("/welcome?u=%s" % u_username)
        else:
            self.write_form(username=u_username, email=u_email, user_error=user_error, pass_error=pass_error, veri_error=veri_error, email_error=email_error)
    
    
    def write_form(self, username="", password="", verify="", email="", user_error="", pass_error="", veri_error="", email_error=""):
        self.response.write(form % {"username": username,
                                    "password": password,
                                    "verify": verify,
                                    "email": email,
                                    "usernameerror": user_error,
                                    "passworderror": pass_error,
                                    "verifyerror": veri_error,
                                    "emailerror": email_error})

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
class WelcomeHandler(webapp2.RequestHandler):
    welcome_message = """
    <h1>Welcome, %s!</h1>
    """
    
    def get(self):
        username = self.request.get('u')
        if check_username(username):
            self.response.write(self.welcome_message % username)
        else:
            self.response.redirect("/signup")



# Webapp initializer
app = webapp2.WSGIApplication([
    ('/signup', SignupHandler),
    ('/signup/welcome', WelcomeHandler)
    ], debug=True)
