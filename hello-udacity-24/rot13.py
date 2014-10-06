# #!/usr/bin/env python
# 
# This script encrypts a string of text using the ROT13 algorithm.
# The user enters text in the text area and the encrypted text is shown once the submit button is pressed.
# 
# Author: Jeremy Brown
# 

import webapp2
import cgi

html = """
<h1>ROT13</h1>
<form name="rot13form" method="post">
	<textarea name="text" autofocus="true" rows="12" cols="100" placeholder="Type some text to be encrypted...">%(t)s</textarea>
	<br>
	<br>
	<input type="submit">
</form>
"""

class ROTHandler(webapp2.RequestHandler):
    def fill_form(self, t=""):
        self.response.write(html % {"t": t})
    
    def get(self):
        self.fill_form()
    def post(self):
        user_input = self.request.get('text')
        encrypted_text = encrypt(user_input)
        self.fill_form(cgi.escape(encrypted_text))

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