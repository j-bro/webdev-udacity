#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import webapp2
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

class MainHandler(Handler):
    def write_form(self, error="", month="", day="", year=""):
        self.render("birthday.html", error=error,
        							month=month,
        							day=day,
        							year=year)

    def get(self):
        self.write_form()

    def post(self):
    	user_month = self.request.get('month')
    	user_day = self.request.get('day')
    	user_year = self.request.get('year')

    	month = valid_month(user_month)
    	day = valid_day(user_day)
    	year = valid_year(user_year)

    	if not (month and day and year):
    		self.write_form("That doesn't look valid to me, friend.", user_month, user_day, user_year)
    	else:
    		self.redirect("/birthday/thanks")

class ThanksHandler(Handler):
	def get(self):
		self.write("Thanks, that's a totally valid day")


months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def valid_month(month):
 	month = month.capitalize();
   	if (month in months):
  	    return month

def valid_day(day):
    if day:
        if day.isdigit():
            day = int(day)
            if day > 0 and day <= 31:
                return day

def valid_year(year):
  	if year:
  		if year.isdigit():
   			year = int(year)
   			if year >= 1990 and year <= 2020:
   				return year

app = webapp2.WSGIApplication([
    ('/birthday', MainHandler),
    ('/birthday/thanks', ThanksHandler)], debug=True)